
from fastapi import FastAPI

from app.api.v1.routes import (
    exports_router,
    health_router,
    imports_router,
    privacy_router,
    rewind_router,
    timeline_router,
)
from app.settings import settings

print(">>> app.main module executing <<<")
def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME)

    app.include_router(health_router, prefix="/api/v1")
    app.include_router(privacy_router, prefix="/api/v1")
    app.include_router(imports_router, prefix="/api/v1")
    app.include_router(exports_router, prefix="/api/v1")
    app.include_router(timeline_router, prefix="/api/v1")
    app.include_router(rewind_router, prefix="/api/v1")

    return app
app = create_app()
print(">>> app.main module finished <<<")
