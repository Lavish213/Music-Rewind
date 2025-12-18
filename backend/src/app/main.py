# LOCATION: backend/src/app/main.py
from __future__ import annotations

from fastapi import FastAPI

from app.settings import settings
from app.api.v1.routes.health import router as health_router
from app.api.v1.routes.privacy import router as privacy_router
from app.api.v1.routes.imports import router as imports_router
from app.api.v1.routes.exports import router as exports_router

# These may exist already in your folder structure.
# If any of these files are not created yet, comment them out until they are.
# from app.api.v1.routes.auth import router as auth_router
# from app.api.v1.routes.sessions import router as sessions_router
# from app.api.v1.routes.candidates import router as candidates_router
# from app.api.v1.routes.entitlements import router as entitlements_router


def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME)

    # Core routes
    app.include_router(health_router, prefix=settings.API_PREFIX)
    app.include_router(imports_router, prefix=settings.API_PREFIX)
    app.include_router(exports_router, prefix=settings.API_PREFIX)
    app.include_router(privacy_router, prefix=settings.API_PREFIX)

    # Optional routes (enable when the modules exist)
    # app.include_router(auth_router, prefix=settings.API_PREFIX)
    # app.include_router(sessions_router, prefix=settings.API_PREFIX)
    # app.include_router(candidates_router, prefix=settings.API_PREFIX)
    # app.include_router(entitlements_router, prefix=settings.API_PREFIX)

    return app


app = create_app()