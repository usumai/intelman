# app/services/markitdown_service.py
from markitdown import MarkItDown

def convert_file_to_markdown(file_path, enable_plugins=False):
    md = MarkItDown(enable_plugins=enable_plugins)
    result = md.convert(file_path)
    return result.text_content
