import requests
from typing import Dict, Any, List
import numpy as np
from sentence_transformers import SentenceTransformer
from datetime import datetime, timedelta
from .base import BaseRAG

class FinancialNewsRAG(BaseRAG):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.embeddings_model = SentenceTransformer(
            config.get('RAG_EMBEDDINGS_MODEL', 'sentence-transformers/all-mpnet-base-v2')
        )
        self.max_articles = 10
        self.cached_articles = self._load_from_cache('financial_articles') or {}
        self.cached_embeddings = self._load_from_cache('financial_embeddings') or {}

    def get_relevant_context(self, query: str) -> Dict[str, Any]:
        """
        Get relevant financial news context for a given query
        """
        try:
            # Update knowledge base if needed
            self._update_if_needed()
            
            # Get query embedding
            query_embedding = self.embeddings_model.encode([query])[0]
            
            # Find most relevant articles
            relevant_articles = self._find_relevant_articles(query_embedding)
            
            # Format context
            context = self._format_context(relevant_articles)
            
            return context
            
        except Exception as e:
            print(f"Error in get_relevant_context: {str(e)}")
            return {
                'content': 'Error retrieving context. Using general knowledge.',
                'references': []
            }

    def update_knowledge_base(self):
        """
        Update the knowledge base with the latest financial news
        """
        try:
            # Fetch financial news using an API
            api_key = self.config.get('NEWS_API_KEY')
            if not api_key:
                raise ValueError("NEWS_API_KEY not found in config.")
            
            url = "https://newsapi.org/v2/everything"
            params = {
                'q': 'finance OR economy OR stock market',
                'language': 'en',
                'sortBy': 'publishedAt',
                'pageSize': self.max_articles,
                'apiKey': api_key
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            articles = response.json().get('articles', [])
            
            for article in articles:
                article_data = {
                    'title': article['title'],
                    'summary': article['description'] or article['content'],
                    'authors': [article['author']] if article['author'] else [],
                    'url': article['url'],
                    'published': article['publishedAt']
                }
                
                # Generate and store embedding
                text_to_embed = f"{article_data['title']} {article_data['summary']}"
                embedding = self.embeddings_model.encode([text_to_embed])[0]
                self.cached_embeddings[article_data['url']] = embedding.tolist()

            # Update cache
            self.cached_articles = {article['url']: article for article in articles}
            self._save_to_cache('financial_articles', self.cached_articles)
            self._save_to_cache('financial_embeddings', self.cached_embeddings)

        except Exception as e:
            print(f"Error updating knowledge base: {str(e)}")

    def _update_if_needed(self):
        """Check if knowledge base needs updating"""
        last_update = self._load_from_cache('last_update')
        if not last_update or datetime.fromisoformat(last_update) < datetime.now() - timedelta(days=1):
            self.update_knowledge_base()
            self._save_to_cache('last_update', datetime.now().isoformat())

    def _find_relevant_articles(self, query_embedding: np.ndarray, top_k: int = 3) -> List[Dict[str, Any]]:
        """Find most relevant articles using embedding similarity"""
        similarities = {}
        for url, article_embedding in self.cached_embeddings.items():
            similarity = np.dot(query_embedding, article_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(article_embedding)
            )
            similarities[url] = similarity

        # Get top-k articles
        top_articles = []
        for url, _ in sorted(similarities.items(), key=lambda x: x[1], reverse=True)[:top_k]:
            if url in self.cached_articles:
                top_articles.append(self.cached_articles[url])

        return top_articles

    def _format_context(self, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Format articles into useful context"""
        if not articles:
            return {
                'content': 'No relevant financial articles found.',
                'references': []
            }

        # Combine summaries and create references
        content = "Based on recent financial news:\n\n"
        references = []

        for article in articles:
            content += f"From '{article['title']}':\n{article['summary']}\n\n"
            references.append({
                'title': article['title'],
                'authors': article['authors'],
                'url': article['url']
            })

        return {
            'content': content.strip(),
            'references': references
        }
