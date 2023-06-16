from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

POSTGRES_URL = os.getenv("POSTGRES_URL")
PGNAME = os.getenv("PGNAME")
PGUSER = os.getenv("PGUSER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
PGHOST = os.getenv("PGHOST")
PGPORT = os.getenv("PGPORT")
