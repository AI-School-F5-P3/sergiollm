from typing import Dict, Any, Optional
from ..rag.quantum_physics import QuantumPhysicsRAG
from ..rag.financial_news import FinancialNewsRAG
from ..llms.llm import LanguageModel
from ..llms.prompts.general_prompts import GENERAL_PROMPTS

class GeneralContentAgent:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.llm = LanguageModel(config.get('LLM_API_KEY'))
        
        # Instantiate RAGs for different domains
        self.rag_quantum = QuantumPhysicsRAG(config)
        self.rag_financial = FinancialNewsRAG(config)

    def generate_content(
        self, 
        topic: str, 
        query: str, 
        format: str = "LinkedIn"
    ) -> Dict[str, Any]:
        """
        Generate content based on the topic, query, and format.
        """
        try:
            # Step 1: Retrieve relevant context
            if topic.lower() == "quantum physics":
                context = self.rag_quantum.get_relevant_context(query)
            elif topic.lower() == "financial news":
                context = self.rag_financial.get_relevant_context(query)
            else:
                return {
                    "error": f"Topic '{topic}' is not supported.",
                    "content": None
                }

            # Step 2: Use LLM to generate content
            prompt = GENERAL_PROMPTS.get(format, "").format(
                query=query,
                context=context["content"]
            )
            content = self.llm.generate(prompt)

            # Step 3: Return generated content along with references
            return {
                "content": content,
                "references": context.get("references", [])
            }

        except Exception as e:
            return {
                "error": f"Error generating content: {str(e)}",
                "content": None
            }

    def update_knowledge_bases(self):
        """
        Update all knowledge bases.
        """
        try:
            self.rag_quantum.update_knowledge_base()
            self.rag_financial.update_knowledge_base()
            return {"status": "Knowledge bases updated successfully."}
        except Exception as e:
            return {"status": f"Error updating knowledge bases: {str(e)}"}

