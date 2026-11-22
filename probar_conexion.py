import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

conexion = psycopg.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
)
with conexion.cursor() as cur:
    cur.execute("SELECT version();")
    print(cur.fetchone()[0])
conexion.close()