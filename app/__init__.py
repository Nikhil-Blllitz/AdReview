from flask import Flask
from dotenv import load_dotenv
import os
from app.routes import bp  # Import the Blueprint

def create_app():
    load_dotenv()  # Load environment variables
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')

    # Register the Blueprint
    app.register_blueprint(bp)

    return app
