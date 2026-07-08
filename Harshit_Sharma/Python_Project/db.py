import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Harshit#8955",
    database="banking_db"
)

cursor = conn.cursor(dictionary=True)