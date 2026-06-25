# models/ModelUsuariosCognifit.py

import requests as http_requests
from entities.UsuariosCognifit import UsuarioCognifit

COGNIFIT_CLIENT_ID = "3f3ef3ef95b485601432890dc61ef669"
COGNIFIT_CLIENT_SECRET = "e72215e742af8533b0a469d4c1e7f764"

class ModelUsuariosCognifit:

    @staticmethod
    def registrar_en_cognifit(mysql, usuario_id, nombre, apellido, email, password, fecha_nacimiento, sexo=1, locale="es"):
        """
        Registra un usuario en CogniFit y guarda el token en la BD.
        Devuelve el objeto UsuarioCognifit creado o un dict con 'error'.
        """
        # 1. Llamar a la API de CogniFit
        try:
            response = http_requests.post(
                'https://api.cognifit.com/registration',
                json={
                    "client_id": COGNIFIT_CLIENT_ID,
                    "client_secret": COGNIFIT_CLIENT_SECRET,
                    "user_name": nombre,
                    "user_lastname": apellido,
                    "user_email": email,
                    "user_password": password,
                    "user_birthday": fecha_nacimiento,
                    "user_sex": sexo,
                    "user_locale": locale
                }
            )
            data = response.json()
        except Exception as e:
            print("Error al conectar con CogniFit:", e)
            return {"error": f"Error al conectar con CogniFit: {str(e)}"}

        if response.status_code != 200 or "user_token" not in data:
            print("Error de CogniFit:", data)
            return {"error": "CogniFit no devolvió un token válido", "detalle": data}

        user_token = data["user_token"]

        # 2. Guardar en la BD
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("""
                INSERT INTO usuarios_cognifit (usuario_id, cognifit_email, cognifit_user_token)
                VALUES (%s, %s, %s)
            """, (usuario_id, email, user_token))
            con.commit()

            nuevo_id = cursor.lastrowid

            # 3. Devolver la entidad completa
            cursor.execute("SELECT * FROM usuarios_cognifit WHERE id = %s", (nuevo_id,))
            row = cursor.fetchone()
            if row:
                return UsuarioCognifit(*row)
            return {"error": "No se pudo recuperar el registro creado"}

        except Exception as e:
            con.rollback()
            print("Error al guardar en usuarios_cognifit:", e)
            return {"error": str(e)}
        finally:
            cursor.close()
            con.close()

    @staticmethod
    def obtener_por_usuario_id(mysql, usuario_id):
        """
        Devuelve el registro de CogniFit asociado a un usuario, o None si no existe.
        """
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("""
                SELECT * FROM usuarios_cognifit WHERE usuario_id = %s
            """, (usuario_id,))
            row = cursor.fetchone()
            if row:
                return UsuarioCognifit(*row)
            return None
        except Exception as e:
            print("Error al obtener usuarios_cognifit:", e)
            return {"error": str(e)}
        finally:
            cursor.close()
            con.close()

    @staticmethod
    def eliminar_por_usuario_id(mysql, usuario_id):
        """
        Elimina el registro de CogniFit asociado a un usuario.
        Devuelve True si se eliminó, False si no.
        """
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("""
                DELETE FROM usuarios_cognifit WHERE usuario_id = %s
            """, (usuario_id,))
            con.commit()
            return cursor.rowcount > 0
        except Exception as e:
            con.rollback()
            print("Error al eliminar usuarios_cognifit:", e)
            return False
        finally:
            cursor.close()
            con.close()

    @staticmethod
    def tiene_cuenta_cognifit(mysql, usuario_id):
        """
        Comprueba si un usuario ya tiene cuenta en CogniFit.
        Devuelve True o False.
        """
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("""
                SELECT id FROM usuarios_cognifit WHERE usuario_id = %s
            """, (usuario_id,))
            return cursor.fetchone() is not None
        except Exception as e:
            print("Error en tiene_cuenta_cognifit:", e)
            return False
        finally:
            cursor.close()
            con.close()