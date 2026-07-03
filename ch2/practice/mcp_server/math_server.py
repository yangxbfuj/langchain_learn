"""
Math MCP 服务端：
- 提供技术的计算工具（加法、减法）
- 通过 stdio 提供服务
"""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")


@mcp.tool()
def add(a: int, b: int) -> int:
    """两个数之和"""
    print(f"[Math Server] Add start {a} and {b}")
    result = a + b
    print(f"[Math Server] Add result {result}")
    return result


@mcp.tool()
def multipy(a: int, b: int) -> int:
    """两个数的乘积"""
    print(f"[Math Server] Multipy start {a} and {b}")
    result = a + b
    print(f"[Math Server] Multipy result {result}")
    return result


def start():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    start()
