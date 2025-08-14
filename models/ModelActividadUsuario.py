from entities.ActividadUsuario import Actividad
class ModelActividadUsuario:

    @classmethod
    def registrar_evento(cls, mysql, usuario_id, tipo_evento, descripcion, tiempo): #, usuario_correo
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("""
                INSERT INTO actividad_usuario (usuario_id, tipo_evento, descripcion, fecha, tiempo_segundos)
                VALUES (%s, %s, %s, NOW(), %s)
            """, 
            (usuario_id, tipo_evento, descripcion, tiempo)
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
                SELECT au.*, u.nombre FROM actividad_usuario au INNER JOIN usuarios u WHERE u.id = au.usuario_id ORDER BY au.fecha DESC;
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
                    "tiempo_segundos": row[5],
                    "nombre_usuario": row[6]
                }
                actividades.append(actividad)
            return actividades

        except Exception as e:
            print("Error en obtener_actividad_reciente:", e)
            return []

        finally:
            cursor.close()
            con.close()
      
    @classmethod
    def obtener_por_usuario(cls, mysql, usuario_id):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("""
                SELECT tipo_evento, descripcion, fecha
                FROM actividad_usuario
                WHERE usuario_id = %s
                ORDER BY fecha DESC
            """, (usuario_id,))
            rows = cursor.fetchall()
            actividades = []
            for row in rows:
                fecha_formateada = row[2].strftime('%Y-%m-%d %H:%M') if row[2] else None
                actividad = {
                    "tipo_evento": row[0],
                    "descripcion": row[1],
                    "fecha": fecha_formateada,
                } 
                actividades.append(actividad)
            return actividades
        except Exception as e:
            print("Error al obtener actividad del usuario:", e)
            return []
            
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