from flask import Flask

from auth_system.routes import bp
from settings import API_PORT, DEBUG

if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(bp)
    app.run(port=API_PORT, debug=DEBUG)
