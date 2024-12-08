# src/rag/quantum_physics.py
import arxiv
from typing import Dict, Any, List
import numpy as np
from sentence_transformers import SentenceTransformer
from datetime import datetime, timedelta
from .base import BaseRAG

class QuantumPhysicsRAG(BaseRAG):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.embeddings_model = SentenceTransformer(
            config.get('RAG_EMBEDDINGS_MODEL', 'sentence-transformers/all-mpnet-base-v2')
        )
        self.max_papers = 5
        self.cached_papers = self._load_from_cache('quantum_papers') or {}
        self.cached_embeddings = self._load_from_cache('quantum_embeddings') or {}

    def get_relevant_context(self, query: str) -> Dict[str, Any]:
        """
        Get relevant quantum physics context for a given query
        """
        try:
            # Update knowledge base if needed
            self._update_if_needed()
            
            # Get query embedding
            query_embedding = self.embeddings_model.encode([query])[0]
            
            # Find most relevant papers
            relevant_papers = self._find_relevant_papers(query_embedding)
            
            # Format context
            context = self._format_context(relevant_papers)
            
            return context
            
        except Exception as e:
            print(f"Error in get_relevant_context: {str(e)}")
            return {
                'content': 'Error retrieving context. Using general knowledge.',
                'references': []
            }

    def update_knowledge_base(self):
        """
        Update the knowledge base with new quantum physics papers
        """
        try:
            # Search for recent quantum physics papers
            client = arxiv.Client()
            search = arxiv.Search(
                query = "cat:quant-ph",
                max_results = self.max_papers,
                sort_by = arxiv.SortCriterion.SubmittedDate
            )

            papers = []
            for result in client.results(search):
                paper_data = {
                    'title': result.title,
                    'summary': result.summary,
                    'authors': [author.name for author in result.authors],
                    'url': result.entry_id,
                    'published': result.published.isoformat()
                }
                papers.append(paper_data)
                
                # Generate and store embedding
                text_to_embed = f"{paper_data['title']} {paper_data['summary']}"
                embedding = self.embeddings_model.encode([text_to_embed])[0]
                self.cached_embeddings[paper_data['url']] = embedding.tolist()

            # Update cache
            self.cached_papers = {paper['url']: paper for paper in papers}
            self._save_to_cache('quantum_papers', self.cached_papers)
            self._save_to_cache('quantum_embeddings', self.cached_embeddings)

        except Exception as e:
            print(f"Error updating knowledge base: {str(e)}")

    def _update_if_needed(self):
        """Check if knowledge base needs updating"""
        last_update = self._load_from_cache('last_update')
        if not last_update or datetime.fromisoformat(last_update) < datetime.now() - timedelta(days=1):
            self.update_knowledge_base()
            self._save_to_cache('last_update', datetime.now().isoformat())

    def _find_relevant_papers(self, query_embedding: np.ndarray, top_k: int = 3) -> List[Dict[str, Any]]:
        """Find most relevant papers using embedding similarity"""
        similarities = {}
        for url, paper_embedding in self.cached_embeddings.items():
            similarity = np.dot(query_embedding, paper_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(paper_embedding)
            )
            similarities[url] = similarity

        # Get top-k papers
        top_papers = []
        for url, _ in sorted(similarities.items(), key=lambda x: x[1], reverse=True)[:top_k]:
            if url in self.cached_papers:
                top_papers.append(self.cached_papers[url])

        return top_papers

    def _format_context(self, papers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Format papers into useful context"""
        if not papers:
            return {
                'content': 'No relevant research papers found.',
                'references': []
            }

        # Combine summaries and create references
        content = "Based on recent quantum physics research:\n\n"
        references = []

        for paper in papers:
            content += f"From '{paper['title']}':\n{paper['summary']}\n\n"
            references.append({
                'title': paper['title'],
                'authors': paper['authors'],
                'url': paper['url']
            })

        return {
            'content': content.strip(),
            'references': references
        }