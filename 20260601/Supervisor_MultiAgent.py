# %%
############################################################################################
# SuperVisor 패턴 : 하나의 상위노드가 여러 작업자를 배치해서 각 작업의 결과를 모아서 최종 답변
############################################################################################
# 초안
# 비평
# 품질 점수
# 80점미만
# 재작성

#       Supervisor
#       Reasearcher
#       Writer
#       Critic
# faile         pass
# Writer        Finalizer

# %%
# 슈퍼바이저를 한단계 더 발전시켜서 에이전트 개념확장
#                     Supervisor
#                          │
#         ┌────────────────┼────────────────┐
#         │                │                │
#         ▼                ▼                ▼
#    ResearchAgent    WriterAgent    CriticAgent
#         │                │                │
#         └────────────────┼────────────────┘
#                          ▼
#                     Finalizer

#  Supervisor--> 오케스트레이터

# %%
import os
import re
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions
from typing_extensions import TypedDict
from langgraph.graph import StateGraph,START,END
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv(override=True)

# openai client
client = OpenAI()
# 임베딩 함수  허깅페이스 :This is a sentence-transformers model 찾아라.
st_ef =  embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name='jhgan/ko-sroberta-multitask'
)
chroma_client = chromadb.PersistentClient()  #DB
collection = chroma_client.get_or_create_collection(   # table
    name = 'Supervisor_MultiAgent',
    embedding_function=st_ef
)

if collection.count() == 0:
    collection.add(
        ids=[
            "doc_langgraph",
            "doc_react",
            "doc_rag",
            "doc_supervisor",
        ],
        documents=[
            "LangGraph는 상태 기반 그래프로 역할별 노드를 연결한다.",
            "ReAct는 생각과 행동을 번갈아 수행하며 중간 도구를 사용할 수 있다.",
            "RAG는 벡터DB에서 찾은 근거를 답변 생성에 사용한다.",
            "Supervisor는 여러 에이전트의 순서와 책임을 조율한다.",
        ],
    )
