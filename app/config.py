import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
STORAGE_FOLDER = os.path.join(BASE_DIR, 'storage')
# DATABASE_URL = os.environ.get('DATABASE_URL', f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

# New entries for authentication.
SECRET_KEY = "your_secret_key_here" 
API_KEY = ""

DB_NAME = "postgres"
DB_USER = "dlpi"
DB_PASS = ""
DB_URL  = "intelmandb.postgres.database.azure.com"
SSLMODE = "require"
DATABASE_URL = os.environ.get(
    'DATABASE_URL',
    f"postgresql://{DB_USER}:{DB_PASS}@{DB_URL}:5432/{DB_NAME}?sslmode={SSLMODE}"
)