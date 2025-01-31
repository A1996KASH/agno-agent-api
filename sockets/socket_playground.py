from typing import Generator, List, Optional, cast
from agno.agent.agent import Agent, RunResponse
from agno.media import Image
from agno.playground.operator import get_agent_by_id
from agno.utils.log import logger
from fastapi import Form


def chat_response_streamer(agent: Agent, message: str, images: Optional[List[Image]] = None) -> Generator:
    run_response = agent.run(message=message, images=images, stream=True, stream_intermediate_steps=True)
    for run_response_chunk in run_response:
        run_response_chunk = cast(RunResponse, run_response_chunk)
        yield run_response_chunk.to_json()


def create_agent_run(
        agent_id: str,
        agents: List[Agent],
        message: str = Form(...),
        stream: bool = Form(True),
        monitor: bool = Form(False),
        session_id: Optional[str] = Form(None),
        user_id: Optional[str] = Form(None),
):
    logger.debug(f"AgentRunRequest: {message} {agent_id} {stream} {monitor} {session_id} {user_id}")
    agent = get_agent_by_id(agent_id, agents)
    if agent is None:
        raise Exception(f"Agent with id {agent_id} not found")
    if session_id is not None:
        logger.debug(f"Continuing session: {session_id}")
    else:
        logger.debug("Creating new session")

    # Create a new instance of this agent
    new_agent_instance = agent.deep_copy(update={"session_id": session_id})
    new_agent_instance.session_name = None

    if user_id is not None:
        new_agent_instance.user_id = user_id

    if monitor:
        new_agent_instance.monitoring = True
    else:
        new_agent_instance.monitoring = False

    base64_image: Optional[Image] = None
    if stream:
        return chat_response_streamer(new_agent_instance, message, images=[base64_image] if base64_image else None)

    else:
        run_response = cast(
            RunResponse,
            new_agent_instance.run(
                message,
                images=[base64_image] if base64_image else None,
                stream=False,
            ),
        )
        return run_response

