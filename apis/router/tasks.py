from fastapi import APIRouter
from jobqueue.celery_worker import run_agent
import time

task_router = APIRouter()


@task_router.post('/tasks')
def agent_run(agent_id: str, message: str, stream: bool = True, monitor: bool = False, session_id: str = None, user_id: str = None):
    task = run_agent.delay(agent_id, message, stream, monitor, session_id, user_id)
    return {
        "status": "success",
        "task_id": task.id,
        "utc": time.time()
    }


@task_router.get('/tasks/{task_id}')
def get_task_result(task_id: str):
    task = run_agent.AsyncResult(task_id)
    return {
        "status": "success",
        "task_id": task.id,
        "result": task.result,
        "state": task.state,
        "utc": time.time()
    }
