# models/ModelSeguimiento.py
from datetime import datetime, timedelta

class ModelSeguimiento:

    # ========== ADMIN ==========
    @staticmethod
    def crear_vinculo(mysql, paciente_id, supervisor_id, tipo_vinculo):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("""
                INSERT INTO vinculos_usuario (paciente_id, supervisor_id, tipo_vinculo)
                VALUES (%s, %s, %s)
            """, (paciente_id, supervisor_id, tipo_vinculo))
            con.commit()
            return cursor.rowcount > 0
        except Exception as e:
            con.rollback()
            raise e
        finally:
            cursor.close()
            con.close()

    @staticmethod
    def eliminar_vinculo(mysql, paciente_id, supervisor_id):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("""
                DELETE FROM vinculos_usuario
                WHERE paciente_id = %s AND supervisor_id = %s
            """, (paciente_id, supervisor_id))
            con.commit()
            return cursor.rowcount > 0
        except Exception as e:
            con.rollback()
            raise e
        finally:
            cursor.close()
            con.close()

    # ========== SUPERVISOR (familiar/médico) ==========
    @staticmethod
    def obtener_pacientes_vinculados(mysql, supervisor_id):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("""
                SELECT u.id, u.nombre, u.correo, u.avatar_url, u.experiencia, u.fecha_registro,
                       v.tipo_vinculo
                FROM vinculos_usuario v
                JOIN usuarios u ON u.id = v.paciente_id
                WHERE v.supervisor_id = %s
                ORDER BY u.nombre ASC
            """, (supervisor_id,))
            rows = cursor.fetchall()

            pacientes = []
            for r in rows:
                pacientes.append({
                    "id": r[0],
                    "nombre": r[1],
                    "correo": r[2],
                    "avatar_url": r[3],
                    "experiencia": r[4],
                    "fecha_registro": r[5].strftime('%Y-%m-%d') if r[5] else None,
                    "tipo_vinculo": r[6],
                })
            return pacientes
        finally:
            cursor.close()
            con.close()

    @staticmethod
    def obtener_resumen_paciente(mysql, usuario_id):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            # Datos básicos
            cursor.execute("""
                SELECT id, nombre, correo, avatar_url, experiencia, fecha_registro, ultima_conexion, activo
                FROM usuarios WHERE id = %s
            """, (usuario_id,))
            u = cursor.fetchone()
            if not u:
                return {"error": "Usuario no encontrado"}

            usuario = {
                "id": u[0],
                "nombre": u[1],
                "correo": u[2],
                "avatar_url": u[3],
                "experiencia": u[4],
                "fecha_registro": u[5].strftime('%Y-%m-%d') if u[5] else None,
                "ultima_conexion": u[6].strftime('%Y-%m-%d %H:%M') if u[6] else None,
                "activo": bool(u[7]),
            }

            # Totales actividad
            cursor.execute("""
                SELECT 
                    SUM(CASE WHEN tipo_evento='Jugar' THEN 1 ELSE 0 END) AS total_jugados,
                    SUM(CASE WHEN tipo_evento='Completar un nivel' THEN 1 ELSE 0 END) AS niveles_completados,
                    SUM(CASE WHEN tipo_evento IN ('Jugar','Completar un nivel') THEN COALESCE(tiempo_segundos,0) ELSE 0 END) AS tiempo_total,
                    SUM(CASE WHEN tipo_evento='Iniciar sesión' THEN 1 ELSE 0 END) AS total_logins
                FROM actividad_usuario
                WHERE usuario_id = %s
            """, (usuario_id,))
            t = cursor.fetchone()
            totals = {
                "total_jugados": int(t[0] or 0),
                "niveles_completados": int(t[1] or 0),
                "tiempo_total": int(t[2] or 0),
                "total_logins": int(t[3] or 0),
            }

            # Últimas actividades (hasta 10)
            cursor.execute("""
                SELECT tipo_evento, descripcion, fecha, tiempo_segundos
                FROM actividad_usuario
                WHERE usuario_id = %s
                ORDER BY fecha DESC
                LIMIT 10
            """, (usuario_id,))
            acts = cursor.fetchall()
            actividades = []
            for a in acts:
                actividades.append({
                    "tipo_evento": a[0],
                    "descripcion": a[1],
                    "fecha": a[2].strftime('%Y-%m-%d %H:%M') if a[2] else None,
                    "tiempo_segundos": a[3],
                })

            # Valoraciones (hasta 5)
            cursor.execute("""
                SELECT v.id, v.juego_id, j.nombre, v.puntuacion, v.comentario, v.fecha
                FROM valoraciones v
                LEFT JOIN juegos j ON j.id = v.juego_id
                WHERE v.usuario_id = %s
                ORDER BY v.fecha DESC
                LIMIT 5
            """, (usuario_id,))
            vals = cursor.fetchall()
            valoraciones = []
            for v in vals:
                valoraciones.append({
                    "id": v[0],
                    "juego_id": v[1],
                    "juego_nombre": v[2],
                    "puntuacion": v[3],
                    "comentario": v[4],
                    "fecha": v[5].strftime('%Y-%m-%d') if v[5] else None,
                })

            # Calcular nivel y progreso desde la experiencia
            exp_total = usuario.get("experiencia", 0)
            nivel_calculado, progreso = calcular_nivel_y_progreso(exp_total)

            # Agregar los campos calculados
            usuario["nivel_calculado"] = nivel_calculado
            usuario["progreso_nivel"] = progreso
            
            return {
                "usuario": usuario,
                "totales": totals,
                "actividades": actividades,
                "valoraciones": valoraciones
            }
        finally:
            cursor.close()
            con.close()

    @staticmethod
    def obtener_series_paciente(mysql, usuario_id, filtro='7d'):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            hoy = datetime.now().date()
            if filtro == '7d':
                desde = hoy - timedelta(days=6)
            elif filtro == '30d':
                desde = hoy - timedelta(days=29)
            else:
                desde = None

            def rellenar(desde, hasta, raw):
                # raw: [(date, value)]
                dmap = {str(r[0]): int(r[1] or 0) for r in raw}
                return [
                    {"fecha": str(desde + timedelta(days=i)), "cantidad": dmap.get(str(desde + timedelta(days=i)), 0)}
                    for i in range((hasta - desde).days + 1)
                ]

            # Actividad por día
            if desde:
                cursor.execute("""
                    SELECT DATE(fecha) d, COUNT(*) c 
                    FROM actividad_usuario
                    WHERE usuario_id = %s AND fecha >= %s
                    GROUP BY d ORDER BY d
                """, (usuario_id, desde))
                act_raw = cursor.fetchall()
            else:
                cursor.execute("""
                    SELECT DATE(fecha) d, COUNT(*) c 
                    FROM actividad_usuario
                    WHERE usuario_id = %s
                    GROUP BY d ORDER BY d
                """, (usuario_id,))
                act_raw = cursor.fetchall()

            # Tiempo jugado por día
            if desde:
                cursor.execute("""
                    SELECT DATE(fecha) d, SUM(tiempo_segundos) s
                    FROM actividad_usuario
                    WHERE usuario_id = %s AND fecha >= %s
                    GROUP BY d ORDER BY d
                """, (usuario_id, desde))
                time_raw = cursor.fetchall()
            else:
                cursor.execute("""
                    SELECT DATE(fecha) d, SUM(tiempo_segundos) s
                    FROM actividad_usuario
                    WHERE usuario_id = %s
                    GROUP BY d ORDER BY d
                """, (usuario_id,))
                time_raw = cursor.fetchall()

            if desde:
                hasta = hoy
                actividades_por_dia = rellenar(desde, hasta, act_raw)
                tiempo_por_dia = rellenar(desde, hasta, time_raw)
            else:
                actividades_por_dia = [{"fecha": str(r[0]), "cantidad": int(r[1] or 0)} for r in act_raw]
                tiempo_por_dia = [{"fecha": str(r[0]), "cantidad": int(r[1] or 0)} for r in time_raw]

            return {
                "actividades_por_dia": actividades_por_dia,
                "tiempo_por_dia": tiempo_por_dia
            }
        finally:
            cursor.close()
            con.close()
            
def calcular_nivel_y_progreso(exp_total):
    nivel = 1
    exp_requerida = 10
    exp_acumulada = 0

    while exp_total >= exp_acumulada + exp_requerida:
        exp_acumulada += exp_requerida
        nivel += 1
        exp_requerida = nivel * 10

    exp_actual_nivel = exp_total - exp_acumulada
    exp_siguiente_nivel = exp_requerida
    progreso = int((exp_actual_nivel / exp_siguiente_nivel) * 100)

    return nivel, progreso