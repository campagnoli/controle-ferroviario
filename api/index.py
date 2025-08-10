from src.main import app

# Vercel precisa de uma função handler que se comporte como uma aplicação WSGI
def handler(environ, start_response):
    return app(environ, start_response)

if __name__ == "__main__":
    app.run()
