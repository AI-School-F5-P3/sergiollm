# src/rag/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any, List
import os
import json
from datetime import datetime

class BaseRAG(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.cache_dir = config.get('RAG_CACHE_DIR', './cache')
        os.makedirs(self.cache_dir, exist_ok=True)

    @abstractmethod
    def get_relevant_context(self, query: str) -> Dict[str, Any]:
        """Get relevant context for a given query"""
        pass

    @abstractmethod
    def update_knowledge_base(self):
        """Update the knowledge base with new information"""
        pass

    def _save_to_cache(self, key: str, data: Any):
        """Save data to cache"""
        cache_path = os.path.join(self.cache_dir, f"{key}.json")
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump({
                'data': data,
                'timestamp': datetime.now().isoformat()
            }, f)

    def _load_from_cache(self, key: str) -> Any:
        """Load data from cache"""
        cache_path = os.path.join(self.cache_dir, f"{key}.json")
        if os.path.exists(cache_path):
            with open(cache_path, 'r', encoding='utf-8') as f:
                return json.load(f)['data']
        return None

