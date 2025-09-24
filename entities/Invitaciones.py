import mysql.connector
from config.db_config import DB_CONFIG # Asegúrate de que la ruta sea correcta

class Invitacion:
    def __init__(self, id, usuario_id, correo_invitado, rol_destino, token, estado, creado_en):
        self.id = id
        self.usuario_id = usuario_id
        self.correo_invitado = correo_invitado
        self.rol_destino = rol_destino
        self.token = token
        self.estado = estado
        self.creado_en = creado_en

    def to_dict(self):
        """Convierte el objeto Juego a un diccionario para fácil serialización (ej. a JSON)."""
        return {
            "id": self.id,
            "nousuario_idmbre": self.usuario_id,
            "correo_invitado": self.correo_invitado,
            "rol_destino": self.rol_destino,
            "token": self.token,
            "estado": self.estado,
            "creado_en": self.creado_en
        }

def get_db_connection():
    """Establece y retorna una conexión a la base de datos."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None