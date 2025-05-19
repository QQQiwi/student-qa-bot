import httpx
from pydantic import BaseModel
from typing import Optional
from fastapi import FastAPI, HTTPException


from config import LLM_SERVER_URL

app = FastAPI()

class LLMRequest(BaseModel):
    prompt: str

class LLMResponse(BaseModel):
    response: str

async def ask_llm(prompt: str) -> Optional[str]:
    try:
        async with httpx.AsyncClient() as client:
            req = LLMRequest(prompt=prompt)
            res = await client.post(LLM_SERVER_URL, json=req.dict())
            res.raise_for_status()
            data = LLMResponse(**res.json())
            return data.response
    except Exception as e:
        print(f"Ошибка подключения к ЛЛМ: {e}")
        return None

@app.post("/ask_llm/", response_model=LLMResponse)
async def ask_llm_endpoint(request: LLMRequest):
    response = await ask_llm(request.prompt)
    if response is None:
        raise HTTPException(status_code=500, detail="Произошла ошибка при обращении к модели.")
    return LLMResponse(response=response)