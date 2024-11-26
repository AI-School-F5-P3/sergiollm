class LangSmithTracker:
    def __init__(self, config):
        self.config = config
    
    def track_generation(self, platform, topic):
        # Simular un tracker básico
        print(f"Tracking generation for platform: {platform}, topic: {topic}")
        yield
