# %%
import os
from dotenv import load_dotenv
load_dotenv(override=True)
os.getenv('OPENAI_API_KEY')[-10:]

# %% [markdown]
# ## ReAct와 LangGraph의 연결 방식
#
# ReAct는 Reason과 Act를 번갈아 수행하는 패턴이다. 질문을 받으면 먼저 현재 답변에 필요한 정보를 판단하고, 부족하면 도구를 호출한다. 그 뒤 도구 결과를 반영해 다시 생각한다.
#
# 아래 코드는 이 흐름을 `think -> act -> answer`의 순서로 분해한다. 상태에는 질문, 생각 메모, 도구 결과, 최종 답변만 둬서 흐름이 어떻게 이어지는지 쉽게 보이도록 만든다.

# %%
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

# %%
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

# 그래프에 들어갈 노드 함수구성 --> Tool
class ReActRAGState(TypedDict):
    question:str
    thought:str
    action:str
    tool_result:str
    answer:str

def think(state:ReActRAGState):
    question = state['question'].lower()
    if any(keyword in question for keyword in ['근거','문서','설명','rag']):
        thought = 'CromaDB에서 근거를 먼저 찾아야 한다'
        action = 'search'
    else:
        thought = '바로 답할 수 있다'
        action = 'respond'
    return {'thought':thought,'action':action}


def search_context(state:ReActRAGState):# 내부문서
    result = collection.query(query_texts=[state['question']], n_results=2)
    context = '\n'.join(result['documents'][0])
    return {'tool_result':context}

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
def respond(state:ReActRAGState):  # LLM이 답변
    answer = f"질문:{state['question']}\n생각:{state['thought']}\n도구:{state['tool_result']}\n\n답변을 생성하세요"
    response = client.chat.completions.create(
        model = 'gpt-5.4-nano',
        messages=[
            {'role':'system','content':'당신은 인공지능 자연어 NLP 전문가입니다.'},
            {'role':'user','content':answer}
        ],
        temperature=0
    )
    return {'answer':response.choices[0].message.content.strip()}

# graph구성
workflow = StateGraph(ReActRAGState)   
workflow.add_node('think',think)
workflow.add_node('search_context',search_context)
workflow.add_node('respond',respond)
workflow.add_edge(START, 'think')
workflow.add_conditional_edges(
    'think',
    lambda state : state['action'],
    {"search":'search_context', "respond":"respond"}
)
workflow.add_edge('search_context','respond')
workflow.add_edge('respond',END)

app = workflow.compile()
kwargs = {
    'question':'LangGraph와 RAG가 연결될때 왜 ReAct는 유용한가?.',
    'thought':'',
    'action':'',
    'tool_result':'',
    'answer':''
}
result = app.invoke(kwargs)
print('route', result['action'])
print('thought', result['thought'])
print('context')
print(result['tool_result'])
print('answer')
print(result['answer'])

# %%
# 기업문서를 벡터Db화  pdf
from pathlib import Path
from typing import Iterable
from uuid import uuid4

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from pypdf import PdfReader

# 문서경로 지정
enterprise_folder = Path(r'.\documents')
# pdf 파일 읽기
def read_pdf_file(path:Path)->str:
    reader = PdfReader(str(path))
    pages:list[str]=[]

    for page in reader.pages:    
        pages.append(page.extract_text() or "")
    return '\n'.join(pages)
    
enterprise_embedding = SentenceTransformerEmbeddingFunction(model_name='all-MiniLM-L6-v2')
enterprize_client = chromadb.PersistentClient()
enterprise_collection = enterprize_client.get_or_create_collection(
    name='enterprise_document',
    embedding_function=enterprise_embedding,
    metadata={'hnsw:space':'cosine'}
)
# txt, md 파일처럼 일반 파일
def read_text_file(path:Path)->str:
    return path.read_text(encoding='utf-8',errors='ignore')

def chunk_text(text:str, chunk_size:int=900, overlab:int=150)->list[str]:
    cleaned = " ".join(text.split())
    if not cleaned:
        return []
    chunks : list[str] = []
    start = 0
    while start < len(cleaned):
        end = min(start+chunk_size, len(cleaned))
        chunks.append(cleaned[start:end])
        if end >= len(cleaned):
            break
        start = end-overlab
    return chunks

from glob import glob
def iter_documents(folder:Path)->Iterable[tuple[Path,str]]:
    for path in folder.rglob('*'):
        if path.is_file():
            surffix = path.suffix.lower()
            if surffix in {'.txt', ".md"}:
                yield path, read_text_file(path)
            elif surffix == '.pdf':
                yield path, read_pdf_file(path)
        

documents_to_add: list[str] = []
metadatas: list[dict[str, str]] = []
ids: list[str] = []

if not enterprise_folder.exists():
    print(f"경고: 기업 문서 폴더가 없습니다: {enterprise_folder}")
    print("폴더 경로를 확인하거나 폴더를 생성한 뒤 다시 실행하세요.")
else:
    for file_path, raw_text in iter_documents(enterprise_folder):
        for index, chunk in enumerate(chunk_text(raw_text), start=1):
            ids.append(f"{file_path.stem}-{index}-{uuid4().hex[:8]}")
            documents_to_add.append(chunk)
            metadatas.append({
                "source_file": file_path.name,
                "source_type": file_path.suffix.lower().lstrip("."),
                "chunk_index": str(index),
            })

    if documents_to_add:
        enterprise_collection.add(
            ids=ids,
            documents=documents_to_add,
            metadatas=metadatas,
        )
        print(f"기업 문서 {len(ids)}개 청크를 벡터DB에 저장했다.")
    else:
        print("enterprise_documents/ 폴더에서 적재할 문서를 찾지 못했다.")

    print("collection count:", enterprise_collection.count())

# %%
# 생성한 벡터db에서 문장이나 단어를 검색해 보세요
from openai import OpenAI
import os
import json
result = enterprise_collection.query(query_texts=['대회 규칙에 대해서 알려주세요'], n_results=2)
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
response = client.chat.completions.create(
        model = 'gpt-5.4-nano',
        messages=[
            {'role':'system',
             'content':'당신은 기업내부또는 외부문서을 기반으로 답변하는 친절한 페르소나 입니다.\n문서에서 추출한 청크들을 기반으로 답변해주세요'},
            {'role':'user','content':json.dumps(result,ensure_ascii=False)}
        ],
        temperature=0
    )
print(response.choices[0].message.content.strip())

# %%
