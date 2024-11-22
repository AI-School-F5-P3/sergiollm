import unittest
from src.agents.content_writer import ContentWriterAgent

class TestContentWriterAgent(unittest.TestCase):
    def test_process(self):
        agent = ContentWriterAgent("Test Writer")
        result = agent.process("Escribe un artículo sobre Python.")
        self.assertIn("Generando contenido basado en el prompt", result)

if __name__ == "__main__":
    unittest.main()
