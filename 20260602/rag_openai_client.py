import asyncio
import sys
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv(override=True)

async def main():
    # 실행할 서버를 설정
    env = os.environ.copy()
    env['PYTHONIOENCODING']='utf-8'

    server_params = StdioServerParameters(
        command=sys.executable,   # python 실행파일
        args = ['rag_server.py']  ,
        env=env
    )
    print('서버에 접속을 시도합니다.')
    # stdio (표준입출력)를 통해서 서버 프로세스를 실행하고 연결
    async with stdio_client(server_params) as (read,write):
        # 세션 열기 및 초기화
        async with ClientSession(read,write) as session:
            await session.initialize()
            print('서버와 성공적으로 연결되었습니다.')

            # 서버의 get_greeting Tool 호출
            print(f'[질문] 바나나는 어떤 특징이 있나요?')
            query = '바나나는 어떤 특징이 있나요?'
            result =  await session.call_tool(
                "search_documents",
                arguments={'query':query}
            )
            context = result.content[0].text
            print(f'검색된 context : {context}')
            print('openai 답변 생성중....')
            client = AsyncOpenAI()
            # RAG 프롬프트
            prompt = f'''
다음 제공된 문서를 바탕으로 사용자의 질문에 답하세요

[문서]
{context}

[질문]
{query}
'''
            # openai 호출
            response = await client.chat.completions.create(
                model = 'gpt-5.4-nano',
                messages=[
                    {'role':'system',"content":"당신은 제공된 문서를 기반으로 답변하는 RAG시스템입니다."},
                    {'role':'user','content':prompt}
                ],
                temperature=0
            )
            answer = response.choices[0].message.content
            print(f'최종답변:{answer}')
if __name__ == '__main__':
    asyncio.run(main())
