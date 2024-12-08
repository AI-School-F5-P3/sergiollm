# src/llms/prompts/financial_prompts.py
FINANCIAL_PROMPTS = {
    'default_template': """
    Create content about {topic} using the following market data and news:
    Market Data: {market_data}
    Recent News: {news}
    
    Target audience: {audience}
    Focus on key trends and actionable insights.
    """,
    
    'blog_template': """
    Write a detailed market analysis blog post about {topic} based on:
    Market Data: {market_data}
    Recent News: {news}
    
    Target audience: {audience}
    
    Include:
    - Current market situation
    - Key trends and patterns
    - Important factors influencing the market
    - Potential implications for investors
    - Data-backed insights
    """,
    
    'twitter_template': """
    Create a concise market update thread about {topic} using:
    Market Data: {market_data}
    Key News: {news}
    
    Make it accessible for {audience}
    Focus on the most important metrics and trends.
    Include relevant $cashtags where appropriate.
    Limit each tweet to 280 characters.
    """,
}