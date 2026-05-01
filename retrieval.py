from langchain_classic.retrievers.document_compressors import FlashrankRerank
from langchain_classic.retrievers import ContextualCompressionRetriever

class StuntingRetriever:
    def __init__(self, vectorstore):
        self.vectorstore = vectorstore
        
    def get_retriever(self):
        # Base retriever dengan MMR untuk diversitas
        base_retriever = self.vectorstore.as_retriever(
            search_type="similarity", 
            search_kwargs={"k": 8}
        )
        
        # Tambahkan Reranker
        compressor = FlashrankRerank(model="ms-marco-MiniLM-L-12-v2", top_n=6)
        compression_retriever = ContextualCompressionRetriever(
            base_compressor=compressor, 
            base_retriever=base_retriever
        )
        return compression_retriever