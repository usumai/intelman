from fastapi import APIRouter, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import sql
from ..config import DATABASE_URL

router = APIRouter(tags=["dbexplorer"])

@router.get("/tables")
def list_tables():
    """
    Return a list of table names from the public schema.
    """
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
            """
        )
        tables = [row["table_name"] for row in cur.fetchall()]
        cur.close()
        return {"tables": tables}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()


@router.get("/table/{table_name}")
def get_table_snapshot(table_name: str):
    """
    Returns a snapshot of a given table. The response contains:
      - "columns": list of column names,
      - "records": up to 10 rows of data from the table.
    """
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # Validate that the table exists in the public schema.
        cur.execute(
            """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = %s;
            """,
            (table_name,),
        )
        if not cur.fetchone():
            raise HTTPException(status_code=404, detail="Table not found")

        # Build a safe query using psycopg2.sql to avoid SQL injection.
        query = sql.SQL("SELECT * FROM {} LIMIT 10;").format(sql.Identifier(table_name))
        cur.execute(query)
        records = cur.fetchall()

        # Extract column names from the cursor description.
        columns = [desc.name for desc in cur.description] if cur.description else []
        cur.close()

        return {"columns": columns, "records": records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()
