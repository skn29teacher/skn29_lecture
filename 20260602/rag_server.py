from mcp.server.fastmcp import FastMCP
# 1. MCP 서버 생성
mcp = FastMCP('Retrieval Server')
# 문서데이터베이스(RAG 지식베이스)
KNOWLEDGE_BASE = [
    {"id": 1, "content": "사과(Apple)는 장미과에 속하는 과일로, 비타민 C가 풍부합니다."},
    {"id": 2, "content": "바나나(Banana)는 파초과에 속하며, 칼륨이 매우 풍부하여 운동 선수들에게 인기가 많습니다."},
    {"id": 3, "content": "포도(Grape)는 포도과에 속하며, 와인을 만드는 주된 원료로 사용됩니다."},
    {"id": 4, "content": "MCP(Model Context Protocol)는 AI 모델이 외부 데이터와 안전하게 통신할 수 있게 해주는 개방형 표준입니다."}
]
# 2 클라이언트(LLM 에이전트)가 문서를 검색할 수 있는 tool
@mcp.tool
def search_documents(query:str)->str:
    '''주어진 검색어(query)를 기반으로 지식 베이스에서 관련 문서를 찾아 반환합니다.'''
    # 간단하게 키워드 기반(-->VectorDB로 변경필요)
    results = [doc['content'] for doc in KNOWLEDGE_BASE if query.lower() in doc['content'].lower()]
    if not results:
        return f"{query}에 대한 관련 문서를 찾을 수 없습니다."
    return "\n--\n".join(results)

if __name__ =='__main__':
    mcp.run()