# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import config_by_name
from app.routes import api
import os
import logging

# Initialize SQLAlchemy
db = SQLAlchemy()


def configure_logging(app):
    """Configure logging for the application"""
    if not app.debug:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        ))
        app.logger.addHandler(handler)
        app.logger.setLevel(logging.INFO)


def create_app(config_name='development'):
    """Factory function to create the Flask application"""
    app = Flask(__name__)

    # Set configuration
    app.config.from_object(config_by_name[config_name])

    # Initialize extensions
    db.init_app(app)

    # Configure logging
    configure_logging(app)

    # Register blueprints
    app.register_blueprint(api, url_prefix='/v1/gpay')

    # Create database tables
    with app.app_context():
        db.create_all()

    return app


def main():
    """Main function to run the application"""
    config_name = os.getenv('FLASK_ENV', 'development')
    app = create_app(config_name)
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


if __name__ == "__main__":
    main()
