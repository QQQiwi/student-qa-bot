import json

from fastapi import FastAPI
from pydantic import BaseModel
import requests

from config import MODELNAME, MODEL_URL


app = FastAPI()


class BotRequestChat(BaseModel):
    user_id: int
    messages: list

class BotRequestPrompt(BaseModel):
    user_id: int
    prompt: str

class BotResponseChat(BaseModel):
    message: dict
    done: bool

class BotResponsePrompt(BaseModel):
    response: str
    done: bool

@app.post("/request_chat", response_model=BotResponseChat)
async def request_chat(request: BotRequestChat):
    request_data = {"model": f"{MODELNAME}",
                    "messages": request.messages,
                    "stream": False}
    answer = requests.post(f"{MODEL_URL + '/api/chat'}", data=json.dumps(request_data))
    return answer.json()

@app.post("/request_prompt", response_model=BotResponsePrompt)
async def request_prompt(request: BotRequestPrompt):
    request_data = {"model": f"{MODELNAME}",
                    "prompt": request.prompt,
                    "stream": False}
    answer = requests.post(f"{MODEL_URL + '/api/generate'}", data=json.dumps(request_data))
    return answer.json()

