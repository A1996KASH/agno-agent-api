# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Expose the port the app runs on
EXPOSE 8000

# Command to run the FastAPI application using the FastAPI CLI -> no workers flag as Kubernetes handles replication
CMD ["fastapi", "run", "main.py","--host", "0.0.0.0", "--port", "8000", "--workers", "2"]

