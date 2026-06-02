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
        args = ['rag_server.py']  ,
        env=env
    )
    print('rag서버에 접속을 시도합니다.')
    # stdio (표준입출력)를 통해서 서버 프로세스를 실행하고 연결
    async with stdio_client(server_params) as (read,write):
        # 세션 열기 및 초기화
        async with ClientSession(read,write) as session:
            await session.initialize()
            print('서버와 성공적으로 연결되었습니다.')

            # 서버의 search_documents Tool 호출
            print(f'[요청] search_documents 호출중...')
            queries = ['바나나','MCP','오렌지']
            for query in queries:
                print('============================')
                print(f'검색키워드:{query}')
                result =  await session.call_tool(
                    "search_documents",
                    arguments={'query':query}
                )                      
                print(f'[응답] {result.content[0].text}')  # mcp는 텍스트나 또는 json형태로 감싸서 응답
            
if __name__ == '__main__':
    asyncio.run(main())
