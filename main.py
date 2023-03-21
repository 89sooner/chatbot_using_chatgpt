import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.docs import get_redoc_html
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import uvicorn

import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI"
    )

@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc"
    )

@app.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint():
    return app.openapi()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/items/{item_id}", response_class=HTMLResponse)
async def read_item(request: Request, item_id: str):
    return templates.TemplateResponse("item.html", {"request": request, "item_id": item_id})

@app.post("/chat")
async def chat(prompt: str):
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    max_tokens=1024,
    # stop=None,
    # temperature=0.5,
    messages=[
        {"role": "user", "content": prompt}
    ]
    )
    message = completion.choices[0].message
    return {"message": message}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    

