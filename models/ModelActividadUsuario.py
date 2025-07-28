from entities.ActividadUsuario import Actividad
class ModelActividadUsuario:

    @classmethod
    def registrar_evento(cls, mysql, usuario_id, tipo_evento, descripcion, usuario_email):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("""
                SELECT id FROM usuarios WHERE correo = %s"""
            , (usuario_email,))
            
            usuario = cursor.fetchone()
            
            if not usuario:
                return {"error": "Usuario no encontrado"}, 404

            usuario_id = usuario[0]
            
            cursor.execute("""
                INSERT INTO actividad_usuario (usuario_id, tipo_evento, descripcion, fecha)
                VALUES (%s, %s, %s, NOW())
            """, 
            (usuario_id, tipo_evento, descripcion)
            )
            con.commit()
            return {"mensaje": "Actividad registrada"}
        
        except Exception as e:
            print("Error en registrar_evento:", e)
            return {"error": str(e)}
        finally:
            cursor.close()
            con.close()
            
    @classmethod
    def obtener_actividad_reciente(cls, mysql):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("""
                SELECT au.id, au.usuario_id, au.tipo_evento, au.descripcion, au.fecha, u.nombre AS nombre_usuario
                FROM actividad_usuario au
                JOIN usuarios u ON au.usuario_id = u.id
                ORDER BY au.fecha DESC
            """)
            rows = cursor.fetchall()
            actividades = []
            for row in rows:
                fecha_formateada = row[4].strftime('%Y-%m-%d %H:%M') if row[4] else None
                actividad = {
                    "id": row[0],
                    "usuario_id": row[1],
                    "tipo_evento": row[2],
                    "descripcion": row[3],
                    "fecha": fecha_formateada,
                    "nombre_usuario": row[5],
                }
                actividades.append(actividad)
            return actividades

        except Exception as e:
            print("Error en obtener_actividad_reciente:", e)
            return []

        finally:
            cursor.close()
            con.close()
            
    # @classmethod
    # def obtener_actividad_reciente_usuario(cls, mysql):
    #     con = mysql.connect()
    #     cursor = con.cursor(dictionary=True)
    #     try:
    #         cursor.execute("""
    #             SELECT au.*, u.nombre AS nombre_usuario
    #             FROM actividad_usuario au
    #             JOIN usuarios u ON au.usuario_id = u.id
    #             ORDER BY au.fecha DESC
    #             LIMIT 30 WHEN u.id=%s
    #         """)
    #         return cursor.fetchall()
    #     except Exception as e:
    #         print("Error en obtener_actividad_reciente:", e)
    #         return []
    #     finally:
    #         cursor.close()
    #         con.close()