import mysql.connector
from app.config import DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME

def get_db_connection():
    try:
        mydb = mysql.connector.connect(
            host=DATABASE_HOST,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            database=DATABASE_NAME
        )
        return mydb
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None