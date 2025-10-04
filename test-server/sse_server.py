from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from fastapi import FastAPI, Request
from starlette.routing import Mount, Route

import os
import uvicorn

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
mcp = FastMCP("chatbot")


# 단순 대화용 MCP 도구 정의
@mcp.tool()
async def chat(input: str) -> str:
    """LLM과 일반적인 대화를 수행합니다."""
    # GPT-4o에게 입력을 비동기로 전달하고 응답을 받음
    result = await llm.ainvoke(input)

    if hasattr(result, "content"):
        return result.content
    return str(result)


# SSE 서버 전송 계층 설정 ("/messages/" 경로로 POST 및 스트리밍 처리)
sse = SseServerTransport("/messages/")


# SSE 연결을 처리하는 엔드포인트 함수 정의
async def handle_sse(request: Request) -> None:
    # 클라이언트와의 SSE 연결을 수립하고, MCP 서버의 처리 루프를 실행
    async with sse.connect_user(
        request.scope,  # HTTP 요청의 범위 정보
        request.receive,  # HTTP 요청의 수신 메시지
        request._send,  # HTTP 요청의 전송 메시지
    ) as (
        read_stream,
        write_stream,
    ):  # 읽기/쓰기 스트림 객체 확보
        await mcp._mcp_server.run(  # MCP 서버 실행
            read_stream,
            write_stream,
            mcp._mcp_server.create_initialization_options(),  # 초기화 옵션
        )


app = FastAPI(
    debug=True,
    routes=[
        Route("/sse", endpoint=handle_sse),  # 실시간 SSE 연결 핸들러
        # 메시지 POST 처리용 경로 등록
        Mount("/messages/", app=sse.handle_post_message),
    ],
)

if __name__ == "__main__":
    uvicorn.run("sse_server:app", port=3000, reload=True)
