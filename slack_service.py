import asyncio
import datetime as dt
from http.client import HTTPException
import httpx
import os, requests
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.errors import SlackApiError

from model.slack import SlackAPI

# Load variables from .env file
load_dotenv()
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

slack = SlackAPI(SLACK_BOT_TOKEN)
app = App(token=SLACK_BOT_TOKEN)

@app.event("app_mention") 
def who_am_i(event, client, message, say):
    say(f'hello! <@{event["user"]}>')
    
@app.message(":hello:")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click Me"},
                    "action_id": "button_click"
                }
            }
        ],
        text=f"Hey there <@{message['user']}>!"
    )

@app.action("button_click")
def action_button_click(body, ack, say):
    # Acknowledge the action
    ack()
    say(f"<@{body['user']['id']}> clicked the button")
    
@app.event("message")
def handle_message_event(message, say): 
    prompt = message['blocks'][0]['elements'][0]['elements'][0]['text']
    say(f"Yes! <@{message['user']}>! Your prompt : {prompt} :wave:")
    
    client = httpx.Client(timeout=None)
    response = client.post('http://127.0.0.1:8000/chat', params={'prompt': prompt})

    message = response.json()['message']['content']
    say(f"{message}")

''' 
@app.event("message")
def handle_message_events(body, logger, say):
    # logger.info(body)
    say(f"@{body}")
'''

async def main():
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    await asyncio.gather(handler.start())
    
if __name__ == "__main__":
    asyncio.run(main())
