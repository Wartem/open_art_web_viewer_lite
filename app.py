import json
import os
import importlib
import sys
from flask import Flask

print("Current working directory:", os.getcwd())
print("sys.path:", sys.path)

current_dir = os.path.dirname(os.path.abspath(__file__))
#parent_dir = os.path.dirname(current_dir)

if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

#if parent_dir not in sys.path:
    #sys.path.insert(0, parent_dir)
    
# Read the project name from the config file
config_path = os.path.join(current_dir, 'config.json')

with open(config_path, 'r') as config_file:
    config = json.load(config_file)
    project_name = config.get('project_name')

if not project_name:
    raise ValueError("Project name not found in config file")

# Dynamic import using importlib
#module = importlib.import_module(project_name)

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

    #from . import routes
    #bp = routes.bp
    #bp.name = app.config['project_name']  # Dynamically set the blueprint name
    #app.register_blueprint(bp)

    return app

#module = importlib.import_module(project_name)
#create_app = getattr(module, 'create_app')

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)