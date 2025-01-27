# PHIDATA-AGENT-API

A FastAPI-based agent API service with modular architecture for handling various agent operations.

## Project Structure

```
PHIDATA-AGENT-API/
├── agents/
│   └── settings.py
├── apis/
│   ├── __pycache__/
│   └── router/
│       ├── __pycache__/
│       ├── __init__.py
│       ├── health.py
│       ├── playground.py
│       ├── v1_router.py
│       └── __init__.py
├── settings/
│   ├── __pycache__/
│   ├── __init__.py
│   └── settings.py
├── .env
├── .env.example
├── .gitignore
├── Dockerfile
├── main.py
├── README.md
└── requirements.txt
```

## Overview

This API service is structured with clear separation of concerns:
- `agents/`: Contains agent-specific settings and configurations
- `apis/`: Houses the API routing logic and endpoint definitions
- `settings/`: Manages application-wide configurations

## Key Components

### API Routes
- `health.py`: Health check endpoints
- `playground.py`: Development and testing endpoints
- `v1_router.py`: Version 1 API routes

### Configuration
- `.env`: Environment-specific configuration (not tracked in git)
- `.env.example`: Template for environment variables
- `settings.py`: Application settings management

## Setup and Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd PHIDATA-AGENT-API
```

2. Set up the environment:
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

3. Configure environment:
```bash
# Copy example environment file
cp .env.example .env
# Edit .env with your configuration
```

## Running the Application

### Local Development
```bash
fastapi dev main.py
```

The API will be available at `http://localhost:8000` by default.

### Docker
```bash
# Build the image
docker build -t phidata-agent-api .

# Run the container
docker run -p 8000:8000 phidata-agent-api
```

## API Documentation

Once the application is running, access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Development

### Project Organization
- Place new agent settings in `agents/settings.py`
- Add new API routes under `apis/router/`
- Configure application settings in `settings/settings.py`

### Best Practices
- Follow PEP 8 style guide
- Update requirements.txt when adding new dependencies
- Keep environment variables in .env (never commit sensitive data)
- Use appropriate HTTP methods for API endpoints

## Contributing

1. Ensure you have the latest code
2. Create a new branch for your feature
3. Write and test your code
4. Submit a pull request
