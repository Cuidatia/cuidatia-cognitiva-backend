import mysql.connector
from config.db_config import DB_CONFIG

class NivelJuego:
    def __init__(self, id, dificultad_textual, experiencia_otorgada):
        self.id = id
        self.dificultad_textual = dificultad_textual
        self.experiencia_otorgada = experiencia_otorgada

    def to_dict(self):
        return {
            "id": self.id,
            "dificultad_textual": self.dificultad_textual,
            "experiencia_otorgada": self.experiencia_otorgada
        }

def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None