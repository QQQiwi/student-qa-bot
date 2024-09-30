import json

from fastapi import FastAPI
from pydantic import BaseModel
import requests

from config import MODELNAME, MODEL_URL


app = FastAPI()


class BotRequest(BaseModel):
    user_id: int
    messages: list


@app.post("/request")
async def request(request: BotRequest):
    request_data = {"model": f"{MODELNAME}",
                    "messages": request.messages,
                    "stream": False}
    answer = requests.post(f"{MODEL_URL}", data=json.dumps(request_data))
    return answer.json()


