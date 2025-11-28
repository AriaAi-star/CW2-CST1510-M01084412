import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parents[1] / 'DATA' / 'inteligent_platform.db'


def connect_database():
	"""Return a new SQLite connection to the project database."""
	# Ensure parent directory exists and use the repository DATA path
	return sqlite3.connect(str(DB_PATH))


# Backwards-compatible global connection (kept for scripts that import `conn`)
try:
	conn = connect_database()
except Exception:
	conn = None