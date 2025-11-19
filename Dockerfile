FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install uvx for MCP server management
RUN pip install uv

# Set working directory
WORKDIR /app

# Copy the application code and metadata required for installation
COPY pyproject.toml ./
COPY README.md ./
COPY mcp_simple_slackbot/ ./mcp_simple_slackbot/

# Install Python dependencies
RUN pip install -e .

# Set the working directory to the app module
WORKDIR /app/mcp_simple_slackbot

# Run the bot
CMD ["python", "main.py"]
