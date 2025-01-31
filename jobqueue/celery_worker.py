import logging
from typing import Generator

from celery import Celery
from settings.settings import settings
from arena.playground import create_agent_run
from agents.example import get_example_agent

# Define the broker URL
broker_url = settings.redis_url
print(f"Celery Broker URL: {broker_url}")

celery_app = Celery("agent_tasks", broker=broker_url, backend=broker_url)

celery_app.conf.update(task_track_started=True)
celery_app.conf.broker_connection_retry_on_startup = True


@celery_app.task
def run_agent(
        agent_id: str,
        message: str,
        stream: bool = True,
        monitor: bool = False,
        session_id: str = None,
        user_id: str = None,
        images: list = None,
        audios: list = None
):
    """Run the agent asynchronously with given parameters."""
    logging.info(f"Running agent {agent_id} with message: {message}, stream: {stream}")

    # Get the example agent (Modify this if you have multiple agents)
    agents = [get_example_agent()]

    try:
        response = create_agent_run(
            agent_id=agent_id,
            agents=agents,
            message=message,
            stream=stream,
            monitor=monitor,
            session_id=session_id,
            user_id=user_id,
            images=images or [],
            audios=audios or []
        )

        # If the response is a generator (stream), convert it to a list before returning
        if isinstance(response, Generator):
            return list(response)

        return response.to_json()

    except Exception as e:
        logging.error(f"Error running agent {agent_id}: {str(e)}")
        return {"error": str(e)}
