import os
import sys
import json
import importlib
import contextlib
from flask import Blueprint, render_template, redirect, url_for, current_app, request, jsonify
import sqlite3

from typing import List, Dict, Any, Optional
from datetime import datetime

project_dir = os.path.dirname(__file__)
project_name = os.path.basename(project_dir)

bp = Blueprint(project_name, __name__, template_folder=os.path.join(project_dir, 'templates'))

source_trans = {'NGA': 'National Gallery of Art', 'MM': 'The Metropolitan Museum of Art'}

VALID_SEARCH_TYPES = {'title', 'attribution', 'displaydate'}
VALID_ART_TYPES = {'all', 'Print', 'Index of American Design', 'Drawing', 
                   'Photograph', 'Painting', 'Sculpture', 'Volume', 'Decorative Art', 
                   'Portfolio', 'Technical Material', 'Time Based Media Art'}

@bp.route('/', methods=['GET', 'POST'])
def index():
    project_name = current_app.config.get('project_name', 'Open Art Web Viewer')
    display_name = current_app.config.get('display_name', project_name)
    
    return render_template('search.html', project_name=project_name, display_name=display_name)
    #return render_template('search.html', project_name=project_name, display_name=display_name)

def generate_result_list(results: List[tuple]) -> List[Dict[str, Any]]:
    def check_undefined(s):
        return s.replace("undefined", "null").replace("\"", "") if isinstance(s, str) else s
    
    def clean_string(s: Optional[str]) -> str:
        s = check_undefined(s)
        return s.strip() if isinstance(s, str) else str(s).strip()

    def _clean_int(i: Any) -> int:
        try:
            return int(float(i))
        except (ValueError, TypeError):
            return 0

    def _clean_url(url) -> str:
        if not isinstance(url, str) or not url:
            return ""
        url = url.strip().lower()
        if not url.startswith(('http://', 'https://')):
            url = f"https://{url}"
        return url

    def _clean_year(year: Any) -> Optional[int]:
        cleaned = _clean_int(year)
        current_year = datetime.now().year
        return cleaned if 0 <= cleaned <= current_year else None

    def _clean_dimensions(dim: Any) -> Optional[float]:
        try:
            return round(float(dim), 2)
        except (ValueError, TypeError):
            return str(dim)

    cleaned_results = []
    for r in results:
        if not r or len(r) < 14:
            continue

        cleaned_result = {
            'source': clean_string(source_trans.get(r[0], r[0])),  
            'objectid': clean_string(r[1]),
            'title': clean_string(r[2]),
            'attribution': clean_string(r[3]),
            'beginyear': clean_string(r[4]),
            'endyear': clean_string(r[5]),
            'displaydate': clean_string(r[6]),
            'classification': clean_string(r[7]),
            'medium': clean_string(r[8]),
            'width': clean_string(r[9]),
            'height': clean_string(r[10]),
            'imgurl_thumb': clean_string(r[11]),
            'imgurl_downsized': clean_string(r[12]),
            'imgurl_full': clean_string(r[13])
        }

        cleaned_results.append(cleaned_result)

    return cleaned_results


def generate_result_list_simple(results):
        # Convert results to a list of dictionaries
    return [
        {
            'source': source_trans.get(r[0], r[0]),
            'objectid': r[1],
            'title': r[2],
            'attribution': r[3],
            'beginyear': r[4],
            'endyear': r[5],
            'displaydate': r[6],
            'classification': r[7],
            'medium': r[8],
            'width': r[9],
            'height': r[10],
            'imgurl_thumb': r[11],
            'imgurl_downsized': r[12],
            'imgurl_full': r[13]
        } for r in results
    ]

@bp.route('/search', methods=['GET', 'POST'])
def search():
    project_name = current_app.config.get('project_name', 'Open Art Web Viewer')
    display_name = current_app.config.get('display_name', project_name)
    
    search_type = request.form.get('search_type', 'title') if request.method == 'POST' else request.args.get('search_type', 'title')
    art_type = request.form.get('art_type', 'all') if request.method == 'POST' else request.args.get('art_type', 'all')
    query = request.form.get('query', '') if request.method == 'POST' else request.args.get('query', '')
    
    page = request.args.get('page', 1, type=int)
    per_page = 12  # Number of items per page
    
    '''
    print(f"Debug - Request method: {request.method}")
    print(f"Debug - search_type: {search_type}")
    print(f"Debug - art_type: {art_type}")
    print(f"Debug - query: {query}")
    '''

    if query:
        conn = sqlite3.connect(current_app.config['SQLITE_DB_PATH'])
        c = conn.cursor()
        
        # Adjust WHERE clause based on search_type
        if search_type == 'title':
            where_clause = "title LIKE ?"
        elif search_type == 'attribution':
            where_clause = "attribution LIKE ?"
        elif search_type == 'displaydate':
            # where_clause = "(beginyear <= ? AND endyear >= ?)"
            where_clause = "displaydate LIKE ?"
        else:
            where_clause = "title LIKE ?"  # Default to title search if invalid search_type

        search_param = query if isinstance(query, tuple) else (f'%{query}%',)

        if art_type != 'all':
            where_clause += " AND classification = ?"
            search_param += (art_type,)
            
        # Validate search_type and art_type
        if search_type not in VALID_SEARCH_TYPES:
            return render_template('search.html', error="Invalid search type", query=query,
                                project_name=project_name, display_name=display_name)
        if art_type not in VALID_ART_TYPES:
            return render_template('search.html', error="Invalid art type", query=query,
                                project_name=project_name, display_name=display_name)

        # Get total count
        count_query = f"SELECT COUNT(*) FROM objects WHERE {where_clause}"
        
        c.execute(count_query, search_param)
            
        total = c.fetchone()[0]

        # Get paginated results with all fields
        offset = (page - 1) * per_page
        
        results_query = f"""
            SELECT source, objectid, title, attribution, beginyear, endyear, displaydate, 
                   classification, medium, width, height, imgurl_thumb, imgurl_downsized, imgurl_full
            FROM objects 
            WHERE {where_clause}
            LIMIT ? OFFSET ?
        """
        # print(results_query)
        
        # print(search_param + (per_page, offset))
        
        c.execute(results_query, search_param + (per_page, offset))
        results = c.fetchall()
        conn.close()

        # Convert results to a list of dictionaries
        results_list = generate_result_list(results)
        
    else:
        results_list = []
        total = 0
    
    #print(f"Debug - Query: {query}, Search Type: {search_type}, Art Type: {art_type}")
    #print(f"Debug - Total results: {total}")
    #print(f"Debug - First few results: {results_list[:3]}")  # Print first 3 results


    try:
        return render_template('search.html', 
                           #results=Markup(json.dumps(results_dict, 
                           results=results_list,
                           query=query if isinstance(query, str) else (query[0] if query else ''),
                           search_type=search_type,
                           art_type=art_type,
                           page=page, 
                           per_page=per_page, 
                           total=total,
                           project_name=project_name, 
                           display_name=display_name)
        
    except json.JSONDecodeError as e:
        print(f"JSON encoding error: {e}")


@bp.route('/api/search', methods=['GET'])
def api_search():
    project_name = current_app.config.get('project_name', 'Open Art Web Viewer')
    display_name = current_app.config.get('display_name', project_name)
    
    query = request.args.get('query', '')
    search_type = request.args.get('search_type', 'title')
    art_type = request.args.get('art_type', 'all')
    page = request.args.get('page', 1, type=int)
    per_page = 12  # Number of items per page
    
    conn = None
    try: 
        conn = sqlite3.connect(current_app.config['SQLITE_DB_PATH'])
        c = conn.cursor()


        # Base query
        base_query = """
            SELECT source, objectid, title, attribution, beginyear, endyear, displaydate,
                classification, medium, width, height, imgurl_thumb, imgurl_downsized, imgurl_full
            FROM objects 
            WHERE """

        # Adjust WHERE clause based on search_type
        if search_type == 'title':
            where_clause = "title LIKE ?"
            search_param = (f'%{query}%',)
        elif search_type == 'attribution':
            where_clause = "attribution LIKE ?"
            search_param = (f'%{query}%',)
        elif search_type == 'displaydate':
            where_clause = "displaydate LIKE ?"
            search_param = (f'%{query}%',)
        else:
                where_clause = "title LIKE ?"
                search_param = (f'%{query}%',) # (f'%{"Query Error"}%',)

        # Add art_type filter if not 'all'
        if art_type != 'all':
            where_clause += " AND classification = ?"
            search_param += (art_type,)

        # Get total count
        count_query = f"SELECT COUNT(*) FROM objects WHERE {where_clause}"
        c.execute(count_query, search_param)
        total = c.fetchone()[0]

        # Get paginated results
        offset = (page - 1) * per_page
        full_query = base_query + where_clause + " LIMIT ? OFFSET ?"
        c.execute(full_query, search_param + (per_page, offset))
        results = c.fetchall()
        
        # Convert results to a list of dictionaries
        results_list = generate_result_list(results)

        return jsonify({
            'results': results_list,
            'has_more': total > (page * per_page),
            'total': total
        })
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return render_template('search.html', error="Database error occurred", project_name=project_name, display_name=display_name)
    finally:
        if conn:
            conn.close()