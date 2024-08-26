import json
import os
import importlib
import sys

# Read the project name from the config file
config_path = os.path.join(os.path.dirname(__file__), 'config.json')

# Add the parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
        project_name = config.get('project_name')

    if not project_name:
        raise ValueError("Project name not found in config file")
    
    # Dynamic import using importlib
    module = importlib.import_module(project_name)
    create_app = getattr(module, 'create_app')

    app = create_app()

    if __name__ == '__main__':
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port)

except FileNotFoundError:
    print(f"Error: Config file not found at {config_path}")
except json.JSONDecodeError:
    print(f"Error: Invalid JSON in config file at {config_path}")
except ValueError as e:
    print(f"Error: {str(e)}")
except ImportError:
    print(f"Error: Could not import module '{project_name}'. Make sure it exists and is in the correct location.")
except AttributeError:
    print(f"Error: Module '{project_name}' does not have a 'create_app' function.")
except Exception as e:
    print(f"An unexpected error occurred: {str(e)}")
sys.exit(1)