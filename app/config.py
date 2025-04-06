import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
STORAGE_FOLDER = os.path.join(BASE_DIR, 'storage')
DATABASE_URL = os.environ.get('DATABASE_URL', f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")
