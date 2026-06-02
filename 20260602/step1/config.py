'''설정관리'''
import os
from dotenv import load_dotenv
load_dotenv(override=True)

class Config:
    '''시스템설정'''
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL')
    LLM_MODEL = os.getenv("LLM_MODEL")
    LLM_TEMPERATURE = os.getenv("LLM_TEMPERATURE")
    RETRIEVAL_TOP_K = int(os.getenv('RETRIEVAL_TOP_K'))
    CHUNK_SIZE = int(os.getenv('CHUNK_SIZE'))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP"))
    DOCUMENTS_PATH = os.getenv('DOCUMENTS_PATH','./data/internal_docs')
    CHROMA_PRESIST_DIRECTORY = os.getenv('CHROMA_PRESIST_DIRECTORY')
    CHROMA_COLLECTION_NAME = os.geten('CHROMA_COLLECTION_NAME')



    @classmethod
    def validate(cls):
        '''필수 설정 검증'''
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY 설정되지 않았습니다.")
        if not os.path.exists(cls.DOCUMENTS_PATH):
            os.makedirs(cls.DOCUMENTS_PATH,exist_ok=True)
            print(f'문서디렉터리 생성:{cls.DOCUMENTS_PATH}')

config = Config()
