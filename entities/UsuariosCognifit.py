import mysql.connector
from config.db_config import DB_CONFIG


class UsuarioCognifit:
    def __init__(self, id, usuario_id, cognifit_email, cognifit_user_token, fecha_creacion, fecha_actualizacion):
        self.id = id
        self.usuario_id = usuario_id
        self.cognifit_email = cognifit_email
        self.cognifit_user_token = cognifit_user_token
        self.fecha_creacion = fecha_creacion
        self.fecha_actualizacion = fecha_actualizacion

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "cognifit_email": self.cognifit_email,
            "cognifit_user_token": self.cognifit_user_token,  # Considera omitirlo o enmascararlo si es sensible
            "fecha_creacion": self.fecha_creacion,
            "fecha_actualizacion": self.fecha_actualizacion
        }


def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None