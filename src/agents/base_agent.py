# src/agents/base_agent.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from ..llms.llm_selector import LLMSelector

class BaseAgent(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.llm_selector = LLMSelector(config)
        self.tools = self._initialize_tools()
        self.prompts = self._load_prompts()

    @abstractmethod
    def _initialize_tools(self) -> Dict[str, Any]:
        """Initialize agent-specific tools"""
        pass

    @abstractmethod
    def _load_prompts(self) -> Dict[str, str]:
        """Load agent-specific prompts"""
        pass

    @abstractmethod
    def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process the assigned task"""
        pass

    def get_llm(self, task_type: str) -> Any:
        return self.llm_selector.select_model(task_type)

