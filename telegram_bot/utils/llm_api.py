import httpx
from pydantic import BaseModel
from typing import Optional
from fastapi import FastAPI, HTTPException
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from config import LLM_SERVER_URL

app = FastAPI()

class LLMRequest(BaseModel):
    prompt: str

class LLMResponse(BaseModel):
    response: str

async def ask_llm(prompt: str) -> Optional[str]:
    logger.info(f"ask_llm: отправка запроса с prompt: {prompt[:50]}...")
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            req = LLMRequest(prompt=prompt)
            res = await client.post(f"{LLM_SERVER_URL}/api/generate", json={
                "model": "llama3",
                "prompt": req.prompt,
                "stream": False
            })
            res.raise_for_status()
            data = LLMResponse(**res.json())
            logger.info(f"ask_llm: получен ответ от LLM, длина ответа: {len(data.get('response', ''))}")
            return data.response
    except Exception as e:
        print(f"Ошибка подключения к LLM: {e}")
        return None

@app.post("/ask_llm/", response_model=LLMResponse)
async def ask_llm_endpoint(request: LLMRequest):
    response = await ask_llm(request.prompt)
    if response is None:
        raise HTTPException(status_code=500, detail="Произошла ошибка при обращении к модели.")
    return LLMResponse(response=response)