"""Career Hub FastAPI application entrypoint.

Phase 1 code foundation only: a home page, a health endpoint, and placeholder
private/public route groups. See docs/architecture.md and docs/phase-plan.md
for what later phases add on top of this.
"""
from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import settings
from app.db import init_db
from app.routers import private, public


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Career Hub", lifespan=lifespan)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


app.include_router(public.router)
app.include_router(private.router)


def run() -> None:
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.bind_host,
        port=settings.http_port,
        reload=False,
    )


if __name__ == "__main__":
    run()
