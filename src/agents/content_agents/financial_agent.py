# src/agents/content_agents/financial_agent.py
from typing import Dict, Any
from ..base_agent import BaseAgent
from ...rag.financial_news import FinancialNewsRAG
from ...llms.prompts.financial_prompts import FINANCIAL_PROMPTS
import yfinance as yf
from datetime import datetime, timedelta

class FinancialAgent(BaseAgent):
    def _initialize_tools(self) -> Dict[str, Any]:
        return {
            'rag': FinancialNewsRAG(self.config),
            'market_api': self._initialize_market_api()
        }

    def _initialize_market_api(self):
        return {
            'get_market_data': self._get_market_data,
            'get_crypto_data': self._get_crypto_data,
            'get_forex_data': self._get_forex_data
        }

    def _load_prompts(self) -> Dict[str, str]:
        return FINANCIAL_PROMPTS

    def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Get market data
            market_data = self._get_relevant_market_data(task['topic'])
            
            # Get news context from RAG
            news_context = self.tools['rag'].get_relevant_context(task['topic'])
            
            # Combine market data and news
            context = {
                'market_data': market_data,
                'news': news_context
            }
            
            # Get appropriate LLM
            llm = self.get_llm('financial')
            
            # Select prompt template based on platform
            prompt_template = self.prompts.get(
                f"{task['platform']}_template",
                self.prompts['default_template']
            )
            
            # Prepare prompt with context
            prompt = prompt_template.format(
                topic=task['topic'],
                market_data=market_data,
                news=news_context['content'],
                audience=task['audience']
            )
            
            # Generate content
            content = llm.generate(prompt)
            
            return {
                'content': {
                    'text': content,
                    'topic': task['topic'],
                    'platform': task['platform'],
                    'market_data': market_data,
                    'sources': news_context.get('references', [])
                },
                'context_used': context,
                'agent_type': 'financial'
            }
            
        except Exception as e:
            print(f"Error in FinancialAgent: {str(e)}")
            raise

    def _get_market_data(self, symbol: str) -> Dict[str, Any]:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1d")
        return {
            'symbol': symbol,
            'current_price': hist['Close'][-1] if not hist.empty else None,
            'change': hist['Close'][-1] - hist['Open'][-1] if not hist.empty else None,
            'volume': hist['Volume'][-1] if not hist.empty else None
        }

    def _get_relevant_market_data(self, topic: str) -> Dict[str, Any]:
        # Define relevant symbols based on topic
        topic_lower = topic.lower()
        
        if 'crypto' in topic_lower:
            symbols = ['BTC-USD', 'ETH-USD']
        elif 'forex' in topic_lower:
            symbols = ['EURUSD=X', 'GBPUSD=X']
        else:
            symbols = ['^GSPC', '^IXIC', '^DJI']  # Default to major indices
            
        return {symbol: self._get_market_data(symbol) for symbol in symbols}