# app/routers/llm.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests

router = APIRouter(tags=["llm"])

class LLMRequest(BaseModel):
    prompt: str = None
    messages: list = None

@router.post("/")
def query_llm(data: LLMRequest):
    if not data.prompt and not data.messages:
        raise HTTPException(status_code=400, detail="No prompt or messages provided")

    # Build messages array
    if data.messages:
        messages = data.messages
    else:
        messages = [{"role": "user", "content": data.prompt}]

    api_url = ""  # Your real LLM endpoint
    headers = {
        "Content-Type": "application/json",
        "api-key": ""
    }
    payload = {
        "messages": messages,
        "max_completion_tokens": 5000,  # Or whatever you need
        "reasoning_effort": "high"
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"LLM request failed: {str(e)}")
