from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    from .main import bp
    app.register_blueprint(bp)
    return app