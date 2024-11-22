import os
from langchain.llms import OpenAI
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración del modelo
llm = OpenAI(model="text-davinci-003", temperature=0.7)

def generate_content(prompt):
    """Genera contenido basado en el prompt."""
    response = llm(prompt)
    return response

if __name__ == "__main__":
    prompt = "Escribe un post breve para LinkedIn sobre las ventajas de la inteligencia artificial."
    print("Generando contenido...\n")
    content = generate_content(prompt)
    print(content)
