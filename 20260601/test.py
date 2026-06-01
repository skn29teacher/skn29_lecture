import os
from dotenv import load_dotenv
load_dotenv(override=True)
os.getenv('OPENAI_API_KEY')[-10:]



from typing_extensions import TypedDict
from langgraph.graph import StateGraph,START, END

class ReActState(TypedDict):
    question:str
    thought:str
    tool_result:str
    answer:str

def think(state:ReActState):
    question = state['question']
    if '문서' in question or '근거' in question:
        thought = '검색도구가 필요합니다..'
    else:
        thought = '바로 답할수 있습니다.'
    return {'thought':thought}

def act(state:ReActState):
    question = state['question']
    if '문서' in question or '근거' in question:
        tool_result = '벡터DB에서 관련 문단 2개를 찾았습니다.'
    else:
        tool_result = '외부도구가 필요하지 않다.'
    return {'tool_result':tool_result}
def answer(state:ReActState):
    answer = f"질문:{state['question']}\n생각:{state['thought']}\n도구:{state['tool_result']}"
    return {'answer':answer}

workflow = StateGraph(ReActState)
workflow.add_node('think',think)
workflow.add_node('act',act)
workflow.add_node('answer',answer)
workflow.add_edge(START,'think')
workflow.add_edge('think','act')
workflow.add_edge('act','answer')
workflow.add_edge('answer',END)
app = workflow.compile()
kwargs = {
    'question':'문서 근거가 피요한 더미 질문입니다.',
    'thought':'',
    'tool_result':'',
    'answer':''
}
result = app.invoke(kwargs)
print(result['answer'])




import chromadb
from dotenv import load_dotenv
from langgraph.graph import StateGraph,START,END
from openai import OpenAI
import chromadb
import os
import re
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

embedding_function = SentenceTransformerEmbeddingFunction(model_name='all-MiniLM-L6-V2')
chroma_client = chromadb.PersistentClient(path='chroma_lesson_01_v3')
collection = chroma_client.get_or_create_collection(
    name = 'react_rag',
    embedding_function=embedding_function
)
if collection.count() == 0:
    collection.add(
        ids=["doc_langgraph", "doc_react", "doc_rag", "doc_chroma"],
        documents=[
            "LangGraph는 상태 기반 그래프로 다단계 에이전트를 설계한다.",
            "ReAct는 reasoning과 acting을 번갈아 수행해 도구 사용을 결합한다.",
            "RAG는 벡터DB 검색 결과를 근거로 답변 품질을 높인다.",
            "ChromaDB는 문서 임베딩을 저장하고 유사한 문서를 검색하는 벡터DB다.",
        ],
    )

