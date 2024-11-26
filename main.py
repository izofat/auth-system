from flask import Flask
from settings import API_PORT, DEBUG


if __name__ == "__main__":
    app = Flask(__name__)
    app.run(port=API_PORT, debug=DEBUG)

