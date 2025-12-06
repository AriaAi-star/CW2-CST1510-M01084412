#aim of this file is to connect our code to sqlite database



#sqlite is a python library to work with databases 
import sqlite3
from pathlib import Path



#we are using path to manage file paths
DB_PATH = Path(__file__).resolve().parents[1] / 'DATA' / 'inteligent_platform.db'


def connect_database():
	"""Return a new SQLite connection to the project database."""
	#Use the repository DATA path and make sure the parent directory is present.
	return sqlite3.connect(str(DB_PATH))

#global connection 
try:
	conn = connect_database()
except Exception:
	conn = None