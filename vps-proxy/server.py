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
    "https://wzyuiail.github.io,https://wzyui.github.io,https://wzyuail.github.io,https://wzyuial.github.io,http://localhost:8100,http://127.0.0.1:8100",
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

    raw_body = await request.body()
    print(f"[proxy] incoming bytes={len(raw_body)}", flush=True)

    try:
        payload = await request.json()
    except Exception as exc:
        print(f"[proxy] invalid json: {type(exc).__name__}: {exc!r}", flush=True)
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {type(exc).__name__}: {exc!r}") from exc

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {COZE_TOKEN}",
    }
    timeout = httpx.Timeout(REQUEST_TIMEOUT_SECONDS, connect=60, read=REQUEST_TIMEOUT_SECONDS, write=120)

    try:
        async with httpx.AsyncClient(timeout=timeout, trust_env=False) as client:
            response = await client.post(COZE_API_URL, json=payload, headers=headers)
    except httpx.TimeoutException as exc:
        print(f"[proxy] timeout: {type(exc).__name__}: {exc!r}", flush=True)
        raise HTTPException(status_code=504, detail=f"Coze request timed out: {type(exc).__name__}: {exc!r}") from exc
    except httpx.HTTPError as exc:
        print(f"[proxy] http error: {type(exc).__name__}: {exc!r}", flush=True)
        raise HTTPException(status_code=502, detail=f"Coze request failed: {type(exc).__name__}: {exc!r}") from exc

    print(f"[proxy] coze status={response.status_code} bytes={len(response.content)}", flush=True)
    content_type = response.headers.get("content-type", "")
    if "application/json" in content_type:
        return JSONResponse(status_code=response.status_code, content=response.json())

    return JSONResponse(
        status_code=response.status_code,
        content={"status": response.status_code, "message": response.text},
    )
