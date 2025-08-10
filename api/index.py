import os
import sys

# Adiciona o diretório 'src' ao PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.main import app

# Vercel precisa de uma função handler que se comporte como uma aplicação WSGI
def handler(environ, start_response):
    return app(environ, start_response)

if __name__ == "__main__":
    app.run()
