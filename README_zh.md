# Mem0 MCP 服务端设置（中文版）

这是一个 Mem0 的本地 MCP 服务端，可让您直接在 Cursor 中存储和搜索记忆。

## 先决条件

- Python 3.10+
- Mem0 API 密钥（在 [https://app.mem0.ai/](https://app.mem0.ai/) 获取）

## 安装

1. **安装依赖**：
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
   # 或 Windows: venv\\Scripts\\activate
   pip install -r requirements.txt
   ```

2. **配置 API 密钥**：
   🚀 **推荐方式**：直接在 `mcp.json` 的 `env` 部分设置 `MEM0_API_KEY`（**无需创建 .env 文件**，见下文 Cursor 配置）。

   **或使用 .env 文件**：
   - 复制 `.env.example` 为 `.env`：
     ```bash
     cp .env.example .env
     ```
   - 编辑 `.env`，将 `your_mem0_api_key_here` 替换为您的真实 Mem0 API 密钥。

**注意**：
- 🚀 **首选**：在 `mcp.json` 的 `env` 部分直接设置 `MEM0_API_KEY` - FastMCP 会自动传递到 server.py 进程。
- **备选**：使用 `.env` 文件（通过 `python-dotenv` 加载）。确保从包含 `.env` 的目录运行服务器。
- 确保 `command` 指向安装了依赖的 Python 环境（例如使用 venv 时指向 `venv/bin/python`）。

## Cursor 配置（`mcp.json`）

在您的 Cursor `mcp.json` 文件中添加以下条目（通常位于 `~/.cursor/mcp.json`，或通过 Cursor 设置 > MCP 访问）：

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

**注意**：
- 您可以选择在 `mcp.json` 的 `env` 部分设置 `MEM0_API_KEY`，**或**使用 `.env` 文件。如果使用 `.env`，确保从包含该文件的目录运行服务器（脚本通过 `python-dotenv` 自动加载）。
- 确保 `command` 指向安装了依赖的 Python 环境（例如使用 venv 时指向 `venv/bin/python`）。

## 提供的工具

1. **`add_memory`**：将交互内容（消息）存储到记忆系统中。用于持久化信息、用户偏好或对话上下文，便于后续检索。

   **重要提示**：为获得最佳效果，请传入**最近对话历史**（用户和助手消息），而非单一消息。这有助于系统推断上下文并提取准确记忆。

   **参数**：
   - `messages`：必需。消息对象列表，包含 `'role'` 和 `'content'`。
     示例：
     ```python
     [
       {'role': 'user', 'content': '我只写 Python 代码。'},
       {'role': 'assistant', 'content': '明白了，我会专注 Python。'}
     ]
     ```
   - `user_id`：用户 ID，默认 `'default_user'`。
   - `agent_id`：代理/助手 ID，默认 `'assistant'`。
   - `app_id`、`run_id`、`metadata` 等可选参数，用于额外上下文。
   - `infer`：是否自动提取关键事实，默认 `True`。
   - `async_mode`：异步添加，默认 `True`。
   - 其他高级参数：`custom_categories`、`custom_instructions`、`includes`、`excludes`、`immutable`、`timestamp`、`expiration_date`、`org_id`、`project_id`、`output_format`（默认 `'v1.1'`）、`version`（默认 `'v2'`）。

2. **`search_memories`**：基于查询的语义相似度检索相关记忆。用于回忆过去信息、上下文或偏好。

   **参数**：
   - `query`：必需。搜索文本或问题。
   - `filters`：必需。过滤字典（如按 `user_id`、`agent_id`、时间或 `metadata` 缩小范围）。
   - `top_k`：返回最大记忆项数，默认 `10`。
   - `fields`：指定输出字段。
   - `rerank`：启用重排序，默认 `False`。
   - `keyword_search`：启用精确关键词匹配，默认 `False`。
   - `filter_memories`：预过滤记忆，默认 `False`。
   - `threshold`：相似度阈值（0.0-1.0），默认 `0.3`。
   - `org_id`、`project_id`、`version`（默认 `'v2'`）。

## 注意事项

- **安全性**：`.env` 已加入 `.gitignore`，不会上传到 GitHub。mcp.json 中的密钥仅本地使用。
- **启动测试**：重启 Cursor，MCP 应自动发现 “mem0”。在聊天中调用工具测试。
- **调试**：若无 API 密钥，server.py 会打印警告，但 mcp.json env 可覆盖。
- **英文版**：查看 [README.md](README.md) 获取英文文档。

## 贡献与问题

欢迎 PR 或 issue！项目路径：`/Users/alexnear/Documents/mem0MCP/`
