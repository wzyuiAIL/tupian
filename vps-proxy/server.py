import asyncio
import os
import time
import uuid
from typing import Any, Iterable

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
REQUEST_TIMEOUT_SECONDS = float(os.environ.get("REQUEST_TIMEOUT_SECONDS", "900"))
JOB_TTL_SECONDS = float(os.environ.get("JOB_TTL_SECONDS", "3600"))

JOBS: dict[str, dict[str, Any]] = {}
JOBS_LOCK = asyncio.Lock()


def parse_origins(value: str) -> Iterable[str]:
    return [origin.strip() for origin in value.split(",") if origin.strip()]


def now() -> float:
    return time.time()


def public_job(job: dict[str, Any]) -> dict[str, Any]:
    started_at = job.get("started_at")
    finished_at = job.get("finished_at")
    elapsed_until = finished_at or now()
    elapsed = round(elapsed_until - started_at, 1) if started_at else 0
    return {
        "job_id": job["job_id"],
        "status": job["status"],
        "stage": job["stage"],
        "message": job["message"],
        "percent": job["percent"],
        "elapsed_seconds": elapsed,
        "request_bytes": job.get("request_bytes", 0),
        "upstream_status": job.get("upstream_status"),
        "upstream_bytes": job.get("upstream_bytes", 0),
        "result": job.get("result"),
        "error": job.get("error"),
    }


async def update_job(job_id: str, **updates: Any) -> None:
    async with JOBS_LOCK:
        job = JOBS.get(job_id)
        if job:
            job.update(updates)


async def cleanup_jobs() -> None:
    cutoff = now() - JOB_TTL_SECONDS
    async with JOBS_LOCK:
        expired = [
            job_id
            for job_id, job in JOBS.items()
            if job.get("finished_at") and job["finished_at"] < cutoff
        ]
        for job_id in expired:
            JOBS.pop(job_id, None)


async def call_coze(job_id: str, payload: dict[str, Any]) -> None:
    if not COZE_TOKEN:
        await update_job(
            job_id,
            status="failed",
            stage="configuration",
            message="VPS 未配置 COZE_TOKEN",
            percent=100,
            error={"detail": "COZE_TOKEN is not configured"},
            finished_at=now(),
        )
        return

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {COZE_TOKEN}",
    }
    timeout = httpx.Timeout(
        REQUEST_TIMEOUT_SECONDS,
        connect=60,
        read=REQUEST_TIMEOUT_SECONDS,
        write=120,
    )

    await update_job(
        job_id,
        status="running",
        stage="forwarding",
        message="VPS 已收到图片，正在转发给 Coze 工作流",
        percent=55,
    )

    try:
        await update_job(
            job_id,
            stage="coze_running",
            message="Coze 工作流正在生成图片，请保持页面打开",
            percent=65,
        )
        async with httpx.AsyncClient(timeout=timeout, trust_env=False) as client:
            response = await client.post(COZE_API_URL, json=payload, headers=headers)

        content_type = response.headers.get("content-type", "")
        if "application/json" in content_type:
            result: Any = response.json()
        else:
            result = {"status": response.status_code, "message": response.text}

        if response.status_code >= 400:
            await update_job(
                job_id,
                status="failed",
                stage="coze_failed",
                message=f"Coze 返回错误：HTTP {response.status_code}",
                percent=100,
                upstream_status=response.status_code,
                upstream_bytes=len(response.content),
                error=result,
                finished_at=now(),
            )
            print(
                f"[job {job_id}] coze failed status={response.status_code} bytes={len(response.content)}",
                flush=True,
            )
            return

        await update_job(
            job_id,
            status="succeeded",
            stage="done",
            message="图片生成完成",
            percent=100,
            upstream_status=response.status_code,
            upstream_bytes=len(response.content),
            result=result,
            finished_at=now(),
        )
        print(
            f"[job {job_id}] coze success status={response.status_code} bytes={len(response.content)}",
            flush=True,
        )

    except httpx.TimeoutException as exc:
        await update_job(
            job_id,
            status="failed",
            stage="timeout",
            message="Coze 生成超时，建议缩小图片或稍后重试",
            percent=100,
            error={"type": type(exc).__name__, "detail": repr(exc)},
            finished_at=now(),
        )
        print(f"[job {job_id}] timeout: {type(exc).__name__}: {exc!r}", flush=True)
    except httpx.HTTPError as exc:
        await update_job(
            job_id,
            status="failed",
            stage="network_error",
            message="VPS 连接 Coze 失败",
            percent=100,
            error={"type": type(exc).__name__, "detail": repr(exc)},
            finished_at=now(),
        )
        print(f"[job {job_id}] http error: {type(exc).__name__}: {exc!r}", flush=True)
    except Exception as exc:
        await update_job(
            job_id,
            status="failed",
            stage="proxy_error",
            message="VPS 代理处理失败",
            percent=100,
            error={"type": type(exc).__name__, "detail": repr(exc)},
            finished_at=now(),
        )
        print(f"[job {job_id}] proxy error: {type(exc).__name__}: {exc!r}", flush=True)


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
    return {"status": "ok", "jobs": str(len(JOBS))}


@app.post("/coze/jobs")
async def create_job(request: Request):
    await cleanup_jobs()
    raw_body = await request.body()
    print(f"[jobs] incoming bytes={len(raw_body)}", flush=True)

    try:
        payload = await request.json()
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid JSON: {type(exc).__name__}: {exc!r}",
        ) from exc

    job_id = uuid.uuid4().hex
    job = {
        "job_id": job_id,
        "status": "queued",
        "stage": "queued",
        "message": "VPS 已创建任务，准备转发给 Coze",
        "percent": 50,
        "request_bytes": len(raw_body),
        "started_at": now(),
        "finished_at": None,
        "result": None,
        "error": None,
    }
    async with JOBS_LOCK:
        JOBS[job_id] = job

    asyncio.create_task(call_coze(job_id, payload))
    return public_job(job)


@app.get("/coze/jobs/{job_id}")
async def get_job(job_id: str):
    async with JOBS_LOCK:
        job = JOBS.get(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found or expired")
        return public_job(job)


@app.post("/coze/run")
async def run_coze_legacy(request: Request):
    created = await create_job(request)
    job_id = created["job_id"]
    deadline = now() + REQUEST_TIMEOUT_SECONDS + 30

    while now() < deadline:
        async with JOBS_LOCK:
            job = JOBS[job_id]
            if job["status"] in {"succeeded", "failed"}:
                snapshot = public_job(job)
                if job["status"] == "succeeded":
                    return JSONResponse(status_code=200, content=job["result"])
                return JSONResponse(status_code=job.get("upstream_status") or 502, content=snapshot)
        await asyncio.sleep(1)

    return JSONResponse(
        status_code=504,
        content={"job_id": job_id, "message": "Request timed out while waiting for job"},
    )
