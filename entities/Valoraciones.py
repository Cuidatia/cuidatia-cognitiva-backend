import mysql.connector
from config.db_config import DB_CONFIG # Asegúrate de que la ruta sea correcta

class Valoracion:
    def __init__(self, id, id_usuario, puntuacion, comentario, fecha, es_destacada, editada):
        self.id = id
        self.id_usuario = id_usuario
        self.puntuacion = puntuacion
        self.comentario = comentario
        self.fecha = fecha
        self.es_destacada = es_destacada
        self.editada = editada

    def to_dict(self):
        return {
            "id": self.id,
            "id_usuario": self.id_usuario,
            "puntuacion": self.puntuacion,
            "comentario": self.comentario,
            "fecha": self.fecha,
            "es_destacada": self.es_destacada,
            "editada": self.editada
        }

def get_db_connection():
    """Establece y retorna una conexión a la base de datos."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None