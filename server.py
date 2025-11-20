import os
import httpx
import json
from typing import List, Dict, Optional, Any
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("mem0")

API_BASE_URL = "https://api.mem0.ai"
API_KEY = os.getenv("MEM0_API_KEY")

if not API_KEY:
    print("Warning: MEM0_API_KEY not found in environment variables.")

async def make_request(method: str, endpoint: str, data: Dict[str, Any] = None) -> Any:
    """Helper function to make HTTP requests to Mem0 API."""
    if not API_KEY:
        raise ValueError("MEM0_API_KEY is not set. Please check your .env file.")

    headers = {
        "Authorization": f"Token {API_KEY}",
        "Content-Type": "application/json",
    }
    
    url = f"{API_BASE_URL}{endpoint}"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(method, url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            error_body = e.response.text
            print(f"Detailed HTTP Error: {error_body}")
            error_msg = f"HTTP error occurred: {e.response.status_code} - {error_body}"
            raise RuntimeError(error_msg)
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise RuntimeError(f"An error occurred: {str(e)}")

@mcp.tool()
async def add_memory(
    messages: List[Dict[str, str]],
    user_id: str = "default_user",
    agent_id: str = "assistant",
    app_id: Optional[str] = None,
    run_id: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
    infer: Optional[bool] = True,
    custom_categories: Optional[Dict[str, Any]] = None,
    custom_instructions: Optional[str] = None,
    includes: Optional[str] = None,
    excludes: Optional[str] = None,
    async_mode: Optional[bool] = True,
    immutable: Optional[bool] = False,
    timestamp: Optional[int] = None,
    expiration_date: Optional[str] = None,
    org_id: Optional[str] = None,
    project_id: Optional[str] = None,
    output_format: Optional[str] = "v1.1",
    version: Optional[str] = "v2"
) -> Any:
    """
    Stores interaction content (messages) into the memory system. Use this to persist information, user preferences, or conversation context that should be retrievable later.

    IMPORTANT:
    To get the best results, pass the RECENT CONVERSATION HISTORY (both user and assistant messages) rather than just a single message.
    This allows the system to infer context and extract accurate memories.

    Args:
        messages: Required. A list of message objects containing 'role' and 'content'.
                  Example of best practice:
                  [
                    {'role': 'user', 'content': 'I only write Python code.'},
                    {'role': 'assistant', 'content': 'Understood, I will focus on Python.'}
                  ]
        user_id: Optional. Identifier for the user. Defaults to 'default_user'.
        agent_id: Optional. Identifier for the agent/assistant. Defaults to 'assistant'.
        app_id: Optional. Identifier for the application.
        run_id: Optional. Identifier for a specific run or session context.
        metadata: Optional. Key-value pairs for storing extra context or tags with the memory.
        infer: Optional. Whether to automatically extract key facts (True) or store raw messages (False). Default: True.
        custom_categories: Optional. A dictionary defining custom categories for memory classification.
        custom_instructions: Optional. Project-specific guidelines for handling memories.
        includes: Optional. Specific preferences to include in the memory.
        excludes: Optional. Specific preferences to exclude from the memory.
        async_mode: Optional. Whether to add memory asynchronously. Default: True.
        immutable: Optional. Whether the memory is immutable. Default: False.
        timestamp: Optional. The timestamp of the memory (Unix timestamp).
        expiration_date: Optional. Date and time when the memory will expire (YYYY-MM-DD).
        org_id: Optional. Organization ID for multi-tenant environments.
        project_id: Optional. Project ID for multi-project environments.
        output_format: Optional. Controls response format structure (v1.0 or v1.1). Default: v1.1.
        version: Optional. The version of the memory to use. Default: v2.
    """
    endpoint = "/v1/memories/"
    
    payload = {
        "messages": messages,
        "infer": infer,
        "async_mode": async_mode,
        "immutable": immutable,
        "output_format": output_format,
        "version": version
    }

    # Add optional parameters if they are provided
    if user_id: payload["user_id"] = user_id
    if agent_id: payload["agent_id"] = agent_id
    if app_id: payload["app_id"] = app_id
    if run_id: payload["run_id"] = run_id
    if metadata: payload["metadata"] = metadata
    if custom_categories: payload["custom_categories"] = custom_categories
    if custom_instructions: payload["custom_instructions"] = custom_instructions
    if includes: payload["includes"] = includes
    if excludes: payload["excludes"] = excludes
    if timestamp is not None: payload["timestamp"] = timestamp
    if expiration_date: payload["expiration_date"] = expiration_date
    if org_id: payload["org_id"] = org_id
    if project_id: payload["project_id"] = project_id

    return await make_request("POST", endpoint, payload)

@mcp.tool()
async def search_memories(
    query: str,
    filters: Dict[str, Any],
    top_k: Optional[int] = 10,
    fields: Optional[List[str]] = None,
    rerank: Optional[bool] = False,
    keyword_search: Optional[bool] = False,
    filter_memories: Optional[bool] = False,
    threshold: Optional[float] = 0.3,
    org_id: Optional[str] = None,
    project_id: Optional[str] = None,
    version: Optional[str] = "v2"
) -> Any:
    """
    Retrieves relevant memories based on semantic similarity to a query. Use this to recall past information, context, or preferences.

    Args:
        query: Required. The search text or question to find related memories for.
        filters: Required. A dictionary of filters to narrow down the search scope (e.g., by user_id, agent_id, time, or metadata).
        top_k: Optional. Maximum number of memory items to return. Default: 10.
        fields: Optional. Specific fields to include in the output objects.
        rerank: Optional. Enable reranking for higher relevance results. Default: False.
        keyword_search: Optional. Enable exact keyword matching alongside semantic search. Default: False.
        filter_memories: Optional. Apply pre-filtering to memories before search. Default: False.
        threshold: Optional. Similarity score threshold (0.0 to 1.0). Only results above this score are returned. Default: 0.3.
        org_id: Optional. Organization ID for multi-tenant environments.
        project_id: Optional. Project ID for multi-project environments.
        version: Optional. The version of the memory to use. Default: v2.
    """
    endpoint = "/v2/memories/search/"
    
    payload = {
        "query": query,
        "filters": filters,
        "top_k": top_k,
        "rerank": rerank,
        "keyword_search": keyword_search,
        "filter_memories": filter_memories,
        "threshold": threshold,
        "version": version
    }

    if fields: payload["fields"] = fields
    if org_id: payload["org_id"] = org_id
    if project_id: payload["project_id"] = project_id

    return await make_request("POST", endpoint, payload)

if __name__ == "__main__":
    mcp.run(transport='stdio')
