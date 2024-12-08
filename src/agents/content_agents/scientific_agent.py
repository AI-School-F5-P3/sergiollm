# src/agents/content_agents/scientific_agent.py
from typing import Dict, Any
from ..base_agent import BaseAgent
from ...rag.quantum_physics import QuantumPhysicsRAG
from ...llms.prompts.scientific_prompts import SCIENTIFIC_PROMPTS

class ScientificAgent(BaseAgent):
    def _initialize_tools(self) -> Dict[str, Any]:
        return {
            'rag': QuantumPhysicsRAG(self.config),
        }

    def _load_prompts(self) -> Dict[str, str]:
        return SCIENTIFIC_PROMPTS

    def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Get scientific context from RAG
            context = self.tools['rag'].get_relevant_context(task['topic'])
            
            # Get appropriate LLM
            llm = self.get_llm('scientific')
            
            # Select prompt template based on platform
            prompt_template = self.prompts.get(
                f"{task['platform']}_template",
                self.prompts['default_template']
            )
            
            # Prepare prompt with context
            prompt = prompt_template.format(
                topic=task['topic'],
                context=context['content'],
                audience=task['audience'],
                references=context.get('references', [])
            )
            
            # Generate content
            content = llm.generate(prompt)
            
            return {
                'content': {
                    'text': content,
                    'topic': task['topic'],
                    'platform': task['platform'],
                    'sources': context.get('references', [])
                },
                'context_used': context,
                'agent_type': 'scientific'
            }
            
        except Exception as e:
            print(f"Error in ScientificAgent: {str(e)}")
            raise