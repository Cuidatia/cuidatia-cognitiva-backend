from entities.EventosUsuario import EventosUsuario

class ModelEventosUsuario:
    @classmethod
    def get_all_eventos_usuario(cls, mysql):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("""
                SELECT * FROM eventos_usuario
                ORDER BY fecha_inscripcion DESC
            """)
            rows = cursor.fetchall()
            eventos_usuario = []
            for row in rows:
                fecha_formateada = row[4].strftime('%Y-%m-%d %H:%M') if row[4] else None
                registro = {
                "id": row[0],
                "usuario_id": row[1],
                "evento_id": row[2],
                "participacion": row[3],
                "fecha_inscripcion": fecha_formateada,
                } 
                eventos_usuario.append(registro)
            return eventos_usuario
        except Exception as e:
            print("Error al obtener usuarios inscritos al evento:", e)
            return []
        
    @classmethod
    def registrar_inscripcion(cls, mysql, usuario_id, evento_id, participacion):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("""
                INSERT INTO eventos_usuario (usuario_id, evento_id, participacion, fecha_inscripcion)
                VALUES (%s, %s, %s, NOW())
            """, 
            (usuario_id, evento_id, participacion,))

            cursor.execute("""
                UPDATE eventos SET plazas_ocupadas = plazas_ocupadas + 1 WHERE id = %s
            """, (evento_id,))

            con.commit()
            return {"mensaje": "Inscripcion al evento registrada"}
        
        except Exception as e:
            print("Error en registrar_inscripcion:", e)
            return {"error": str(e)}
        finally:
            cursor.close()
            con.close()

    @classmethod
    def marcar_participacion(cls, mysql, inscripcion_id, participacion):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("""
                UPDATE eventos_usuario SET participacion = %s 
                WHERE id = %s
            """, 
            (participacion, inscripcion_id,))

            con.commit()
            return {"mensaje": "Participacion en el evento marcada"}
        
        except Exception as e:
            print("Error en marcar_participacion:", e)
            return {"error": str(e)}
        finally:
            cursor.close()
            con.close()

    @classmethod
    def eliminar_inscripcion(cls, mysql, usuario_id, evento_id):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("""
                DELETE FROM eventos_usuario WHERE usuario_id = %s AND evento_id = %s
            """, 
            (usuario_id,evento_id,))

            cursor.execute("""
                UPDATE eventos SET plazas_ocupadas = plazas_ocupadas - 1 WHERE id = %s
            """, (evento_id,))
            
            con.commit()
            return {"mensaje": "Inscripcion al evento eliminada"}
        
        except Exception as e:
            print("Error en eliminar_inscripcion:", e)
            return {"error": str(e)}
        finally:
            cursor.close()
            con.close()

    @classmethod
    def obtener_eventos_usuario(cls, mysql, usuario_id):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("""
                SELECT eu.usuario_id, eu.evento_id, eu.participacion, eu.fecha_inscripcion,
                   e.nombre AS nombre_evento, e.ubicacion, e.fecha_evento
                FROM eventos_usuario eu
                JOIN eventos e ON eu.evento_id = e.id
                WHERE eu.usuario_id = %s
                ORDER BY eu.fecha_inscripcion DESC
            """, (usuario_id,))
            rows = cursor.fetchall()
            eventos = []
            for row in rows:
                fecha_inscripcion = row[3].strftime('%Y-%m-%d %H:%M') if row[3] else None
                fecha_evento = row[6].strftime('%Y-%m-%d %H:%M') if row[6] else None
                evento = {
                    "usuario_id": row[0],
                    "evento_id": row[1],
                    "participacion": row[2],
                    "fecha_inscripcion": fecha_inscripcion,
                    "nombre_evento": row[4],
                    "ubicacion": row[5],
                    "fecha_evento": fecha_evento,
                } 
                eventos.append(evento)
            return eventos
        except Exception as e:
            print("Error al obtener eventos del usuario:", e)
            return []
        
    @classmethod
    def obtener_inscritos_evento(cls, mysql, evento_id):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("""
                SELECT eu.usuario_id, eu.evento_id, eu.participacion, 
                    eu.fecha_inscripcion, u.nombre, u.correo
                FROM eventos_usuario eu
                JOIN usuarios u ON eu.usuario_id = u.id
                WHERE eu.evento_id = %s
                ORDER BY eu.fecha_inscripcion DESC
            """, (evento_id,))
            rows = cursor.fetchall()
            usuarios = []
            for row in rows:
                fecha_formateada = row[3].strftime('%Y-%m-%d %H:%M') if row[3] else None
                usuario = {
                "usuario_id": row[0],
                "evento_id": row[1],
                "participacion": row[2],
                "fecha_inscripcion": fecha_formateada,
                "nombre": row[4],
                "correo": row[5],
                } 
                usuarios.append(usuario)
            return usuarios
        except Exception as e:
            print("Error al obtener usuarios inscritos al evento:", e)
            return []
        
    @classmethod
    def get_inscripcion_usuario_evento(cls, mysql, usuario_id, evento_id):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("""
                SELECT * FROM eventos_usuario
                WHERE usuario_id = %s AND evento_id = %s
            """, (usuario_id, evento_id))
            row = cursor.fetchone()

            if not row:
                return None
        
            fecha_formateada = row[4].strftime('%Y-%m-%d %H:%M') if row[4] else None
            eventos_usuario = EventosUsuario(row[0], row[1], row[2], row[3], fecha_formateada)
                
            return eventos_usuario.to_dict()
        except Exception as e:
            print("Error al obtener usuarios inscritos al evento:", e)
            return []