import json
import socketio
from arena.playground import create_agent_run
from agents.example import get_example_agent

# Initialize Socket.IO server
sio_server = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=[], logger=True)
sio_app = socketio.ASGIApp(socketio_server=sio_server)


@sio_server.event
async def connect(sid, environ, auth):
    """Handles new client connections."""
    print(f"Client connected: {sid}")


@sio_server.event
async def run_agent(sid, data):
    """
    Handles the `run_agent` event, validating input and streaming responses.
    """
    try:
        # Parse incoming JSON data
        data = json.loads(data)
    except json.JSONDecodeError:
        await sio_server.emit("run_agent", {"error": "Invalid JSON format"}, room=sid)
        return

    # Validate required parameters
    required_params = ["message", "agent_id"]
    missing_params = [param for param in required_params if not data.get(param)]
    if missing_params:
        await sio_server.emit(
            "run_agent",
            {"error": f"Missing required parameters: {', '.join(missing_params)}"},
            room=sid,
        )
        return

    # Extract parameters
    message = data["message"]
    agent_id = data["agent_id"]
    stream = str(data.get("stream", "false")).lower() == "true"  # Convert string "true"/"false" to boolean
    session_id = data.get("session_id")
    user_id = data.get("user_id")

    print(f"Running agent (ID: {agent_id}) with message: {message}, stream: {stream}")

    try:
        # Get agent instance
        agents = [get_example_agent()]
        response = create_agent_run(
            agent_id=agent_id,
            agents=agents,
            message=message,
            stream=stream,
            session_id=session_id,
            user_id=user_id
        )

        if stream:
            # Handle streaming case - emit responses as they come
            for response_chunk in response:
                await sio_server.emit("run_agent", response_chunk, room=sid)
        else:
            # Handle non-streaming case - emit a single response
            await sio_server.emit("run_agent", response.to_json(), room=sid)

    except Exception as e:
        error_message = f"Error running agent: {str(e)}"
        print(error_message)
        sio_server.emit("run_agent", {"error": error_message}, room=sid)
