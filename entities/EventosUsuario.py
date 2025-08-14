import mysql.connector
from config.db_config import DB_CONFIG

class EventosUsuario:
    def __init__(self, id, usuario_id, evento_id, participacion, fecha_inscripcion):
        self.id = id
        self.usuario_id = usuario_id
        self.evento_id = evento_id
        self.participacion = participacion
        self.fecha_inscripcion = fecha_inscripcion

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "evento_id": self.evento_id,
            "participacion": self.participacion,
            "fecha_inscripcion": self.fecha_inscripcion
        }

def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None