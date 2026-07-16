FROM public.ecr.aws/docker/library/python:3.13-slim-bookworm@sha256:01f42367a0a94ad4bc17111776fd66e3500c1d87c15bbd6055b7371d39c124fb

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install explicit requirements for the framework and testing
RUN pip install --no-cache-dir \
    pytest==8.1.1 \
    pyyaml==6.0.1

# Setup project directory structure
RUN mkdir -p /app/project /app/project/logs

# Copy core codebase files (excluding solution/tests fields)
COPY project/ /app/project/

# Give appropriate workspace execution permissions
RUN chmod -R 755 /app/project