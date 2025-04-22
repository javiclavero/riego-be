import mysql.connector
from app.config import DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME

def get_locations_from_db():
    db_conn = None
    try:
        db_conn = mysql.connector.connect(
            host=DATABASE_HOST,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            database=DATABASE_NAME
        )
        cursor = db_conn.cursor(dictionary=True)  # Para obtener resultados como diccionarios
        cursor.execute("SELECT LocId, LocName, LocLatitude, LocLongitude FROM tblLocations")
        locations = cursor.fetchall()
        return locations
    except mysql.connector.Error as err:
        print(f"Error al obtener localizaciones de la base de datos: {err}")
        return None
    finally:
        if db_conn and db_conn.is_connected():
            cursor.close()
            db_conn.close()