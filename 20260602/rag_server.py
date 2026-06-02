from mcp.server.fastmcp import FastMCP
import chromadb

# 1. MCP 서버 생성
mcp = FastMCP('Retrieval Server')

# 2. Vector DB (ChromaDB) 설정
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="knowledge_base")

# 문서 데이터베이스(RAG 지식베이스)
KNOWLEDGE_BASE = [
    {"id": "doc1", "content": "사과(Apple)는 장미과에 속하는 과일로, 비타민 C가 풍부합니다."},
    {"id": "doc2", "content": "바나나(Banana)는 파초과에 속하며, 칼륨이 매우 풍부하여 운동 선수들에게 인기가 많습니다."},
    {"id": "doc3", "content": "포도(Grape)는 포도과에 속하며, 와인을 만드는 주된 원료로 사용됩니다."},
    {"id": "doc4", "content": "MCP(Model Context Protocol)는 AI 모델이 외부 데이터와 안전하게 통신할 수 있게 해주는 개방형 표준입니다."}
]

import sys

# Vector DB에 문서 추가 (자동으로 임베딩 벡터 생성됨)
print("Vector DB에 문서를 임베딩 중입니다... 잠시만 기다려주세요.", file=sys.stderr, flush=True)
collection.add(
    documents=[doc["content"] for doc in KNOWLEDGE_BASE],
    ids=[doc["id"] for doc in KNOWLEDGE_BASE]
)
print("임베딩 완료!", file=sys.stderr, flush=True)

# 3. 클라이언트(LLM 에이전트)가 문서를 검색할 수 있는 tool
@mcp.tool()
def search_documents(query: str) -> str:
    '''주어진 검색어(query)를 기반으로 지식 베이스에서 관련 문서를 찾아 반환합니다. (VectorDB 유사도 검색)'''
    # Vector DB에서 가장 유사한 문서 1개 검색
    results = collection.query(
        query_texts=[query],
        n_results=1
    )
    
    if not results['documents'] or not results['documents'][0]:
        return f"'{query}'에 대한 관련 문서를 찾을 수 없습니다."
        
    # 검색된 문서들을 반환
    found_docs = results['documents'][0]
    return "\n--\n".join(found_docs)

if __name__ =='__main__':
    mcp.run()