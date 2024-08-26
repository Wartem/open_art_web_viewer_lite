# open_art_web_viewer initialization
from flask import Flask
import os
import json

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)

    # Load configuration from config.json
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
            app.config.update(config)

    # Set default values for project_name, display_name, and SQLITE_DB_PATH
    app.config.setdefault('project_name', os.path.basename(os.path.dirname(__file__)))
    app.config.setdefault('display_name', app.config['project_name'])
    app.config.setdefault('SQLITE_DB_PATH', os.path.join(os.path.dirname(__file__), 'open_art.db'))

    # ... other configurations ...

    from . import routes
    bp = routes.bp
    bp.name = app.config['project_name']  # Dynamically set the blueprint name
    app.register_blueprint(bp)

    return app