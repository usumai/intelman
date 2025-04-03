# /app/endpoints/dbexplorer.py
from flask import Blueprint, render_template, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from config import DATABASE_URL

dbexplorer_bp = Blueprint('dbexplorer', __name__, url_prefix='/dbexplorer')

@dbexplorer_bp.route('/')
def explorer():
    conn = None
    try:
        # Connect using the connection string from your configuration
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Query the "users" table
        cur.execute("SELECT * FROM users;")
        users = cur.fetchall()
        
        # Query the "posts" table
        cur.execute("SELECT * FROM posts;")
        posts = cur.fetchall()
        
        cur.close()
    except Exception as e:
        current_app.logger.error(f"Database query failed: {e}")
        users = []
        posts = []
    finally:
        if conn:
            conn.close()
    
    return render_template('dbexplorer.html', users=users, posts=posts)
