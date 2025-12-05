from .auth_routes import auth_bp
from .group_routes import group_bp
from .analysis_routes import analysis_bp
from .client_routes import client_bp

def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(group_bp)
    app.register_blueprint(analysis_bp)
    app.register_blueprint(client_bp)