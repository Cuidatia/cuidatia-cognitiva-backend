import mysql.connector
from config.db_config import DB_CONFIG # Asegúrate de que la ruta sea correcta
import bcrypt

class Usuario:
    def __init__(self, id, nombre, correo, fecha_nacimiento, contrasena_hash, fecha_registro, id_rol, avatar_url, biografia, ultima_conexion, activo, experiencia, reset_token, reset_token_expira, debe_actualizar_datos):
        self.id = id
        self.nombre = nombre
        self.correo = correo
        self.fecha_nacimiento = fecha_nacimiento
        self.contrasena_hash = contrasena_hash
        self.fecha_registro = fecha_registro
        self.id_rol = id_rol
        self.avatar_url = avatar_url
        self.biografia = biografia
        self.ultima_conexion = ultima_conexion
        self.activo = activo
        self.experiencia = experiencia
        self.reset_token = reset_token
        self.reset_token_expira = reset_token_expira
        self.debe_actualizar_datos = debe_actualizar_datos

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "correo": self.correo,
            "fecha_nacimiento": self.fecha_nacimiento,
            "contrasena_hash": True,
            "fecha_registro": self.fecha_registro,
            "id_rol": self.id_rol,
            "avatar_url": self.avatar_url,
            "biografia": self.biografia,
            "ultima_conexion": self.ultima_conexion,
            "activo": self.activo,
            "experiencia": self.experiencia,
            "reset_token": self.reset_token,
            "reset_token_expira": self.reset_token_expira,
            "debe_actualizar_datos": self.debe_actualizar_datos
        }

def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None

def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))