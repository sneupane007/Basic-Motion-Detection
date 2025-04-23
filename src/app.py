"""
Main application initialization
"""
from flask import Flask
import os

from src.config.settings import DEBUG, HOST, PORT
from src.api.routes import api_bp
from src.dashboard.routes import dashboard_bp

def create_app():
    """
    Create and configure the Flask application
    
    Returns:
        Flask: The configured Flask application
    """
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    
    # Register blueprints
    app.register_blueprint(api_bp)
    app.register_blueprint(dashboard_bp)
    
    return app

def run_app():
    """Run the Flask application"""
    app = create_app()
    app.run(host=HOST, port=PORT, debug=DEBUG)

if __name__ == '__main__':
    run_app() 