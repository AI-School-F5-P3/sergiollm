import subprocess
import os
import sys

def start_ollama_server():
    try:
        # Ejecuta el comando para iniciar el servidor de Ollama
        subprocess.Popen(
            ['ollama', 'serve', '--host', '127.0.0.1', '--port', '11434'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("Servidor Ollama iniciado en http://127.0.0.1:11434")
    except FileNotFoundError as e:
        print(f"Error al intentar ejecutar Ollama: {e}")
    except Exception as e:
        print(f"Ha ocurrido un error: {e}")

if __name__ == "__main__":
    start_ollama_server()
