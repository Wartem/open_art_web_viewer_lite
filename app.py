import json
import os
import sys
from __init__ import create_app

#print("Current working directory:", os.getcwd())
#print("sys.path:", sys.path)

current_dir = os.path.dirname(os.path.abspath(__file__))
#parent_dir = os.path.dirname(current_dir)

if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

#if parent_dir not in sys.path:
    #sys.path.insert(0, parent_dir)
    
# Read the project name from the config file
config_path = os.path.join(current_dir, 'config.json')

#try:
with open(config_path, 'r') as config_file:
    config = json.load(config_file)
    project_name = config.get('project_name')

if not project_name:
    raise ValueError("Project name not found in config file")

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
        
#except Exception as e:
    #print(f"An unexpected error occurred: {str(e)}")