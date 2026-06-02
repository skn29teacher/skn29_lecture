from fastmcp import FastMCP
mcp = FastMCP(name='SimpleServer')

@mcp.tool
def get_greeting(name:str)->str:
    return f'안녕하세요 {name}님! mcp서버에서 보내는 메세지 입니다.'

@mcp.tool
def multiply(a:float, b:float)->float:
    '''Multiplies two numbers together.'''
    return a*b

if __name__ == '__main__':
    mcp.run()

# uv pip install fastmcp
# 실행은 uv run server.py    