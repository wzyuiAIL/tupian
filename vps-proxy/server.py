import os
from typing import Iterable

import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


COZE_API_URL = os.environ.get("COZE_API_URL", "https://px5r5j8mt8.coze.site/run")
COZE_TOKEN = os.environ.get("COZE_TOKEN", "")
ALLOWED_ORIGINS = os.environ.get(
    "ALLOWED_ORIGINS",
    "https://wzyuial.github.io,http://localhost:8100,http://127.0.0.1:8100",
)
REQUEST_TIMEOUT_SECONDS = float(os.environ.get("REQUEST_TIMEOUT_SECONDS", "600"))


def parse_origins(value: str) -> Iterable[str]:
    return [origin.strip() for origin in value.split(",") if origin.strip()]


app = FastAPI(title="tupian Coze Proxy")

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(parse_origins(ALLOWED_ORIGINS)),
    allow_credentials=False,
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/coze/run")
async def run_coze(request: Request):
    if not COZE_TOKEN:
        raise HTTPException(status_code=500, detail="COZE_TOKEN is not configured")

    payload = await request.json()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {COZE_TOKEN}",
    }

    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT_SECONDS) as client:
            response = await client.post(COZE_API_URL, json=payload, headers=headers)
    except httpx.TimeoutException as exc:
        raise HTTPException(status_code=504, detail="Coze request timed out") from exc
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Coze request failed: {exc}") from exc

    content_type = response.headers.get("content-type", "")
    if "application/json" in content_type:
        return JSONResponse(status_code=response.status_code, content=response.json())

    return JSONResponse(
        status_code=response.status_code,
        content={"status": response.status_code, "message": response.text},
    )
