from app import init_app
from constants import PORT

app = init_app()

if __name__ == "__main__":
    app.run(debug = True, port = PORT)
