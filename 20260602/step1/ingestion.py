'''문서수집 및 임베딩 모듈'''
import os
from typing import List
from datetime import datetime
from tqdm import tqdm
from langchain_community.document_loaders import PyPDFLoader,TextLoader,DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
import chromadb
from langchain_core.documents import Document
from config import config

class DocumentIngestion:
    '''문서수집 및 임베딩 처리 클래스'''
    def __init__(self,doc_path:str = None,persist_directory:str = None):
        self.doc_path = doc_path or config.DOCUMENTS_PATH
        self.persist_directory = persist_directory or config.CHROMA_PRESIST_DIRECTORY
        print(f'임베딩 모델 로딩:{config.EMBEDDING_MODEL}')

        self.embeddings = HuggingFaceEmbeddings(
            model_name=config.EMBEDDING_MODEL,
            model_kwargs={'device':'cpu'},
            encode_kwargs = {'normalize_embeddings':True}
        )
        print('임베딩 모델 로드 완료')
    def load_documents(self)->list[Document]:
        '''pdf txt md 문서 로딩'''
        print(f'문서로딩 시작:{self.doc_path}')
        documents=[]
        supported_extentions = {
            '.pdf','.txt','.md'
        }
        for root,dirs,files in os.walk(self.doc_path):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext not in supported_extentions:
                    continue
                file_path = os.path.join(root,file)
                try:
                    if ext =='.pdf':
                        loader = PyPDFLoader(file_path)
                    else:
                        loader = TextLoader(file_path,encoding='utf-8')
                    docs = loader.load()
                    for doc in docs:
                        doc.metadata.update({
                            'filename':file,
                            'filepath':file_path,
                            'file_type':ext.replace('.',""),
                            'ingestion_date':datetime.now().isoformat(),
                        })
                    documents.extend(docs)
                    print(f'{file}: {len(docs)}개 페이지')
                except Exception as e:
                    print(f'{file} {str(e)}')
        print(f'총 {len(documents)}개 문서 로딩 완료')
        return documents
    
if __name__ =='__main__'    :
    config.validate()
    temp = DocumentIngestion()
    temp.load_documents()