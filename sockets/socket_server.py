import json

import socketio
from sockets.socket_playground import create_agent_run
from agents.example import get_example_agent
sio_server = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins=[], logger=True)

sio_app = socketio.ASGIApp(socketio_server=sio_server)


@sio_server.event
async def connect(sid, environ, auth):
    print("connected", sid)


@sio_server.event
async def run_agent(sid, data):
    # Parse incoming data
    try:
        data = json.loads(data)
    except json.JSONDecodeError:
        await sio_server.emit("run_agent", {"error": "Invalid JSON data"}, room=sid)
        return

    # Validate required parameters
    required_params = ["message", "agent_id"]
    missing_params = [param for param in required_params if not data.get(param)]
    if missing_params:
        await sio_server.emit(
            "run_agent", 
            {"error": f"Missing required parameters: {', '.join(missing_params)}"}, 
            room=sid
        )
        return

    # Get and validate parameters
    message = data["message"]
    stream = data.get("stream", False)
    if isinstance(stream, str):
        stream = stream.lower() == 'true'

    print(f"Running agent with message: {message}")
    print(f"Streaming: {stream}")
    
    response = create_agent_run(
        agent_id=data["agent_id"],
        agents=[get_example_agent()], 
        message=message,
        session_id=data.get("session_id"),  # Optional parameter
        stream=stream,
        user_id=data.get("user_id")
    )

    if stream:
        # Handle streaming case - emit chunks as they come
        for response_chunk in response:
            await sio_server.emit("run_agent", response_chunk, room=sid)
    else:
        # Handle non-streaming case - emit single response
        await sio_server.emit("run_agent", response.to_json(), room=sid)
