# src/llms/prompts/scientific_prompts.py
SCIENTIFIC_PROMPTS = {
    'default_template': """
    Create content about {topic} using the following scientific context:
    {context}
    
    Target audience: {audience}
    Make the content engaging and accessible while maintaining scientific accuracy.
    Include relevant references: {references}
    """,
    
    'blog_template': """
    Write a comprehensive blog post about {topic} based on the following research:
    {context}
    
    Target audience: {audience}
    
    Structure the post with:
    - An engaging introduction
    - Clear explanations of key concepts
    - Real-world applications
    - Visual descriptions where appropriate
    - A conclusion that ties everything together
    
    References: {references}
    """,
    
    'twitter_template': """
    Create an engaging tweet thread about {topic} based on:
    {context}
    
    Make it accessible for {audience} while maintaining scientific accuracy.
    Focus on the most fascinating aspects and practical implications.
    
    Key sources: {references}
    Limit each tweet to 280 characters.
    """,
}

