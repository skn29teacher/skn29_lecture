# %%
############ Router 기반 분기 설계 ##################
# openai로 질문을 분류, 필요할 때만 chromaDB에서 근거를 찾은뒤 답변
# 분류결과에 따라서 필요한 노드만 호출

# 한국어 임베딩 모델
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

# %%
# openai client
client = OpenAI()
# 임베딩 함수  허깅페이스 :This is a sentence-transformers model 찾아라.
st_ef =  embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name='jhgan/ko-sroberta-multitask'
)
chroma_client = chromadb.PersistentClient()  #DB
collection = chroma_client.get_or_create_collection(   # table
    name = 'router_colleciton',
    embedding_function=st_ef
)
# collection 에 데이터 추가
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


class RouterState(TypedDict):
    question:str
    router:str
    retrived_context:str
    answer:str

ALLOWED_ROUTES = {
    'feq','rag','tool'
}
# 라우터 기반 분기
def classify_route(state:RouterState):
    prompt = [
        {'role':'system','content':'질문을 faq, rag,tool중 하나로만 분류한다. 답변은 한 단어로만 출력한다'},
        {'role':'user','content':state['question']}

    ]
    try:
        response = client.chat.completions.create(
            model='gpt-5.4-nano',
            messages=prompt,
            temperature=0
        )
        router = (
            response.choices[0]
            .message.content
            .strip()
            .lower()
        )
    except Exception:
        return "raq"
    if route not in ALLOWED_ROUTES:
        text = state["question"].lower()

        if (
            "계산" in text
            or any(symbol in text for symbol in ["+", "-", "*", "/"])
        ):
            route = "tool"

        elif (
            "문서" in text
            or "근거" in text
            or "rag" in text
        ):
            route = "rag"

        else:
            route = "faq"

    return {
        "route": route
    }

def retrieve_context(state: RouterState):
    result = collection.query(
        query_texts=[state["question"]],
        n_results=2,
    )

    documents = result["documents"][0]

    return {
        "retrieved_context": "\n".join(documents)
    }


def faq_answer(state: RouterState):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "짧고 명확한 한국어 정의를 "
                    "한 문단으로 답한다."
                ),
            },
            {
                "role": "user",
                "content": state["question"],
            },
        ],
        temperature=0,
    )

    return {
        "answer": response.choices[0].message.content.strip()
    }


def rag_answer(state: RouterState):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "주어진 근거만 사용해 한국어로 답한다."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"질문: {state['question']}\n\n"
                    f"근거:\n{state['retrieved_context']}"
                ),
            },
        ],
        temperature=0,
    )

    return {
        "answer": response.choices[0].message.content.strip()
    }


def tool_answer(state: RouterState):
    expression = re.findall(
        r"[0-9\+\-\*/\(\)\.]+",
        state["question"].replace(" ", "")
    )

    if expression:
        try:
            tool_result = str(
                eval(
                    expression[0],
                    {"__builtins__": {}},
                    {}
                )
            )

        except Exception:
            tool_result = "도구 계산에 실패했다."

    else:
        tool_result = (
            "실행형 도구가 필요한 질문으로 분류되었다."
        )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "계산 결과를 짧게 설명하는 "
                    "한국어 답변을 쓴다."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"질문: {state['question']}\n"
                    f"도구 결과: {tool_result}"
                ),
            },
        ],
        temperature=0,
    )

    return {
        "answer": response.choices[0].message.content.strip()
    }


workflow = StateGraph(RouterState)

workflow.add_node(
    "classify_route",
    classify_route
)

workflow.add_node(
    "retrieve_context",
    retrieve_context
)

workflow.add_node(
    "faq_answer",
    faq_answer
)

workflow.add_node(
    "rag_answer",
    rag_answer
)

workflow.add_node(
    "tool_answer",
    tool_answer
)

workflow.add_edge(
    START,
    "classify_route"
)

workflow.add_conditional_edges(
    "classify_route",
    lambda state: state["route"],
    {
        "faq": "faq_answer",
        "rag": "retrieve_context",
        "tool": "tool_answer",
    },
)

workflow.add_edge(
    "retrieve_context",
    "rag_answer"
)

workflow.add_edge(
    "faq_answer",
    END
)

workflow.add_edge(
    "rag_answer",
    END
)

workflow.add_edge(
    "tool_answer",
    END
)

app = workflow.compile()

result = app.invoke(
    {
        "question": "LangGraph의 정의가 무엇인가?",
        "route": "",
        "retrieved_context": "",
        "answer": "",
    }
)

print("route:", result["route"])
print(result["answer"])

# %%
client
