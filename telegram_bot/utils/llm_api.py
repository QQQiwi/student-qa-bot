import httpx
from pydantic import BaseModel
from typing import Optional

from telegram_bot.config import LLM_SERVER_URL

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
        print(f"Ошибка подключени к ЛЛМ: {e}")
        return "Произошла ошибка при обращении к модели."
