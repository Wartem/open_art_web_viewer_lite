![Python](https://img.shields.io/badge/language-Python-blue.svg)
![Flask](https://img.shields.io/badge/framework-Flask-lightgrey.svg)
![Jinja](https://img.shields.io/badge/template%20engine-Jinja-yellow.svg)
![SQLite](https://img.shields.io/badge/database-SQLite-blue.svg)
![HTML](https://img.shields.io/badge/language-HTML-orange.svg)
![CSS](https://img.shields.io/badge/language-CSS-green.svg)
![JavaScript](https://img.shields.io/badge/language-JavaScript-yellow.svg)
![JSON](https://img.shields.io/badge/data-JSON-lightblue.svg)

# open_art_web_viewer_lite
### A standalone version of Open Art Web Viewer
----------------------
![OpenArtWebViewer 2024-08-27 113110](https://github.com/user-attachments/assets/78a8d204-0b1b-4fb5-ae0c-3ea05ee1230a)

**Overview**
------------

Open Art Web Viewer Lite is a Python-based web application designed to provide an interactive interface for searching and exploring artworks from various collections. The application uses the Flask web framework to handle HTTP requests and render templates, while also utilizing SQLite as its database management system.

**Directory Structure**
----------------------
```
project_root/
├── setup.py                # Setup script for the package
├── runtime.txt             # Specifies the runtime environment
├── routes.py               # Defines the application routes
├── requirements.txt        # Lists project dependencies
├── README.md               # Project documentation
├── pyproject.toml          # Project configuration file
├── Procfile                # Used for deployment (e.g., on Heroku)
├── open_art.db             # Database file
├── LICENSE                 # License information
├── config.json             # Configuration settings in JSON format
├── app.py                  # Main application script
├── __init__.py             # Indicates this directory is a Python package
├── templates/              # Directory for HTML templates
│   ├── search.html         # Template for the search page
│   └── base.html           # Base template for the application
└── static/                 # Directory for static assets
    ├── images/             # Directory for image files
    └── css/                # Directory for CSS stylesheets
```

The project's directory structure can be broken down into several key components:

* `app.py`: This is the main entry point for the application, responsible for creating a Flask instance, loading configuration settings from `config.json`, and setting up routes.
* `routes.py`: This module contains the various Flask routes that handle HTTP requests, including search queries, API endpoints, and more. The routes are defined using the Blueprint system in Flask.
* `templates/`: This directory contains HTML templates used to render pages for users, such as the search pages.
* `static/`: This directory holds CSS files.

**API Endpoints**
----------------

The Open Art Web Viewer Lite API is exposed through several routes defined in `routes.py`. These endpoints allow users to interact with the application programmatically, using HTTP requests. Some key API endpoints include:

* `/search`: This endpoint handles search queries and returns a list of matching artworks.
* `/api/search`: This endpoint provides JSON data for the search results, including pagination information.

**Search Functionality**
------------------------

The search functionality is implemented using a combination of Flask routes and SQL queries against the SQLite database. When a user submits a search query, the application uses a WHERE clause to filter the results based on the specified criteria (e.g., title, attribution, or display date).

**Dynamic Image Loading**
-------------------------

The Open Art Web Viewer Lite application loads artwork images dynamically as you scroll through the search results or individual artwork details. This approach helps to improve performance by only loading a few images at a time, reducing the initial page load time and improving responsiveness.

When you reach the bottom of the page, additional images are loaded automatically, allowing you to see more artworks without having to wait for all of them to be loaded initially. This feature is implemented using JavaScript and HTML techniques that allow the browser to handle the loading of images in the background.

The `loading` attribute on the image tags specifies that they should be loaded lazily, which helps to reduce the initial page load time and improve overall performance.

**Data Cleaning and Database Schema**
------------------

The SQLite database used by Open Art Web Viewer Lite contains a single table called `objects`. This table stores information about each artwork in the collection, including its title, attribution, display date, medium, and more.

A open_art.db file is provided, created by [github.com/Wartem/open_art](https://github.com/Wartem/open_art)
This file can updated by replacing it with a new one from the same project.

The CSV files obtained from various art sources are not "clean" and contain errors. These errors are not fixed before the database is created. Instead, this project includes code to clean and process the data, making it usable for our purposes.

The following schema is used for storing the processed art data:

| Column | Name | Type | Not Null | Default | Primary Key |
|--------|------|------|----------|---------|-------------|
| 0 | source | TEXT | Yes | | No |
| 1 | objectid | TEXT | Yes | | No |
| 2 | title | TEXT | Yes | | No |
| 3 | attribution | TEXT | Yes | | No |
| 4 | beginyear | INTEGER | Yes | | No |
| 5 | endyear | INTEGER | Yes | | No |
| 6 | displaydate | INTEGER | Yes | | No |
| 7 | classification | TEXT | Yes | | No |
| 8 | medium | TEXT | Yes | | No |
| 9 | width | INTEGER | Yes | | No |
| 10 | height | INTEGER | Yes | | No |
| 11 | imgurl_thumb | TEXT | Yes | | No |
| 12 | imgurl_downsized | TEXT | Yes | | No |
| 13 | imgurl_full | TEXT | Yes | | Yes |

The `imgurl_full` column serves as the primary key for the database since objectid insn't unique.

This project handles inconsistencies and errors present in the original CSV files. Data cleaning is internally performed for several reasons:

1. **Transparency**: Keeping the cleaning process within the project allows for clear visibility into data transformations.
2. **Flexibility**: We can easily adapt our cleaning methods as new issues arise.
3. **Source Integrity**: Preserving the original data ensures we can revisit it if needed.

By managing the cleaning process ourselves, we can tailor it to meet the specific needs of this project, ensuring a more reliable dataset.


**Getting Started**
-------------------

### Prerequisites

Before you start, make sure you have the following installed:

* Python 3.x (preferably the latest version)
* pip (the package installer for Python)
* A code editor or IDE of your choice
* Git (if you want to clone the repository)

### Installation

1. Clone the repository using Git into a folder of your choice:
```bash
git clone https://github.com/wartem/open_art_web_viewer_lite.git
```

2. Create and activate a virtual environment (optional but recommended):
```bash
python -m venv .venv
cd open_art_web_viewer_lite

source .venv/bin/activate  # On Unix or MacOS
# OR
.\.venv\Scripts\activate 
```

3. Install the dependencies using pip:
```bash
pip install -r requirements.txt
```

### Running the Application

4. Run the application with Flask:
```bash
python app.py
```
5. Open a web browser and navigate to `http://localhost:5000` to view the application.

**Live Demo**
------------------
[Live demo](https://open-art-web-viewer-lite-fef64c62288d.herokuapp.com/)

**Alternatives**
------------------
**Open Art Viewer**
The SQLite file created by OpenArt can be directly used with the Open Art Viewer.  
You can download it here: [Open Art Viewer 1.0 ](https://sites.google.com/view/wartem/art-viewer) (SQLite file is already included).

**License**
----------

The Open Art Web Viewer Lite project is released under the MIT License. This license allows users to freely use, modify, and distribute the code as they see fit.
