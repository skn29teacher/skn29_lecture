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

class SupervisorState(TypedDict):
    task:str
    research_notes:str
    draft:str
    cirtique:str
    final_answer:str

def supervisor(state:SupervisorState):
    return state

def researcher(state:SupervisorState):
    result = collection.query(
        query_texts=[state['task']],
        n_results=3
    )
    context = '\n'.join(result['documents'][0])
    response = client.chat.completions.create(
        model='gpt-5.4-nano',
        messages=[
            {'role':'system','content':'너는 Reasearch Agent이고 주어진 근거를 요약합니다.'},
            {'role':'user','content':f"작업:{state['task']}\n\n근거:{context}"}
        ]
    )
    return {
        'research_notes': response.choices[0].message.construct.strip()
    }

# -------------------------
# Writer Agent
# -------------------------

def writer(state: SupervisorState):

    response = client.chat.completions.create(
        model="gpt-5.4-nano",
        messages=[
            {
                "role": "system",
                "content":
                "당신은 Writer Agent이다."
            },
            {
                "role": "user",
                "content":
                f"""
작업:
{state['task']}

조사 내용:
{state['research_notes']}

설명문 초안을 작성하라.
"""
            },
        ],
    )

    return {
        "draft":
        response.choices[0].message.content.strip()
    }


# -------------------------
# Critic Agent
# -------------------------

def critic(state: SupervisorState):

    response = client.chat.completions.create(
        model="gpt-5.4-nano",
        messages=[
            {
                "role": "system",
                "content":
                "당신은 Critic Agent이다."
            },
            {
                "role": "user",
                "content":
                f"""
작업:
{state['task']}

초안:
{state['draft']}

부족한 점과 개선점을 평가하라.
"""
            },
        ],
    )

    return {
        "critique":
        response.choices[0].message.content.strip()
    }


# -------------------------
# Finalizer Agent
# -------------------------

def finalizer(state: SupervisorState):

    response = client.chat.completions.create(
        model="gpt-5.4-nano",
        messages=[
            {
                "role": "system",
                "content":
                "최종 답변 작성 Agent"
            },
            {
                "role": "user",
                "content":
                f"""
작업:
{state['task']}

조사:
{state['research_notes']}

초안:
{state['draft']}

비평:
{state['critique']}

비평을 반영하여 최종 답변을 작성하라.
"""
            },
        ],
    )

    return {
        "final_answer":
        response.choices[0].message.content.strip()
    }


graph = StateGraph(    SupervisorState)
graph.add_node(    "supervisor",    supervisor)
graph.add_node(    "researcher",    researcher)
graph.add_node(    "writer",    writer)
graph.add_node(    "critic",    critic)
graph.add_node(    "finalizer",    finalizer)
graph.add_edge(    START,    "supervisor")
graph.add_edge(    "supervisor",    "researcher")
graph.add_edge(    "researcher",    "writer")
graph.add_edge(    "writer",    "critic")
graph.add_edge(    "critic",    "finalizer")
graph.add_edge(    "finalizer",    END)
app = graph.compile()
result = app.invoke(
    {
        "task":
        "LangGraph Supervisor 패턴을 설명하라",
        "research_notes": "",
        "draft": "",
        "critique": "",
        "final_answer": "",
    }
)

print("\n=== FINAL ===")
print(result["final_answer"])

print("\n=== RESEARCH ===")
print(result["research_notes"])

print("\n=== CRITIQUE ===")
print(result["critique"])
