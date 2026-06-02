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

class DocumentIngrestion:
    '''문서수집 및 임베딩 처리 클래스'''
    def __init__(self,doc_path:str = None,persist_directory:str = None):
        self.doc_path = doc_path or config.DOCUMENTS_PATH
        self.persist_directory = persist_directory or config.CHRO