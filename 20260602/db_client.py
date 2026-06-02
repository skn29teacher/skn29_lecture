"""
db_client.py
============
MCP DbServer와 연동하는 OpenAI Tool Calling 기반 DB 어시스턴트 클라이언트.

흐름:
  1. OpenAI에게 MCP 툴 목록을 함수(tools)로 등록
  2. 사용자 질문 → OpenAI가 필요한 툴 호출 결정
  3. MCP 서버에 실제 툴 실행 요청
  4. 결과를 다시 OpenAI에게 전달 → 최종 자연어 답변 생성
"""

import asyncio
import json
import os

from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import OpenAI

# ── 환경변수 로드 ────────────────────────────────────────────────────────────
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-5.4-nano"

# ── MCP 서버 실행 파라미터 ────────────────────────────────────────────────────
SERVER_PARAMS = StdioServerParameters(
    command="uv",
    args=["run", r"C:\skn29_자연어\20260602\db_server.py"],
)

# ── MCP 툴 → OpenAI function schema 변환 ─────────────────────────────────────

def mcp_tools_to_openai_functions(mcp_tools: list) -> list[dict]:
    """MCP ListToolsResult의 툴 목록을 OpenAI tools 형식으로 변환합니다."""
    functions = []
    for tool in mcp_tools:
        # inputSchema가 없으면 빈 object schema 사용
        parameters = tool.inputSchema if tool.inputSchema else {"type": "object", "properties": {}}
        functions.append({
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description or "",
                "parameters": parameters,
            },
        })
    return functions


# ── 메인 대화 루프 ────────────────────────────────────────────────────────────

async def run(user_question: str):
    async with stdio_client(SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            # MCP 서버 초기화 & 툴 목록 획득
            await session.initialize()
            tools_result = await session.list_tools()
            openai_tools = mcp_tools_to_openai_functions(tools_result.tools)

            print(f"\n[등록된 MCP 툴 수: {len(openai_tools)}]")
            for t in openai_tools:
                print(f"  - {t['function']['name']}: {t['function']['description'][:60]}")

            # ── 초기 메시지 구성 ──────────────────────────────────────────────
            messages = [
                {
                    "role": "system",
                    "content": (
                        "당신은 데이터베이스 전문가 어시스턴트입니다. "
                        "사용자의 질문에 답하기 위해, 먼저 get_database_shema를 호출하여 스키마를 확인한 후, "
                        "execute_sql_query를 사용하여 적절한 SQL 쿼리를 실행하세요. "
                        "결과를 사용자가 이해하기 쉽게 자연어로 설명해 주세요."
                    ),
                },
                {
                    "role": "user",
                    "content": user_question,
                },
            ]

            print(f"\n[사용자 질문] {user_question}\n")

            # ── Tool Calling 루프 ─────────────────────────────────────────────
            while True:
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    tools=openai_tools,
                    tool_choice="auto",
                )
                msg = response.choices[0].message

                # 툴 호출이 없으면 최종 답변 출력
                if not msg.tool_calls:
                    print("[어시스턴트 답변]")
                    print(msg.content)
                    break

                # assistant 메시지를 히스토리에 추가
                messages.append(msg)

                # 각 툴 호출을 MCP 서버에 실행
                for tool_call in msg.tool_calls:
                    func_name = tool_call.function.name
                    func_args = json.loads(tool_call.function.arguments)

                    print(f"[툴 호출] {func_name}({func_args})")

                    mcp_result = await session.call_tool(func_name, func_args)

                    # 결과 텍스트 추출
                    if mcp_result.content:
                        result_text = "\n".join(
                            block.text
                            for block in mcp_result.content
                            if hasattr(block, "text")
                        )
                    else:
                        result_text = "결과 없음"

                    print(f"[툴 결과] {result_text[:200]}{'...' if len(result_text) > 200 else ''}\n")

                    # tool 결과 메시지를 히스토리에 추가
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result_text,
                    })


# ── 진입점 ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    question = "개발팀에서 일하는 직원들 중 가장 급여가 높은 사람의 이름과 급여를 알려주세요."
    asyncio.run(run(question))
