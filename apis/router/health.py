from fastapi import APIRouter
import time

health_router = APIRouter()


@health_router.get('/health')
def get_health():
    """
    CHECK HEALTH OF THE API
    """
    return {
        "status": "success",
        "router": "health",
        "path": "/health",
        "utc": time.time()
    }
