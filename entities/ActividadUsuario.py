import mysql.connector
from config.db_config import DB_CONFIG # Asegúrate de que la ruta sea correcta

class Actividad:
    def __init__(self, id, usuario_id, tipo_evento, description, fecha):
        self.id = id
        self.usuario_id = usuario_id
        self.tipo_evento = tipo_evento
        self.description = description
        self.fecha = fecha

    def to_dict(self):
        """Convierte el objeto Juego a un diccionario para fácil serialización (ej. a JSON)."""
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "tipo_evento": self.tipo_evento,
            "description": self.description,
            "fecha": self.fecha,
        }

def get_db_connection():
    """Establece y retorna una conexión a la base de datos."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None