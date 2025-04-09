from fastapi import HTTPException, UploadFile
from typing import Optional, List
import os
import requests
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import sql
from .config import STORAGE_FOLDER, DATABASE_URL, API_KEY
import json


###############################################################################
# BROWSE SERVICES
###############################################################################
def get_files_from_db():
    # ... your logic for listing from the database
    # e.g., read from intel_L100_files table and return a list
    # something like:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM intel_l100_files") 
    files = cur.fetchall()
    ...
    return {"files": files}

def list_files_service():
    """
    Return a list of files in the storage folder.
    """
    if not os.path.exists(STORAGE_FOLDER):
        return {"files": []}
    files = [
        f for f in os.listdir(STORAGE_FOLDER)
        if os.path.isfile(os.path.join(STORAGE_FOLDER, f))
    ]
    return {"files": files}

def download_file_service(filename: str):
    """
    Return a FileResponse for downloading a file by its name.
    (Note: Usually you'd return fastapi.responses.FileResponse here,
    but if you're doing it from the router, you can do that in the router function.)
    """
    file_path = os.path.join(STORAGE_FOLDER, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return file_path  # Let the router wrap this in FileResponse

def get_file_details_service(file_id: int):
    """
    Retrieve a single file record by its file_id from the intel_l100_files table.
    """
    import psycopg2
    from psycopg2.extras import RealDictCursor
    from fastapi import HTTPException
    from .config import DATABASE_URL

    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM intel_l100_files WHERE file_id = %s", (file_id,))
            file_record = cur.fetchone()
            if not file_record:
                raise HTTPException(status_code=404, detail="File not found")
            return file_record
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()
###############################################################################
# UPLOAD SERVICES
###############################################################################
def process_upload_service(file: UploadFile):
    """
    Handle uploading file, saving it, converting to markdown, updating DB.
    """
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    # We do an async read here, but let's simplify to synchronous for demonstration.
    # If you prefer the fully async read, you can handle that in the router itself.
    try:
        original_filename = file.filename
        _, ext = os.path.splitext(original_filename)

        create_user = "test_user"  # or from token in real usage
        status = "uploaded"

        # Insert a new record to get the file_id
        file_id = insert_file_record(create_user, original_filename, status)
        new_filename = f"{file_id}{ext}"
        new_file_path = os.path.join(STORAGE_FOLDER, new_filename)

        # Ensure storage folder exists
        os.makedirs(STORAGE_FOLDER, exist_ok=True)

        # Save the file to disk
        content = file.file.read()  # Synchronous read
        with open(new_file_path, "wb") as f:
            f.write(content)

        # Convert to markdown
        markdown_content = convert_file_to_markdown(new_file_path)

        # Update the DB record
        update_file_record(file_id, new_filename, markdown_content)

        return {
            "record_id": file_id,
            "allocated_filename": new_filename,
            "markdown": markdown_content
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing upload: {e}")

###############################################################################
# HELPER FUNCTIONS FOR UPLOAD SERVICE
###############################################################################
def convert_file_to_markdown(file_path: str, enable_plugins: bool = False) -> str:
    """
    Convert a file to Markdown using MarkItDown or any library you like.
    """
    from markitdown import MarkItDown
    md = MarkItDown(enable_plugins=enable_plugins)
    result = md.convert(file_path)
    return result.text_content

def insert_file_record(create_user, uploaded_file_name, status):
    """
    Insert a record into intel_L100_files table.
    """
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO intel_L100_files (create_user, uploaded_file_name, file_name, status)
                VALUES (%s, %s, %s, %s)
                RETURNING file_id;
            """, (create_user, uploaded_file_name, "placeholder", status))
            file_id = cur.fetchone()[0]
        conn.commit()
        return file_id
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

def update_file_record(file_id, file_name, markdown_extract):
    """
    Update the file record with the allocated file name and markdown content.
    """
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE intel_L100_files
                SET file_name = %s,
                    markdown_extract = %s,
                    metad_create_date = CURRENT_TIMESTAMP,
                    metad_edit_date = CURRENT_TIMESTAMP
                WHERE file_id = %s;
            """, (file_name, markdown_extract, file_id))
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

def update_file_record_scrape(file_id: int, scraped_data: dict):
    """
    Update the intel_l100_files record with scraped metadata data.
    
    Parameters:
      file_id (int): The unique identifier of the file record.
      scraped_data (dict): A dictionary containing the following keys:
          - "document_title" (mapped to the title column)
          - "document_author" (mapped to the author column)
          - "document_version" (mapped to the version column)
          - "document_description" (mapped to the file_description column)
    
    The function updates the record's title, author, version, and file_description,
    and sets the metad_edit_date to the current timestamp.
    """
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE intel_l100_files
                SET title = %s,
                    author = %s,
                    version = %s,
                    file_description = %s,
                    metad_edit_date = CURRENT_TIMESTAMP
                WHERE file_id = %s;
            """, (
                scraped_data.get("document_title", ""),
                scraped_data.get("document_author", ""),
                scraped_data.get("document_version", ""),
                scraped_data.get("document_description", ""),
                file_id
            ))
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

def scrape_metadata_service(file_id: int):
    """
    Retrieve a file record by file_id, then perform a simple scraping action.
    For demonstration, we open the file and read its first 100 characters as a "preview".
    You can replace the logic below with more advanced scraping as needed.
    """
    # Get file details from the DB; this will also raise a 404 if not found.
    file_details = get_file_details_service(file_id)
    markdown_extract = file_details["markdown_extract"]
    prompt = 'Return only JSON based on information contained withing this: '+markdown_extract
    scraped_data = query_llm_tool(prompt)

    update_file_record_scrape(file_id=file_id, scraped_data=scraped_data)

    
###############################################################################
# LLM SERVICE
###############################################################################


def query_llm_service(prompt: Optional[str] = None, messages: Optional[List[dict]] = None):
    """
    Send a request to your LLM backend and return the JSON response.
    """
    url_str = "https://dlpi-ai-api.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2025-01-01-preview"
    
    if not prompt and not messages:
        raise HTTPException(status_code=400, detail="No prompt or messages provided")
    final_messages = messages if messages else [{"role": "user", "content": prompt}]
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY
    }
    payload = {
        "messages": final_messages,
        "max_tokens": 1000,
        "temperature": 0.7
    }
    try:
        response = requests.post(url_str, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"LLM request failed: {str(e)}")


def query_llm_tool(prompt: Optional[str] = None, messages: Optional[List[dict]] = None):
    """
    Send a request to your LLM backend and return structured JSON using tool calling.
    Ensures the JSON matches: {"document_title": "","document_author": "","document_version": "","document_description": ""}
    """
    url_str = "https://dlpi-ai-api.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2025-01-01-preview"

    if not prompt and not messages:
        raise HTTPException(status_code=400, detail="No prompt or messages provided")
    
    final_messages = messages if messages else [{"role": "user", "content": prompt}]
    
    tools = [
        {
            "type": "function",
            "function": {
                "name": "generate_document_metadata",
                "description": "Generate structured metadata for a document.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "document_title": { "type": "string" },
                        "document_author": { "type": "string" },
                        "document_version": { "type": "string" },
                        "document_description": { "type": "string" }
                    },
                    "required": ["document_title", "document_author", "document_version", "document_description"]
                }
            }
        }
    ]

    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY
    }

    payload = {
        "messages": final_messages,
        "tools": tools,
        "tool_choice": {
            "type": "function",
            "function": { "name": "generate_document_metadata" }
        },
        "max_tokens": 1000,
        "temperature": 0.0  # Keep it deterministic for clean JSON
    }

    try:
        response = requests.post(url_str, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Parse the JSON from tool_calls
        tool_calls = data["choices"][0]["message"].get("tool_calls", [])
        if tool_calls:
            function_args = tool_calls[0]["function"].get("arguments", "{}")
            return json.loads(function_args)  # clean parsed JSON
        else:
            raise HTTPException(status_code=500, detail="No tool call returned from model.")

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"LLM request failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


def get_llm_response_text(prompt: str) -> str:
    """
    Calls the query_llm_service with a given prompt and returns the text content.
    Returns an empty string if the response is missing or malformed.
    """
    if not prompt:
        # You could choose to raise an exception here, but returning empty is also possible.
        return ""
    
    response = query_llm_service(prompt=prompt)
    try:
        text_content = response["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        # If the JSON structure isn't as expected, return an empty string
        return ""
    
    # If the content is None or an empty string, return "" instead
    return text_content or ""


###############################################################################
# DB EXPLORER SERVICES
###############################################################################
def list_tables_service():
    """
    Return a list of table names from the public schema.
    """
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
        """)
        tables = [row["table_name"] for row in cur.fetchall()]
        cur.close()
        return {"tables": tables}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()

def get_table_snapshot_service(table_name: str):
    """
    Return columns and up to 10 rows from a named table.
    """
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # Validate table
        cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public' AND table_name = %s;
        """, (table_name,))
        if not cur.fetchone():
            raise HTTPException(status_code=404, detail="Table not found")

        query = sql.SQL("SELECT * FROM {} LIMIT 10;").format(sql.Identifier(table_name))
        cur.execute(query)
        records = cur.fetchall()

        columns = [desc.name for desc in cur.description] if cur.description else []
        cur.close()

        return {"columns": columns, "records": records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()
