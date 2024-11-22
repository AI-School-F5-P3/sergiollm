import arxiv
from typing import List, Dict, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from src.utils.config import Config
import logging

class DocumentProcessor:
    """Procesador de documentos científicos para RAG."""
    
    def __init__(self, config: Config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.embeddings = HuggingFaceEmbeddings()
        self.vector_store = self._initialize_vector_store()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
    
    def _initialize_vector_store(self) -> Chroma:
        """Inicializa la base de datos vectorial."""
        return Chroma(
            persist_directory=self.config.chroma_persist_directory,
            embedding_function=self.embeddings
        )
    
    def fetch_arxiv_papers(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Obtiene papers relevantes de arXiv."""
        try:
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )
            
            papers = []
            for result in search.results():
                paper = {
                    "title": result.title,
                    "abstract": result.summary,
                    "authors": [author.name for author in result.authors],
                    "url": result.entry_id,
                    "published": result.published
                }
                papers.append(paper)
            
            return papers
            
        except Exception as e:
            self.logger.error(f"Error fetching arXiv papers: {str(e)}")
            return []
    
    def process_papers(self, papers: List[Dict[str, Any]]) -> None:
        """Procesa y almacena papers en la base de datos vectorial."""
        for paper in papers:
            try:
                # Crear documento combinado
                text = f"""
                Title: {paper['title']}
                Authors: {', '.join(paper['authors'])}
                Abstract: {paper['abstract']}
                URL: {paper['url']}
                """
                
                # Dividir en chunks
                chunks = self.text_splitter.split_text(text)
                
                # Almacenar en la base de datos vectorial
                self.vector_store.add_texts(
                    texts=chunks,
                    metadatas=[{"source": paper['url']} for _ in chunks]
                )
                
            except Exception as e:
                self.logger.error(f"Error processing paper {paper['title']}: {str(e)}")
    
    def query_knowledge_base(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """Consulta la base de conocimiento vectorial."""
        try:
            results = self.vector_store.similarity_search(query, k=k)
            formatted_results = []
            for result in results:
                formatted_result = {
                    "text": result.page_content,
                    "metadata": result.metadata
                }
                formatted_results.append(formatted_result)
            return formatted_results
        except Exception as e:
            self.logger.error(f"Error querying knowledge base: {str(e)}")
            return []
    
    def persist_vector_store(self) -> None:
        """Persiste el estado actual de la base de datos vectorial en disco."""
        try:
            self.vector_store.persist()
            self.logger.info("Vector store persisted successfully.")
        except Exception as e:
            self.logger.error(f"Error persisting vector store: {str(e)}")
    
    def load_vector_store(self) -> None:
        """Carga el estado persistido de la base de datos vectorial desde disco."""
        try:
            self.vector_store.load()
            self.logger.info("Vector store loaded successfully.")
        except Exception as e:
            self.logger.error(f"Error loading vector store: {str(e)}")