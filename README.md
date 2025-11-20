# Mem0 MCP Server Setup

This is a local MCP server for Mem0, allowing you to store and search memories directly from Cursor.

## Prerequisites

- Python 3.10+
- A Mem0 API Key (Get one at [https://app.mem0.ai/](https://app.mem0.ai/))

## Installation

1.  **Install Dependencies**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2.  **Configure API Key**:
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Open `.env` and replace `your_mem0_api_key_here` with your actual Mem0 API Key.

   **Alternative**: Set `MEM0_API_KEY` directly in the `env` section of `mcp.json` (see below).

## Cursor Configuration (`mcp.json`)

Add the following entry to your Cursor `mcp.json` file (usually located at `~/.cursor/mcp.json` or accessible via Cursor Settings > MCP):

```json
{
  "mcpServers": {
    "mem0": {
      "command": "/Users/alexnear/Documents/mem0MCP/venv/bin/python",
      "args": [
        "/Users/alexnear/Documents/mem0MCP/server.py"
      ],
      "env": {
        "MEM0_API_KEY": "your_api_key_here" 
      }
    }
  }
}
```

**Note**: 
- You can either set `MEM0_API_KEY` in the `env` section of `mcp.json` OR use the `.env` file. If using the `.env` file, make sure you run the server from the directory containing the `.env` file, or the python script loads it correctly (which it does via `python-dotenv`).
- Ensure the python command points to the python environment where you installed the requirements (e.g., if you used a venv, point to `venv/bin/python`).

## Tools Provided

1.  **`add_memory`**: Stores messages/interactions.
2.  **`search_memories`**: Semantically searches stored memories (v2).

## 中文文档
See [README_zh.md](README_zh.md) for Chinese documentation.
