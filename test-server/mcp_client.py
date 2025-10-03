from mcp_server import ask_gpt

import asyncio


# 클라이언트 함수: 질문을 보내고 응답을 출력
async def client():
    question = "mcp와 agent의 관계는?"
    result = await ask_gpt(question, None)
    print(f"{question}의 답변: {result}")


# 비동기 함수 실행
asyncio.run(client())
