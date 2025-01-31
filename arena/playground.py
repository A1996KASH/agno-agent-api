from typing import Generator, List, Optional, cast
from agno.agent.agent import Agent, RunResponse
from agno.media import Image, Audio
from agno.playground.operator import get_agent_by_id
from agno.utils.log import logger


def chat_response_streamer(agent: Agent, message: str, images: Optional[List[Image]] = None,
                           audios: Optional[List[Audio]] = None) -> Generator:
    """
    Generates a streaming response from the agent.
    """
    run_response = agent.run(message=message, images=images, audios=audios, stream=True, stream_intermediate_steps=True)

    for run_response_chunk in run_response:
        run_response_chunk = cast(RunResponse, run_response_chunk)
        yield run_response_chunk.to_json()


def create_agent_run(
        agent_id: str,
        agents: List[Agent],
        message: str,
        stream: bool,
        monitor: bool = False,
        session_id: Optional[str] = None,
        user_id: Optional[str] = None,
        images: Optional[List[Image]] = None,
        audios: Optional[List[Audio]] = None,
):
    """
    Runs an agent with the given parameters.
    """
    logger.debug(
        f"AgentRunRequest: agent_id={agent_id}, stream={stream}, monitor={monitor}, session_id={session_id}, user_id={user_id}")
    # Fetch the agent by ID
    agent = get_agent_by_id(agent_id, agents)
    if agent is None:
        raise ValueError(f"Agent with ID {agent_id} not found")

    logger.debug(f"Session {'continuing' if session_id else 'creating new'}: {session_id}")

    # Create a new instance of this agent
    new_agent_instance = agent.deep_copy(update={"session_id": session_id})
    new_agent_instance.session_name = None

    if user_id is not None:
        new_agent_instance.user_id = user_id

    new_agent_instance.monitoring = monitor

    if stream:
        return chat_response_streamer(new_agent_instance, message, images=images, audios=audios)

    else:
        run_response = cast(
            RunResponse,
            new_agent_instance.run(
                message=message,
                images=images or None,
                audios=audios or None,
                stream=False,
            ),
        )
        return run_response
