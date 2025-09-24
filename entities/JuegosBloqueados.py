import mysql.connector
from config.db_config import DB_CONFIG # Asegúrate de que la ruta sea correcta

class BloqueoJuego:
    def __init__(self, id, usuario_id, juego_id, activo, motivo, creado_por, created_at, updated_at):
        self.id = id
        self.usuario_id = usuario_id
        self.juego_id = juego_id
        self.activo = activo
        self.motivo = motivo
        self.creado_por = creado_por
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        """Convierte el objeto Juego a un diccionario para fácil serialización (ej. a JSON)."""
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "juego_id": self.juego_id,
            "activo": self.activo,
            "motivo": self.motivo,
            "creado_por": self.creado_por,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

def get_db_connection():
    """Establece y retorna una conexión a la base de datos."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None