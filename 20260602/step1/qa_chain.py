"""
RAG 체인 구현
"""

from operator import itemgetter

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from langchain_openai import ChatOpenAI

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from config import config


class RAGSystem:

    PROMPT_TEMPLATE = """
당신은 내부 문서 기반 질의응답 전문 AI 어시스턴트입니다.

핵심 지침

1. 반드시 제공된 컨텍스트만 사용하십시오.
2. 컨텍스트에 없으면
   "제공된 내부 문서에 해당 정보가 없습니다."
   라고 답변하십시오.
3. 추측하지 마십시오.
4. 답변 시 참조 문서를 언급하십시오.
5. 한국어로 답변하십시오.

컨텍스트:
{context}

질문:
{question}

답변:
"""

    def __init__(self, persist_directory=None):
        config.validate()
        print("RAG 시스템 초기화 중...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=config.EMBEDDING_MODEL,
            model_kwargs={
                "device": "cpu"
            },
            encode_kwargs={
                "normalize_embeddings": True
            }
        )

        persist_dir = (
            persist_directory
            or config.CHROMA_PRESIST_DIRECTORY
        )

        self.vectorstore = Chroma(
            persist_directory=persist_dir,
            embedding_function=self.embeddings,
            collection_name=config.CHROMA_COLLECTION_NAME,
        )

        self.retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={
                "k": config.RETRIEVAL_TOP_K
            }
        )

        self.llm = ChatOpenAI(
            model=config.LLM_MODEL,
            temperature=config.LLM_TEMPERATURE,
            api_key=config.OPENAI_API_KEY,
        )

        self.chain = self._create_chain()

        print("RAG 시스템 초기화 완료")

    def _format_docs(self, docs):

        formatted_docs = []

        for doc in docs:

            filename = doc.metadata.get(
                "filename",
                "Unknown"
            )

            formatted_docs.append(
                f"[문서명: {filename}]\n"
                f"{doc.page_content}"
            )

        return "\n\n".join(formatted_docs)

    def _create_chain(self):

        prompt = PromptTemplate.from_template(
            self.PROMPT_TEMPLATE
        )

        chain = (
            {
                "context":
                    itemgetter("question")
                    | self.retriever
                    | self._format_docs,

                "question":
                    itemgetter("question"),
            }
            | prompt
            | self.llm
            | StrOutputParser()
        )

        return chain

    def ask(self, question: str):

        answer = self.chain.invoke(
            {
                "question": question
            }
        )

        return answer
    
if __name__ == '__main__':
    rag = RAGSystem()
    result = rag.ask('대회 규칙 알려줘')
    print(result)
