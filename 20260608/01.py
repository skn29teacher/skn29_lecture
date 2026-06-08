import os
import sys
import torch
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings,HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langgraph.graph import StateGraph, END
from typing_extensions import TypedDict

# 벡터데이터베이스 로드
embeddings = HuggingFaceEmbeddings(model_name="jhgan/ko-sroberta-multitask")
vector_db = Chroma(persist_directory="./chroma_db_session", embedding_function=embeddings)
retriever = vector_db.as_retriever(search_kwargs={"k": 2})

model_id = 'Qwen/Qwen2.5-1.5B-Instruct'
local_model_dir = './local_qwen_model'

if not os.path.exists(local_model_dir):
    os.makedirs(local_model_dir, exist_ok=True)
    _tokenizer = AutoTokenizer.from_pretrained(model_id)
    _model = AutoModelForCausalLM.from_pretrained(model_id,torch_dtype = torch.float32)
    _tokenizer.save_pretrained(local_model_dir)
    _model.save_pretrained(local_model_dir)

tokenizer = AutoTokenizer.from_pretrained(local_model_dir)
model = AutoModelForCausalLM.from_pretrained(model_id,torch_dtype = torch.float32,
                                             device_map='cpu',low_cpu_mem_usage=True)

pipe = pipeline(
    'text-generation',
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=256,
    max_length=None,
    temperature=0.1,
    do_sample=True,
    clean_up_tokenization_spaces=False,
    return_full_text=False
)
llm = HuggingFacePipeline(pipeline=pipe)

class GraphState(TypedDict):
    question:str
    context:str
    generation:str
    source_info:str

def retrieve(state:GraphState):
    print('--retrieve node --')
    question = state['question']
    docs = retriever.invoke(question)
    contexts,sources = [],[]
    for i, doc in enumerate(docs):
        # 텍스트데이터 포멧팅
        contexts.append(f'[문서 {i+1}] {doc.page_content}')
        # 메타데이터 추출
        filename = doc.metadata.get('filename', 'N/A')
        f_type = doc.metadata.get('file_type', 'N/A')
        cat = doc.metadata.get('category', 'N/A')
        sources.append(f"-문서 {i+1} [파일명:{filename} / 유형 : {f_type} / 카테고리 : {cat} ]")
    contexts_str = '\n\n'.join(contexts)
    sources_str = '\n\n'.join(sources)
    print(f'Retrieve {len(docs)} documents')
    return {"context":contexts_str, "source_info":sources_str}

def generate(state:GraphState):
    print('--generate node --')
    question = state['question']
    context = state['context']
    # LLM을 위한 프롬프트 템플릿
    messages = [
        {'role':'system', 'content':"주어진 문장을 참고해서 사용자의 질문에 한국어로 정확하고 간결하게 답변하세요"},
        {'role':'user','content':f'[본문]\n{context}\n\n[질문]\n{question}'}
    ]
    prompt = tokenizer.apply_chat_template(messages,tokenize=False, add_generation_prompt=True)
    response = llm.invoke(prompt)
    return {'generation':response.strip(), "source_info":state["source_info"]}

workflow = StateGraph(GraphState)
workflow.add_node('retrieve',retrieve)
workflow.add_node('generate',generate)
workflow.set_entry_point('retrieve')
workflow.add_edge('retrieve','generate')
workflow.add_edge('generate',END)
app = workflow.compile()

if __name__=='__main__':
    print('종료하려면 q를 입력하세요')
    while True:
        try:
            user_question = input("질문\n")
            if user_question.strip().lower() in ['q','exit','quit']:
                print('프로그램을 종료합니다.')
                break
            inputs = {'question':user_question}
            final_state = app.invoke(inputs)
            print('\n========= 답변 =======')
            print(final_state['generation'])
            print('\n========= 출처정보 =======')
            print(final_state['source_info'])
            print('\n=========================')
        except Exception as e:
            print(f'error : {e}')
            break