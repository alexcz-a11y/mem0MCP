🇨🇳 [中文文档](README_zh.md)

# Mem0 MCP Server Setup

This is a local MCP server for Mem0, allowing you to store and search memories directly from Cursor.

## Prerequisites

- Python 3.10+
- A Mem0 API Key (Get one at [https://app.mem0.ai/](https://app.mem0.ai/))

## Installation

1. **Install Dependencies**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure API Key**:
   🚀 **推荐方式**：直接在 `mcp.json` 的 `env` 部分设置 `MEM0_API_KEY`（无需创建 .env 文件，见下文 Cursor 配置）。

   **或使用 .env 文件**：
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Open `.env` and replace `your_mem0_api_key_here` with your actual Mem0 API Key.

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
- 🚀 **首选**：Set `MEM0_API_KEY` **directly in the `env` section of `mcp.json`** - FastMCP passes it to the server process automatically.
- **Alternative**: Use `.env` file (loaded via `python-dotenv`). Ensure server runs from the directory containing `.env`.
- Ensure the python command points to the python environment where you installed the requirements (e.g., if you used a venv, point to `venv/bin/python`).

## Tools Provided

1. **`add_memory`**: Stores messages/interactions.
2. **`search_memories`**: Semantically searches stored memories (v2).
