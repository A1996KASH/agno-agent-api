from os import getenv
from phi.playground import Playground
from agents.example import get_example_agent


example_agent = get_example_agent(debug_mode=True)
playground = Playground(agents=[example_agent])

playground_router = playground.get_router()
