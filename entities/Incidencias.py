import mysql.connector
from config.db_config import DB_CONFIG # Asegúrate de que la ruta sea correcta

class Incidencia:
    def __init__(self, id, nombre, email, tipo, mensaje, fecha, resuelta):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.tipo = tipo
        self.mensaje = mensaje
        self.fecha = fecha
        self.resuelta = resuelta

    def to_dict(self):
        """Convierte el objeto Juego a un diccionario para fácil serialización (ej. a JSON)."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "tipo": self.tipo,
            "mensaje": self.mensaje,
            "fecha": self.fecha,
            "resuelta": self.resuelta
        }

def get_db_connection():
    """Establece y retorna una conexión a la base de datos."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None