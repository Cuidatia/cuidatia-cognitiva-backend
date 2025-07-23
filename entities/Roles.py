import mysql.connector
from config.db_config import DB_CONFIG

class Rol:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre
        }

def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None
