import mysql.connector
from config.db_config import DB_CONFIG # Asegúrate de que la ruta sea correcta

class NivelJuegoUsuario:
    def __init__(self, id, usuario_id, nivel_id, juego_id, es_favorito, tiempo_jugado, ultima_conexion):
        self.id = id
        self.usuario_id = usuario_id
        self.nivel_id = nivel_id
        self.juego_id = juego_id
        self.es_favorito = es_favorito
        self.tiempo_jugado = tiempo_jugado
        self.ultima_conexion = ultima_conexion

    def to_dict(self):
        """Convierte el objeto Juego a un diccionario para fácil serialización (ej. a JSON)."""
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "nivel_id": self.nivel_id,
            "juego_id": self.juego_id,
            "es_favorito": self.es_favorito,
            "tiempo_jugado": self.tiempo_jugado,
            "ultima_conexion": self.ultima_conexion
        }

def get_db_connection():
    """Establece y retorna una conexión a la base de datos."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None