# /app/services/file_database_service.py
import psycopg2
from config import DATABASE_URL

def get_connection():
    """Return a new database connection."""
    return psycopg2.connect(DATABASE_URL)

def insert_file_record(create_user, uploaded_file_name, status):
    """
    Inserts a new record in the intel_L100_files table.
    Returns the generated file_id.
    """
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO intel_L100_files (create_user, uploaded_file_name, file_name, status)
            VALUES (%s, %s, %s, %s)
            RETURNING file_id;
        """, (create_user, uploaded_file_name, "placeholder", status))
        file_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
    return file_id

def update_file_record(file_id, file_name, markdown_extract):
    """
    Updates the file record with the allocated filename, markdown content, 
    and metadata timestamps.
    """
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE intel_L100_files
            SET file_name = %s,
                markdown_extract = %s,
                metad_create_date = CURRENT_TIMESTAMP,
                metad_edit_date = CURRENT_TIMESTAMP
            WHERE file_id = %s;
        """, (file_name, markdown_extract, file_id))
        conn.commit()
        cur.close()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
