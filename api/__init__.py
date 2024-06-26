# api/routes/__init__.py
from .routes import api

def register_routes(app):
    app.register_blueprint(api)
