import mysql.connector
from config.db_config import DB_CONFIG

class Chat:
    def __init__(self, id, usuario_id, contenido, fecha, nombre):
        self.id = id
        self.usuario_id = usuario_id
        self.contenido = contenido
        self.fecha = fecha
        self.nombre = nombre

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "mensaje": self.contenido,
            "fecha": self.fecha,
            "usuario": self.nombre or "Anónimo"
        }

def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None