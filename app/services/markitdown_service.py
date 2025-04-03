# /app/services/markitdown_service.py
from markitdown import MarkItDown

def convert_file_to_markdown(file_path, enable_plugins=False):
    """
    Converts the given file to markdown using MarkItDown.
    
    :param file_path: Path to the file to be converted.
    :param enable_plugins: Boolean to control plugin usage.
    :return: Extracted markdown text.
    """
    md = MarkItDown(enable_plugins=enable_plugins)
    result = md.convert(file_path)
    return result.text_content
