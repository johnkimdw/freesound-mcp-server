# Freesound MCP Server

A Model Context Protocol (MCP) server that integrates with [Freesound.org](https://freesound.org), enabling AI agents to search and discover audio content for video editing and content creation workflows.

## Features

The Freesound MCP Server enables AI assistants to:

- **Search Audio Content**: Find sound effects, ambient sounds, and music loops using natural language queries
- **Access Metadata**: Get detailed information about audio files including duration, tags, licensing, and descriptions
- **Preview Content**: Access preview URLs for immediate audio playback evaluation
- **License Compliance**: Retrieve licensing information to ensure proper attribution and usage rights

## Installation

### Prerequisites

You will need to obtain a Freesound API key:

1. Create an account at [Freesound.org](https://freesound.org)
2. Apply for an API key at [https://freesound.org/api/apply/](https://freesound.org/api/apply/)
3. Once approved, note your API key for configuration

### Docker Installation (Recommended)

The easiest way to run the Freesound MCP Server is using Docker. No local Python installation required.

Afterwards, build your docker image.
```
cd /path/to/freesound-mcp-server
docker build -t freesound-mcp .  
```

#### Claude Desktop

Add the following configuration to your Claude Desktop config file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "freesound": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "FREESOUND_API_KEY",
        "freesound-mcp"
      ],
      "env": {
        "FREESOUND_API_KEY": "<YOUR_FREESOUND_API_KEY>"
      }
    }
  }
}
```

### Local Installation

If you prefer not to use Docker, you can install and run the server locally using Python and uv.

#### Requirements

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) package manager

#### Setup

1. Clone the repository:
```bash
git clone https://github.com/johnkimdw/freesound-mcp-server.git
cd freesound-mcp-server
```

2. Install dependencies:
```bash
uv sync
```

3. Set your API key:
```bash
export FREESOUND_API_KEY=your_api_key_here
```

#### Claude Desktop Configuration

```json
{
  "mcpServers": {
    "freesound": {
      "command": "/path/to/uv",
      "args": [
        "--directory",
        "/path/to/freesound-mcp-server",
        "run",
        "freesound-mcp"
      ],
      "env": {
        "FREESOUND_API_KEY": "<YOUR_FREESOUND_API_KEY>"
      }
    }
  }
}
```

## Usage

Once configured, you can interact with the Freesound MCP Server through your AI assistant. Here are some example queries:

- "Find thunder sound effects for a storm scene"
- "Search for ambient city sounds under 30 seconds"
- "Look for piano music loops with Creative Commons licensing"
- "Find dog barking sound effects"
- "Search for ocean waves background audio"

## Available Tools

### search_sounds

Search for audio files on Freesound.org using natural language queries.

**Parameters:**
- `query` (string, required): Search terms for audio content
- `max_results` (integer, optional): Number of results to return (1-30, default: 10)

**Returns:**
- Audio file metadata including:
  - File name and description
  - Duration and file format
  - Tags and categories
  - License information
  - Preview URLs (high and low quality)
  - Uploader information
  - Direct links to Freesound.org pages

## Transport Options

The server supports multiple transport methods for different deployment scenarios:

### Stdio Transport (Default)
Used for local integration with Claude Desktop and other MCP clients:
```bash
uv run freesound-mcp
# python -m freesound_mcp.server --transport stdio
```
<!-- 
### HTTP Transport
For web integration or custom deployments:
```bash
python -m freesound_mcp.server --transport http --port 8000
```

### Streamable HTTP Transport
For advanced streaming scenarios:
```bash
python -m freesound_mcp.server --transport streamable-http --port 8000
``` -->

## Development

### Building from Source

```bash
# Clone the repository
git clone https://github.com/yourname/freesound-mcp-server.git
cd freesound-mcp-server

# Install dependencies
uv sync

# Run tests
uv run pytest

# Build Docker image
docker build -t freesound-mcp .
```

### Testing

Use the MCP Inspector for detailed debugging:

```bash
npx @modelcontextprotocol/inspector uv run freesound-mcp
```

## Licensing and Attribution

This MCP server respects Freesound.org's terms of service and API usage guidelines. All audio content retrieved through this server:

- Originates from Freesound.org and is subject to their licensing terms
- Requires proper attribution as specified by individual file licenses
- Should be used in compliance with Creative Commons and other applicable licenses

**Important**: Always review the licensing information provided with each audio file to ensure compliance with attribution requirements and usage restrictions.

## Error Handling

The server includes comprehensive error handling for common scenarios:

- **Invalid API Key**: Clear error messages when authentication fails
- **Rate Limiting**: Automatic handling of API rate limits with appropriate error responses
- **Network Issues**: Timeout handling and connection error management
- **Invalid Queries**: Input validation and sanitization

## Configuration

### Environment Variables

- `FREESOUND_API_KEY` (required): Your Freesound.org API key

### Advanced Configuration

For advanced users, additional configuration options are available through command-line arguments:

```bash
python -m freesound_mcp.server --help
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

The audio content accessed through this server is provided by Freesound.org and is subject to individual Creative Commons and other open licenses as specified by content creators.