from entities.Invitaciones import Invitacion
import uuid 

class ModelInvitacion:
    @classmethod
    def invitar_usuario(cls, mysql, usuario_id, correo, rol_destino):
        """Insertar invitación (supervisor o médico) en la tabla invitaciones"""
        token = str(uuid.uuid4())
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("""
                INSERT INTO invitaciones (usuario_id, correo_invitado, rol_destino, token)
                VALUES (%s, %s, %s, %s)
            """, (usuario_id, correo, rol_destino, token))
            con.commit()
            return {"message": "Invitación registrada correctamente"}
        except Exception as e:
            print("Error en invitar_usuario:", e)
            return {"error": str(e)}
        finally:
            cursor.close()
            con.close()
            
    @classmethod
    def listar_invitaciones(cls, mysql):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("""
                SELECT i.id, i.correo_invitado, i.rol_destino, i.estado, i.creado_en,
                       u.nombre AS usuario_invitador
                FROM invitaciones i
                LEFT JOIN usuarios u ON i.usuario_id = u.id
                ORDER BY i.creado_en DESC
            """)
            rows = cursor.fetchall()
            columnas = [desc[0] for desc in cursor.description]  # nombres de columnas
            invitaciones = [dict(zip(columnas, row)) for row in rows]  # convertir a dict
            return invitaciones
        except Exception as e:
            print("Error en listar_invitaciones:", e)
            raise e
        finally:
            cursor.close()
            con.close()

    # 📌 Rechazar invitación
    @classmethod
    def rechazar_invitacion(cls, mysql, invitacion_id):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("""
                UPDATE invitaciones
                SET estado = 'rechazada'
                WHERE id = %s AND estado = 'pendiente'
            """, (invitacion_id,))
            con.commit()

            if cursor.rowcount == 0:
                return {"error": "La invitación no existe o ya fue gestionada"}

            return {"message": "Invitación rechazada"}
        except Exception as e:
            return {"error": str(e)}
        finally:
            cursor.close()
            con.close()