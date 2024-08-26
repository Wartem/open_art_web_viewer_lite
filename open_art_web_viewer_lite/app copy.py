import json
import os
import importlib
import sys

print("Current working directory:", os.getcwd())
print("sys.path:", sys.path)


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
    
print("Current working directory:", os.getcwd())
print("sys.path:", sys.path)

# Read the project name from the config file
config_path = os.path.join(parent_dir, 'config.json')

#if parent_dir not in sys.path:
    #sys.path.insert(0, parent_dir)

try:
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
        project_name = config.get('project_name')

    if not project_name:
        raise ValueError("Project name not found in config file")
    
    # Dynamic import using importlib
    #module = importlib.import_module(project_name)
    
    #module = importlib.import_module('.' + project_name, package=__package__)
    #create_app = getattr(module, 'create_app')
    
    from open_art_web_viewer_lite import create_app

    app = create_app()

    if __name__ == '__main__':
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port)

except FileNotFoundError as e:
    print(f"Error: Config file not found at {config_path}")
    print(f"Error: {str(e)}")
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON in config file at {config_path}")
    print(f"Error: {str(e)}")
except ValueError as e:
    print(f"Error: {str(e)}")
except ImportError as e:
    print(f"Error: Could not import module '{project_name}'. Make sure it exists and is in the correct location.")
    print(f"Error: {str(e)}")
except AttributeError as e:
    print(f"Error: Module '{project_name}' does not have a 'create_app' function.")
    print(f"Error: {str(e)}")
except Exception as e:
    print(f"An unexpected error occurred: {str(e)}")