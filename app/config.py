import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
STORAGE_FOLDER = os.path.join(BASE_DIR, 'storage')
DATABASE_URL = os.environ.get('DATABASE_URL', f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

# New entries for authentication.
SECRET_KEY = "your_secret_key_here"  # Remember to use a secure key in production.
ALGORITHM = "HS256"