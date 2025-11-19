# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Setup
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r mcp_simple_slackbot/requirements.txt
```

### Running the Bot

#### Local Development
```bash
cd mcp_simple_slackbot
python main.py
```

#### Docker
```bash
# Copy environment file and configure
cp .env.example .env
# Edit .env with your API keys

# Build and run with docker-compose
docker-compose up --build

# Or run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the bot
docker-compose down
```

### Code Quality
```bash
# Type checking
pyright

# Linting and formatting
ruff check
ruff format

# Run tests
pytest
```

## Architecture

This is a Slack bot that integrates with the Model Context Protocol (MCP) to provide AI assistance with external tool capabilities.

### Core Components

1. **MCPBotHub** (`main.py`): Central orchestrator that initializes and manages all components
2. **Configuration** (`config.py`): Handles environment variables and JSON config loading with placeholder substitution
3. **MCPManager** (`mcp_manager.py`): Manages connections to multiple MCP servers and their tools
4. **LLMClient** (`llm.py`): Handles communication with OpenAI API (configurable base URL)
5. **SlackBot** (`slack_manager.py`): Manages Slack Socket Mode connection and message handling

### Data Flow

1. Slack message received → SlackBot
2. SlackBot sends message + available tools → LLMClient
3. If LLM requests tool use → MCPManager executes tool via appropriate MCP server
4. Tool results returned to LLM for interpretation
5. Final response sent back to Slack

### Configuration

- Environment variables loaded from `.env` file in `mcp_simple_slackbot/` directory
- MCP servers configured in `servers_config.json` with environment variable substitution using `${VAR_NAME}` syntax
- Supports multiple LLM providers via configurable `OPENAI_BASE_URL`
- Optional Azure OpenAI integration for video generation (Sora)

### MCP Server Integration

The bot connects to multiple MCP servers defined in `servers_config.json`:
- SQLite database server for data persistence
- Web fetch server for retrieving web content
- Sequential thinking server for enhanced reasoning
- Google Maps server (requires API key)

Each server runs as a separate process and communicates via the MCP protocol.