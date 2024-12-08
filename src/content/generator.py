from typing import Dict, Any, Optional
from ..agents.coordinator import CoordinatorAgent
from ..image.generator import ImageGenerator

class ContentGenerator:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.coordinator = CoordinatorAgent(config)
        self.image_generator = ImageGenerator(config)

    def generate(self, 
                platform: str, 
                topic: str, 
                audience: str, 
                language: str, 
                context: Optional[Dict] = None,
                generate_image: bool = True) -> Dict[str, Any]:
        
        # Prepare the task
        task = {
            'platform': platform,
            'topic': topic,
            'audience': audience,
            'language': language,
            'context': context,
            'type': self._determine_content_type(topic)
        }
        
        # Generate content through the coordinator
        result = self.coordinator.route_task(task)
        
        # Generate image if requested
        if generate_image:
            try:
                image_path = self.image_generator.generate(prompt=topic)
                result['image_path'] = image_path
            except Exception as e:
                print(f"Error generating image: {str(e)}")
                result['image_path'] = None
        
        return result

    def _determine_content_type(self, topic: str) -> str:
        topic_lower = topic.lower()
        
        if any(keyword in topic_lower for keyword in ['quantum', 'physics', 'science']):
            return 'scientific'
        elif any(keyword in topic_lower for keyword in ['market', 'stock', 'finance']):
            return 'financial'
        
        return 'general'