# /app/routers/file.py
from fastapi import APIRouter, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
from ..config import DATABASE_URL

router = APIRouter(tags=["file"])

@router.get("/{file_id}")
def get_file_details(file_id: int):
    """
    Retrieve detailed information for a file record from the database.
    Expected columns might include:
      - file_id
      - create_user
      - uploaded_file_name
      - file_name (the renamed file stored on disk)
      - status
      - markdown_extract
      - metad_create_date
      - metad_edit_date
    """
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM intel_L100_files WHERE file_id = %s", (file_id,))
        file_record = cur.fetchone()
        cur.close()
        if not file_record:
            raise HTTPException(status_code=404, detail="File record not found")
        return file_record
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()
