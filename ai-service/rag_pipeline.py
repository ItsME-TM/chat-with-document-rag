import os
import tempfile
from typing import List, Tuple
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import numpy as np

class RAGPipeline:
    def __init__(self):
        """
        Initialize the RAG pipeline with free local embeddings.
        """
        # Using a small, efficient, and free model from HuggingFace
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            length_function=len,
        )
        self.vector_store = None
        self.document_chunks = []

    def load_document(self, file_path: str) -> List:
        """
        Load document based on file extension.
        Supports PDF, DOCX, and TXT files.
        """
        file_extension = os.path.splitext(file_path)[1].lower()

        if file_extension == '.pdf':
            loader = PyPDFLoader(file_path)
        elif file_extension == '.docx':
            loader = Docx2txtLoader(file_path)
        elif file_extension == '.txt':
            loader = TextLoader(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

        documents = loader.load()
        return documents

    def process_document(self, file_path: str) -> bool:
        """
        Process a document through the full RAG pipeline:
        1. Load document
        2. Split into chunks
        3. Generate embeddings
        4. Store in FAISS vector store
        """
        try:
            # Load document
            documents = self.load_document(file_path)

            # Split document into chunks
            chunks = self.text_splitter.split_documents(documents)
            self.document_chunks = chunks

            # Create FAISS vector store from chunks
            self.vector_store = FAISS.from_documents(chunks, self.embeddings)

            return True
        except Exception as e:
            print(f"Error processing document: {e}")
            return False

    def search_similar_chunks(self, query: str, k: int = 3) -> List[Tuple[str, float]]:
        """
        Search for similar chunks to the query.
        Returns list of (chunk_text, similarity_score) tuples.
        """
        if self.vector_store is None:
            return []

        # Perform similarity search
        docs_and_scores = self.vector_store.similarity_search_with_score(query, k=k)

        # Format results
        results = []
        for doc, score in docs_and_scores:
            results.append((doc.page_content, float(score)))

        return results

    def get_context_for_query(self, query: str, k: int = 3) -> str:
        """
        Get relevant context for a query by searching similar chunks.
        Returns concatenated context string.
        """
        similar_chunks = self.search_similar_chunks(query, k)
        context_parts = [chunk for chunk, score in similar_chunks]
        return "\n\n".join(context_parts)

# Global pipeline instance (in production, you'd want to manage this per session/user)
pipeline_instance = None

def initialize_pipeline() -> RAGPipeline:
    """
    Initialize or return the global pipeline instance.
    """
    global pipeline_instance
    if pipeline_instance is None:
        pipeline_instance = RAGPipeline()
    return pipeline_instance