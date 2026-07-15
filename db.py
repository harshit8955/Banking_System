import os
import mysql.connector

conn = mysql.connector.connect(
    host=os.environ.get("DB_HOST", "localhost"),
    user=os.environ.get("DB_USER", "root"),
    password=os.environ.get("DB_PASSWORD", "Harshit#8955"),
    database=os.environ.get("DB_NAME", "banking_db")
)

cursor = conn.cursor(dictionary=True)


def ensure_connection():
    """Reconnect if the MySQL connection has timed out."""
    conn.ping(reconnect=True)