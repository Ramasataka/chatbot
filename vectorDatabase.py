import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

class VectorDatabase:
    def __init__(self, persist_directory="./chroma_db_stunting_1024_512_new_chunking"):
        self.persist_directory = persist_directory
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )
        
    def load_db(self):
        if not os.path.exists(self.persist_directory):
            print(f"⚠️ Folder {self.persist_directory} tidak ditemukan!")
        
        vectorstore = Chroma(
            persist_directory=self.persist_directory, 
            embedding_function=self.embeddings
        )
        print("✅ Database Chroma berhasil dimuat.")
        return vectorstore