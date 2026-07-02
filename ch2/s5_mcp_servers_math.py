from typing import Any, Dict, Optional

import httpx
from mcp.server.fastmcp import FastMCP

math_mcp = FastMCP("Math")


@math_mcp.tool()
def add(a: int, b: int) -> int:
    """两个整数的加法

    Args:
        a (int): 第一个加数
        b (int): 第二个加数

    Returns:
        int: 结果和
    """
    return a + b


@math_mcp.tool()
def multipy(a: int, b: int) -> int:
    """两个整数的乘法

    Args:
        a (int): 第一个乘数
        b (int): 第二个乘数

    Returns:
        int: 结果积
    """
    return a * b


def start():
    math_mcp.run(transport="stdio")


if __name__ == "__main__":
    start()
