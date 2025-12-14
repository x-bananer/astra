from flask import Flask
from flask_cors import CORS

from config import Config
from db import init_db

from routes.auth_routes import auth_bp
from routes.analysis_routes import analysis_bp
from routes.client_routes import client_bp
from routes.group_routes import group_bp

# create a Flask backend app
app = Flask(__name__)
app.secret_key = Config.SECRET_KEY # for the cookies, sessions etc. encryption

# add the CORS configuration to the app so the frontend can call the backend from another origin
CORS(
    app, # the flask app
    supports_credentials=True, # the backend allows the browser the send and recieve credentials (cookies, auth headers)
    origins=[Config.BASE_CLIENT_URL] # the frontend origin
)

# attach all existing blueprints with routes to the app
app.register_blueprint(auth_bp)
app.register_blueprint(analysis_bp)
app.register_blueprint(client_bp)
app.register_blueprint(group_bp)

# initialize the database once when the app starts
init_db()

# equals to `flask --app app run --debug --port 4000`
if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=4000)