# FastMCP는 MCP 서버를 빠르게 설정할 수 있는 클래스
from mcp.server.fastmcp import FastMCP

import logging
import asyncio

logging.basicConfig(level=logging.INFO)

mcp = FastMCP("MATH")


@mcp.tool()
def add(a: int, b: int) -> int:
    """두 숫자를 더합니다."""
    logging.info(f"Adding {a} + {b}")  # 로그에 연산 내용 출력
    return a + b


@mcp.tool()
def subtract(a: int, b: int) -> int:
    """두 숫자를 뺍니다."""
    logging.info(f"Subtracting {a} - {b}")  # 로그에 연산 내용 출력
    return a - b


if __name__ == "__main__":
    asyncio.run(
        mcp.run(transport="stdio")
    )  # MCP 서버를 stdio 방식으로 실행  (ex. Cursor나 Claude Desktop에서 연결 가능)
