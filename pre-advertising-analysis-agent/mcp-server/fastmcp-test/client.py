import asyncio
from fastmcp import Client

# Create a client instance with proper error handling
client = Client("browser_mcp_server.py")

async def call_tool(task: str):
    try:
        async with client:
            result = await client.call_tool("execute_task", {"task": task})
            print(result)
            return result
    except Exception as e:
        print(f"Error calling tool: {e}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    asyncio.run(call_tool("amazon stock price"))