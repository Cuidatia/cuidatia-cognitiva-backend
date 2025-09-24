import mysql.connector
from config.db_config import DB_CONFIG # Asegúrate de que la ruta sea correcta

class VinculoUsuario:
    def __init__(self, id, paciente_id, supervisor_id, tipo_vinculo, fecha_vinculo):
        self.id = id
        self.paciente_id = paciente_id
        self.supervisor_id = supervisor_id
        self.tipo_vinculo = tipo_vinculo
        self.fecha_vinculo = fecha_vinculo

    def to_dict(self):
        return {
            "id": self.id,
            "paciente_id": self.paciente_id,
            "supervisor_id": self.supervisor_id,
            "tipo_vinculo": self.tipo_vinculo,
            "fecha_vinculo": self.fecha_vinculo
        }

def get_db_connection():
    """Establece y retorna una conexión a la base de datos."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None