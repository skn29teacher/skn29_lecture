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
from langchain_chroma import Chroma


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
    
    def chunk_documents(self, documents: List[Document])->List[Document]:
        '''문서청킹'''
        print(f'문서청킹시작 : size = {config.CHUNK_SIZE} overlap : {config.CHUNK_OVERLAP}')
        text_spliter = RecursiveCharacterTextSplitter(chunk_size=config.CHUNK_SIZE
                                                      ,chunk_overlap=config.CHUNK_OVERLAP
                                                      ,length_function=len,
                                                      separators = ['\n\n','\n','. ','! ','? ',' ',""]
                                                      )
        chunks = text_spliter.split_documents(documents)        
        for idx, chunk in enumerate(chunks):
            chunk.metadata.update({
                'chunk_id':idx,
                'source_type':'internal',
                'chunk_size':len(chunk.page_content)
            })
        print(f'총 {len(chunks)}개 청크 생성')
        return chunks
        
    def create_vectorstore( self,  chunks: List[Document], ):
        """
        Chroma 벡터스토어 생성
        """
        print("\n 벡터스토어 생성 중...")
        print(
            f"  - 저장 위치: "
            f"{self.persist_directory}"
        )

        print(
            f"  - 컬렉션명: "
            f"{config.CHROMA_COLLECTION_NAME}"
        )

        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            collection_name=
                config.CHROMA_COLLECTION_NAME,
            persist_directory=
                self.persist_directory,
        )

        print(" 벡터스토어 생성 완료"  )

        return vectorstore

    def run(self):
        """
        전체 파이프라인 실행
        """
        print("=" * 60)
        print(
            " 문서 수집 및 "
            "임베딩 파이프라인 시작"
        )
        print("=" * 60)
        documents = self.load_documents()
        if not documents:
            raise ValueError(
                f"{self.doc_path} "
                f"에서 문서를 찾을 수 없습니다."
            )
        chunks = self.chunk_documents(  documents  )
        vectorstore = ( self.create_vectorstore( chunks ) )
        print("\n" + "=" * 60)
        print(" 파이프라인 완료")
        print(            f"원본 문서 수: "       f"{len(documents)}"       )
        print(            f"생성 청크 수: "            f"{len(chunks)}"        )

        print(            f"저장 위치: "            f"{self.persist_directory}"        )

        print("=" * 60)
        return vectorstore


if __name__ =='__main__'    :
    config.validate()
    temp = DocumentIngestion()
    vectorstores = temp.run()