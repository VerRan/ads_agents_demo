from typing import Any, Dict, Optional
import httpx
import json
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("dify")

# Constants
url = "http://127.0.0.1:9000/"   # You can get it from dify console.
# DEFAULT_API_KEY = "API_KEY "  # You can get the API_KEY from dify console.

async def make_http_request(url: str, data: Dict[str, Any], streaming: bool = True) -> Dict[str, Any]:
    """Make a request to the Dify API with proper error handling.
    
    Args:
        endpoint: API endpoint to call
        data: Request payload
        api_key: Dify API key
        streaming: Whether to use streaming response mode
    """
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=data, timeout=60.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error: {e.response.status_code}", "details": e.response.text}
        except Exception as e:
            return {"error": f"Request failed: {str(e)}"}
        

@mcp.tool()
async def execute_task(task: str) -> str:
    """Send a message to Dify chat completion API.
    
    Args:
        message: The user message to send
        conversation_id: Optional conversation ID for continuing a conversation
        user_id: Optional user identifier for the request
        api_key: Optional API key to override the default
    """
    data = {
    "task": task,
    "cdp_url": "http://localhost:9222",
    "max_steps": 30
    }
    result = await make_http_request("data", data, streaming=False)
    
    if "error" in result:
        return f"Error: {result['error']}\n{result.get('details', '')}"
    
    # Extract only the answer from the response
    try:
        answer = result.get("answer", "No answer provided")
        return answer
    except Exception as e:
        return f"Failed to parse response: {str(e)}"
    
if __name__ == "__main__":
    # Initialize and run the server
    # mcp.run(transport="streamable-http", host="127.0.0.1", port=9000)
    mcp.run(transport='streamable-http')
    # mcp.run()