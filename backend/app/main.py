from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.routes import router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Medical Symptom QR AI API",
        version="0.4.0",
        description="MVP triage support API. Not a medical diagnosis system.",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router, prefix="/api")
    return app


app = create_app()
