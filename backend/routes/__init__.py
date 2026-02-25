# This file makes the routes directory a Python package
# Import all route blueprints for easy access

from .auth_routes import auth_bp
from .inventory_routes import inventory_bp
from .search_routes import search_bp
from .request_routes import request_bp

# List of all blueprints for registration
__all__ = ['auth_bp', 'inventory_bp', 'search_bp', 'request_bp']

# Optional: Helper function to register all blueprints
def register_blueprints(app):
    """Register all blueprints with the Flask app"""
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(inventory_bp, url_prefix='/api')
    app.register_blueprint(search_bp, url_prefix='/api')
    app.register_blueprint(request_bp, url_prefix='/api')
    
    return app