import asyncio
import sys
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters
import os

async def main():
    # 실행할 서버를 설정
    env = os.environ.copy()
    env['PYTHONIOENCODING']='utf-8'

    server_params = StdioServerParameters(
        command=sys.executable,   # python 실행파일
        args = ['server.py']  ,
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
            print(f'[요청] get_greeting 호출중...')
            greeting_result =  await session.call_tool(
                "get_greeting",
                arguments={'name':'홍길동'}
            )
            print(f'[응답] {greeting_result.content[0].text}')  # mcp는 텍스트나 또는 json형태로 감싸서 응답

            # 서버의 multiply Tool 호출
            print(f'[요청] multiply 호출중...')
            multiply_result =  await session.call_tool(
                "multiply",
                arguments={'a':10.5, 'b':20.3}
            )
            print(f'[응답] {multiply_result.content[0].text}')  # mcp는 텍스트나 또는 json형태로 감싸서 응답
if __name__ == '__main__':
    asyncio.run(main())
