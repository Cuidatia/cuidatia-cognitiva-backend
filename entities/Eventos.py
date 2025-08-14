import mysql.connector
from config.db_config import DB_CONFIG

class Evento:
    def __init__(self, id, nombre, descripcion, categoria, plazas_ocupadas, plazas_totales, imagen, ubicacion, localidad, fecha_evento, activo, momento_insercion):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.categoria = categoria
        self.plazas_ocupadas = plazas_ocupadas
        self.plazas_totales = plazas_totales
        self.imagen = imagen
        self.ubicacion = ubicacion
        self.localidad = localidad
        self.fecha_evento = fecha_evento
        self.activo = activo
        self.momento_insercion = momento_insercion

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "categoria": self.categoria,
            "plazas_ocupadas": self.plazas_ocupadas,
            "plazas_totales": self.plazas_totales,
            "imagen": self.imagen,
            "ubicacion": self.ubicacion,
            "localidad": self.localidad,
            "fecha_evento": self.fecha_evento,
            "activo":self.activo,
            "momento_insercion": self.momento_insercion
        }

def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None