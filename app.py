import json
import os
import sys
import routes
from flask import Flask


def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)

    # Load configuration from config.json
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    if os.path.exists(config_path):
        with open(config_path, "r") as config_file:
            config = json.load(config_file)
            app.config.update(config)
    else:
        print(f"Warning: {config_path} does not exist. Using default configurations.")

    # Set default values for project_name, display_name, and SQLITE_DB_PATH
    app.config.setdefault("project_name", os.path.basename(os.path.dirname(__file__)))
    app.config.setdefault("display_name", app.config["project_name"])
    app.config.setdefault(
        "SQLITE_DB_PATH", os.path.join(os.path.dirname(__file__), "open_art.db")
    )

    # ... other configurations ...

    bp = routes.bp
    bp.name = app.config["project_name"]  # Dynamically set the blueprint name
    app.register_blueprint(bp)

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # Set the 'FLASK_DEBUG' environment variable for a Flask application in terminal before running
    # For Unix-based systems (Linux, macOS):
    # export FLASK_DEBUG=true
    # For Windows:
    # set FLASK_DEBUG=true
    app.run(host="0.0.0.0", port=port, debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true')