# src/agents/coordinator.py
from typing import Dict, Any
from .base_agent import BaseAgent
from .content_agents.scientific_agent import ScientificAgent
from .content_agents.financial_agent import FinancialAgent
from .content_agents.general_content_agent import GeneralContentAgent

class CoordinatorAgent:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.agents = self._initialize_agents()

    def _initialize_agents(self) -> Dict[str, BaseAgent]:
        return {
            'scientific': ScientificAgent(self.config),
            'financial': FinancialAgent(self.config),
            'general': GeneralContentAgent(self.config)
        }

    def route_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        try:
            content_type = self._determine_content_type(task)
            return self.agents[content_type].process(task)
        except Exception as e:
            print(f"Error in routing task: {str(e)}")
            # Fallback to general content agent
            return self.agents['general'].process(task)

    def _determine_content_type(self, task: Dict[str, Any]) -> str:
        topic = task.get('topic', '').lower()
        
        # Scientific content identifiers
        scientific_keywords = ['quantum', 'physics', 'science', 'scientific']
        if task.get('type') == 'scientific' or any(keyword in topic for keyword in scientific_keywords):
            return 'scientific'
        
        # Financial content identifiers
        financial_keywords = ['market', 'stock', 'finance', 'crypto', 'forex']
        if task.get('type') == 'financial' or any(keyword in topic for keyword in financial_keywords):
            return 'financial'
        
        return 'general'