# MCP 서버 및 도구 실행 시 context 정보 처리
from mcp.server.fastmcp import FastMCP, Context
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

mcp = FastMCP("GPT-4o-mini MCP")


# GPT-4o에 질문을 보내는 도구 정의
@mcp.tool()
async def ask_gpt(question: str, context: Context) -> str:
    # GPT-4o-mini 모델 인스턴스 생성 (temperature=0.3은 약간의 다양성 허용)
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
    return llm.invoke(question)


if __name__ == "__main__":
    mcp.run(transport="stdio")
