import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient


def build_tools() -> MultiServerMCPClient:
    mcp_client = MultiServerMCPClient({
        "Math": {
            "transport": "stdio",
            "command": "uv",
            "args": ["run", "-m", "ch2.practice.mcp_server.math_server", "start"],
        },
        "Weather": {"transport": "streamable-http", "url": "http://localhost:8000/mcp"},
    })
    return asyncio.run(mcp_client.get_tools())
