from os import getenv
from urllib.parse import urlparse

from dotenv import load_dotenv
import psycopg2

load_dotenv()

host = getenv("HOST")
port = getenv("PORT")
user = getenv("DATABASE_USER")
password = getenv("PASSWORD")
database = getenv("DATABASE")

conn = psycopg2.connect(
    host=host,
    port=port,
    user=user,
    password=password,
    database=database,
)
cur = conn.cursor()

try:
    cur.execute(
        "SELECT 'Hello, Database World!' as message, version() as db_version;"
    )
    result = cur.fetchone()

    if result:
        print("Database connection successful!")
        print(f"Message: {result[0]}")
        print(f"Database version: {result[1]}")
    else:
        print("No results returned from database query")

except Exception as e:
    print(f"Error connecting to database: {e}")

finally:
    cur.close()
    conn.close()
