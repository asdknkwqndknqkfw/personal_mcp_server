from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType

import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")


# 간단한 덧셈 함수를 정의하고 랭체인 도구로 등록
@tool
def add(a: int, b: int) -> int:
    """두 숫자를 더합니다."""
    return a + b


# 간단한 뺄셈 함수를 정의하고 랭체인 도구로 등록
@tool
def subtract(a: int, b: int) -> int:
    """두 숫자를 뺍니다."""
    return a - b


tools = [add, subtract]

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 랭체인의 Function Calling 기반 에이전트를 초기화
# LLM이 사용자 입력을 분석해 적절한 도구(add/subtract)를 자동으로 선택해 호출
agent = initialize_agent(
    llm=llm,
    tools=tools,
    agent=AgentType.OPENAI_FUNCTIONS,  # Function Calling 기반 에이전트
    verbose=True,
)

# 사용자 질의 입력에 대해 에이전트가 적절한 도구(subtract)를 선택하여 실행
response = agent.run("5에서 3을 뺀 결과는?")
print(response)
