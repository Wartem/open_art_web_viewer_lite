import os
from flask import Blueprint, render_template, current_app, request, jsonify
import sqlite3
from typing import List, Dict, Any, Optional
from functools import lru_cache

project_dir = os.path.dirname(__file__)
project_name = os.path.basename(project_dir)

bp = Blueprint(
    project_name, __name__, template_folder=os.path.join(project_dir, "templates")
)

SOURCE_TRANS = {
    "NGA": "National Gallery of Art",
    "MM": "The Metropolitan Museum of Art",
}

VALID_SEARCH_TYPES = {"title", "attribution", "displaydate"}
VALID_ART_TYPES = {
    "all", "Print", "Index of American Design", "Drawing", "Photograph", "Painting",
    "Sculpture", "Volume", "Decorative Art", "Portfolio", "Technical Material",
    "Time Based Media Art",
}

def get_db_connection():
    return sqlite3.connect(current_app.config["SQLITE_DB_PATH"])

def execute_db_query(query: str, params: tuple) -> List[tuple]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

def get_search_params(request):
    return (
        request.args.get("query", ""),
        request.args.get("search_type", "title"),
        request.args.get("art_type", "all")
    )

def construct_where_clause(search_type: str, art_type: str) -> tuple:
    where_clause = f"{search_type} LIKE ?" if search_type in VALID_SEARCH_TYPES else "title LIKE ?"
    params = [f"%{request.args.get('query', '')}%"]
    
    if art_type != "all" and art_type in VALID_ART_TYPES:
        where_clause += " AND classification = ?"
        params.append(art_type)
    
    return where_clause, tuple(params)

@lru_cache(maxsize=128)
def get_project_info():
    return (
        current_app.config.get("project_name", "Open Art Web Viewer"),
        current_app.config.get("display_name", current_app.config.get("project_name", "Open Art Web Viewer"))
    )

def clean_string(s: Optional[str]) -> str:
    if not isinstance(s, str):
        return str(s).strip()
    return s.replace("undefined", "null").replace('"', "").strip()

def generate_result_list(results: List[tuple]) -> List[Dict[str, Any]]:
    return [
        {
            "source": clean_string(SOURCE_TRANS.get(r[0], r[0])),
            "objectid": clean_string(r[1]),
            "title": clean_string(r[2]),
            "attribution": clean_string(r[3]),
            "beginyear": clean_string(r[4]),
            "endyear": clean_string(r[5]),
            "displaydate": clean_string(r[6]),
            "classification": clean_string(r[7]),
            "medium": clean_string(r[8]),
            "width": clean_string(r[9]),
            "height": clean_string(r[10]),
            "imgurl_thumb": clean_string(r[11]),
            "imgurl_downsized": clean_string(r[12]),
            "imgurl_full": clean_string(r[13]),
        }
        for r in results if r and len(r) >= 14
    ]

@bp.route("/", methods=["GET", "POST"])
def index():
    project_name, display_name = get_project_info()
    return render_template(
        "search.html", project_name=project_name, display_name=display_name
    )

@bp.route("/search", methods=["GET", "POST"])
def search():
    project_name, display_name = get_project_info()
    query, search_type, art_type = get_search_params(request)
    page = request.args.get("page", 1, type=int)
    per_page = 12

    if not query:
        return render_template(
            "search.html",
            results=[],
            total=0,
            project_name=project_name,
            display_name=display_name,
            query=query,
            search_type=search_type,
            art_type=art_type,
            page=page,
            per_page=per_page,
        )

    try:
        where_clause, search_param = construct_where_clause(search_type, art_type)
        count_query = f"SELECT COUNT(*) FROM objects WHERE {where_clause}"
        total = execute_db_query(count_query, search_param)[0][0]

        offset = (page - 1) * per_page
        results_query = f"""
            SELECT source, objectid, title, attribution, beginyear, endyear, displaydate, 
                   classification, medium, width, height, imgurl_thumb, imgurl_downsized, imgurl_full
            FROM objects 
            WHERE {where_clause}
            LIMIT ? OFFSET ?
        """
        results = execute_db_query(results_query, search_param + (per_page, offset))
        results_list = generate_result_list(results)

        return render_template(
            "search.html",
            results=results_list,
            query=query,
            search_type=search_type,
            art_type=art_type,
            page=page,
            per_page=per_page,
            total=total,
            project_name=project_name,
            display_name=display_name,
        )

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return render_template(
            "search.html",
            error="Database error occurred",
            project_name=project_name,
            display_name=display_name,
        )

@bp.route("/api/search", methods=["GET"])
def api_search():
    query, search_type, art_type = get_search_params(request)
    page = request.args.get("page", 1, type=int)
    per_page = 12

    try:
        where_clause, search_param = construct_where_clause(search_type, art_type)
        count_query = f"SELECT COUNT(*) FROM objects WHERE {where_clause}"
        total = execute_db_query(count_query, search_param)[0][0]

        offset = (page - 1) * per_page
        results_query = f"""
            SELECT source, objectid, title, attribution, beginyear, endyear, displaydate,
                classification, medium, width, height, imgurl_thumb, imgurl_downsized, imgurl_full
            FROM objects 
            WHERE {where_clause}
            LIMIT ? OFFSET ?
        """
        results = execute_db_query(results_query, search_param + (per_page, offset))
        results_list = generate_result_list(results)

        return jsonify({
            "results": results_list,
            "has_more": total > (page * per_page),
            "total": total,
        })

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return jsonify({"error": "Database error occurred"}), 500