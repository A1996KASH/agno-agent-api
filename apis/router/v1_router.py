from fastapi import APIRouter
from apis.router.health import health_router
from apis.router.playground import playground_router
from apis.router.tasks import task_router
v1_router = APIRouter(prefix='/v1')

v1_router.include_router(health_router)
v1_router.include_router(playground_router)
v1_router.include_router(task_router)
