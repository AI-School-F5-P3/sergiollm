class BaseAgent:
    """Clase base para agentes."""
    def __init__(self, name):
        self.name = name

    def process(self, task):
        raise NotImplementedError("Este método debe ser implementado por agentes específicos.")
