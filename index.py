```python
from src.main import app

# Vercel precisa de uma função handler
def handler(request):
    return app(request.environ, start_response)

if __name__ == "__main__":
    app.run()
