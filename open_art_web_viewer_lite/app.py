import json
import os
import sys

# Add the project root directory to sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Print debug information
print("Current working directory:", os.getcwd())
print("sys.path:", sys.path)

# Read the project name from the config file
config_path = os.path.join(project_root, 'config.json')

try:
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
        project_name = config.get('project_name')

    if not project_name:
        raise ValueError("Project name not found in config file")

    # Import the create_app function
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
    print(f"Error: Could not import create_app function from '{project_name}'. Make sure it exists and is in the correct location.")
    print(f"Error: {str(e)}")
except Exception as e:
    print(f"An unexpected error occurred: {str(e)}")