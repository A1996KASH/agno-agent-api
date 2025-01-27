from fastapi import FastAPI
import os
import openlit
from fastapi.middleware.cors import CORSMiddleware
from apis.router.v1_router import v1_router
from settings.settings import settings


def create_app() -> FastAPI:
    """
    Create FastAPI app
    """

    app: FastAPI = FastAPI(
        title='Phidata API',
        docs_url=None if settings.environment == "production" else "/docs",
        redoc_url=None if settings.environment == "production" else "/redoc",
        openapi_url=None if settings.environment == "production" else "/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(v1_router)

    return app

"""
uncomment the below block to enable openlit
"""
# openlit.init(
#     otlp_endpoint="http://otel-collector:4318"
# )

app = create_app()
