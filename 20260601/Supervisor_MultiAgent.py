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

# --------------------------------------------------
# State
# --------------------------------------------------

class SupervisorState(TypedDict):
    task: str
    research_notes: str
    draft: str
    critique: str
    score: int
    revision_count: int
    final_answer: str

# --------------------------------------------------
# Research Agent
# --------------------------------------------------

def researcher(state: SupervisorState):

    result = collection.query(
        query_texts=[state["task"]],
        n_results=3,
    )

    context = "\n".join(
        result["documents"][0]
    )

    response = client.chat.completions.create(
        model="gpt-5.4-nano",
        messages=[
            {
                "role": "system",
                "content":
                "당신은 Research Agent이다. "
                "근거를 간결하게 정리하라."
            },
            {
                "role": "user",
                "content":
                f"""
작업:
{state['task']}

근거:
{context}
"""
            }
        ]
    )

    return {
        "research_notes":
        response.choices[0].message.content.strip()
    }


# --------------------------------------------------
# Writer Agent
# --------------------------------------------------

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

조사내용:
{state['research_notes']}

이전 비평:
{state['critique']}

비평을 반영하여 설명문을 작성하라.
"""
            }
        ]
    )

    return {
        "draft":
        response.choices[0].message.content.strip()
    }


# --------------------------------------------------
# Critic Agent
# --------------------------------------------------

def critic(state: SupervisorState):
    response = client.chat.completions.create(
        model="gpt-5.4-nano",
        messages=[
            {
                "role": "system",
                "content":
                """
당신은 Critic Agent이다.

반드시 아래 형식으로 답한다.

SCORE: 숫자

CRITIQUE:
비평 내용
"""
            },
            {
                "role": "user",
                "content":
                f"""
작업:
{state['task']}

초안:
{state['draft']}
"""
            }
        ]
    )

    text = response.choices[0].message.content.strip()

    score = 50

    try:
        import re

        match = re.search(
            r"SCORE:\s*(\d+)",
            text
        )

        if match:
            score = int(match.group(1))

    except Exception:
        pass

    return {
        "critique": text,
        "score": score,
    }


# --------------------------------------------------
# Supervisor
# --------------------------------------------------

def supervisor(state: SupervisorState):
    score = state["score"]
    revision_count = state["revision_count"]
    if score >= 80:
        return {}

    return {
        "revision_count":
        revision_count + 1
    }

# --------------------------------------------------
# Routing
# --------------------------------------------------

def route_after_critic(
    state: SupervisorState
):
    if state["score"] >= 80:
        return "finalizer"
    
    if state["revision_count"] >= 2:
        return "finalizer"

    return "writer"


# --------------------------------------------------
# Finalizer
# --------------------------------------------------

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

최종 초안:
{state['draft']}

비평:
{state['critique']}

최종 답변 작성
"""
            }
        ]
    )

    return {
        "final_answer":
        response.choices[0].message.content.strip()
    }


# --------------------------------------------------
# Graph
# --------------------------------------------------

workflow = StateGraph(
    SupervisorState
)

workflow.add_node(    "researcher",    researcher)
workflow.add_node(    "writer",    writer)
workflow.add_node(    "critic",    critic)
workflow.add_node(    "supervisor",    supervisor)
workflow.add_node(    "finalizer",    finalizer)
workflow.add_edge(    START,    "researcher")
workflow.add_edge(    "researcher",    "writer")
workflow.add_edge(    "writer",    "critic")
workflow.add_edge(    "critic",    "supervisor")
workflow.add_conditional_edges(
    "supervisor",
    route_after_critic,
    {
        "writer": "writer",
        "finalizer": "finalizer",
    }
)
workflow.add_edge(    "finalizer",    END)
app = workflow.compile()

# --------------------------------------------------
# Run
# --------------------------------------------------

result = app.invoke(
    {
        "task":
        "LangGraph Supervisor 기반 멀티 에이전트 패턴 설명",

        "research_notes": "",

        "draft": "",

        "critique": "",

        "score": 0,

        "revision_count": 0,

        "final_answer": "",
    }
)

print("\n=== FINAL ===")
print(result["final_answer"])

print("\n=== SCORE ===")
print(result["score"])

print("\n=== REVISION ===")
print(result["revision_count"])

print("\n=== CRITIQUE ===")
print(result["critique"])

# %%
