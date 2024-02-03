from fastapi import FastAPI, APIRouter

# routes
from api.v1.calendar import router as events_router


def register_routes(app: FastAPI) -> FastAPI:
    # API ROUTER
    api_router = APIRouter(prefix='/api', tags=['api'])
    # V1
    v1_router = APIRouter(prefix='/v1', tags=['v1'])
    v1_router.include_router(events_router)

    # Build Routes
    api_router.include_router(v1_router)
    app.include_router(api_router)

    return app
