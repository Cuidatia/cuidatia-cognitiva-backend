import mysql.connector
from config.db_config import DB_CONFIG # Asegúrate de que la ruta sea correcta

class Juego:
    def __init__(self, id, nombre, descripcion, imagen, icono, categoria, numero_jugadas, es_destacado, bloqueado, cognifit_key):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.imagen = imagen
        self.icono = icono
        self.categoria = categoria
        self.numero_jugadas = numero_jugadas
        self.es_destacado = es_destacado
        self.bloqueado = bloqueado
        self.cognifit_key = cognifit_key

    def to_dict(self):
        """Convierte el objeto Juego a un diccionario para fácil serialización (ej. a JSON)."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "imagen": self.imagen,
            "icono": self.icono,
            "categoria": self.categoria,
            "numero_jugadas": self.numero_jugadas,
            "es_destacado": self.es_destacado,
            "bloqueado": self.bloqueado,
            "cognifit_key": self.cognifit_key
        }

def get_db_connection():
    """Establece y retorna una conexión a la base de datos."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None