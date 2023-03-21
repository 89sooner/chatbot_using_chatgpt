from slack_sdk import WebClient
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

class SlackAPI:
    """
    슬랙 API 핸들러
    """
    def __init__(self, token):
        # 슬랙 클라이언트 인스턴스 생성
        self.client = WebClient(token)
        
    def get_channel_id(self, channel_name):
        """
        슬랙 채널ID 조회
        """
        result = self.client.conversations_list()
        channels = result.data['channels']
        channel = list(filter(lambda c: c["name"] == channel_name, channels))[0]
        channel_id = channel["id"]
        return channel_id

    def get_message_ts(self, channel_id, query):
        """
        슬랙 채널 내 메세지 조회
        """
        result = self.client.conversations_history(channel=channel_id)
        messages = result.data['messages']
        message = list(filter(lambda m: m["text"]==query, messages))[0]
        message_ts = message["ts"]
        return message_ts

    def post_thread_message(self, channel_id, message_ts, text):
        """
        슬랙 채널 내 메세지의 Thread에 댓글 달기
        """
        result = self.client.chat_postMessage(
            channel=channel_id,
            text = text,
            thread_ts = message_ts
        )
        return result

    def post_message(self, channel_id, text):
        """
        슬랙 채널에 메세지 보내기
        """
        result = self.client.chat_postMessage(
            channel=channel_id,
            text=text
        )
        return result
    

# if __name__ == "__main__":
#     slack = SlackAPI("&&&")

#     channel_name = "test_chat"
#     query = "hi"
#     text = "자동 생성 문구 테스트"

#     # 채널ID 파싱
#     channel_id = slack.get_channel_id(channel_name)
#     # 메세지ts 파싱
#     message_ts = slack.get_message_ts(channel_id, query)
#     # 댓글 달기
#     slack.post_thread_message(channel_id, message_ts, text)
    