from mcp import ClientSession  # MCP 클라이언트 세션 객체
from mcp.client.sse import sse_client  # SSE 방식으로 MCP 서버와 통신하는 클라이언트

import asyncio
import sys
import json


async def main():
    # 사용자가 URL 없이 실행할 때
    if len(sys.argv) < 2:
        # 사용법 안내
        print("Usage: python client.py http://127.0.0.1:3000/sse")
        return

    url = sys.argv[1]
    print(f"[클라이언트] 서버에 SSE 연결 시도 중... ({url})")
    # SSE 클라이언트를 통해 서버에 실시간 연결
    async with sse_client(url) as (reader, writer):
        # MCP 프로토콜 세션 초기화
        async with ClientSession(reader, writer) as session:
            await session.initialize()  # 초기 MCP handshake 수행
            print("MCP Chat Client 시작됨. 'quit' 입력 시 종료됩니다.")

            # 사용자 입력 루프
            while True:
                user_input = input("\nQuery: ").strip()
                if user_input.lower() == "quit":
                    try:
                        # JSON 파싱 시도
                        data = json.loads(response.content)
                        print("\n GPT-4o 응답:\n" + data["content"])

                    except json.JSONDecodeError:
                        # 그냥 텍스트일 경우 그대로 출력
                        print("\n GPT-4o 응답:\n" + response.content)

                try:
                    # MCP 서버에 "chat" 도구를 호출하고 사용자 입력 전달
                    response = await session.call_tool("chat", {"input": user_input})
                    # 응답의 content가 문자열인 경우 JSON인지 판별
                    if isinstance(response.content, str):
                        pass
                    elif isinstance(response.content, dict):
                        print(
                            "\n GPT-4o 응답:\n"
                            + response.content.get("content", str(response.content))
                        )
                    else:
                        print("\n GPT-4o 응답:\n" + str(response.content))

                except Exception as e:
                    print(f"오류 발생: {e}")


if __name__ == "__main__":
    asyncio.run(main())
