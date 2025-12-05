from flask import Flask
from flask_cors import CORS

from config import Config
from db import init_db

from routes.auth_routes import auth_bp
from backend.routes.analysis_routes import analysis_bp
from routes.client_routes import client_bp
from routes.group_routes import group_bp

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

CORS(
    app,
    supports_credentials=True,
    origins=["http://localhost:3000"]
)

app.register_blueprint(auth_bp)
app.register_blueprint(analysis_bp)
app.register_blueprint(client_bp)
app.register_blueprint(group_bp)

init_db()

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=4000)