from flask import request, jsonify
from entities.Usuarios import Usuario, hash_password, check_password
from datetime import datetime, timedelta
import uuid 

class ModelUsuarios:
    @classmethod
    def get_all_usuarios(cls, mysql):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("SELECT * FROM usuarios")
            rows = cursor.fetchall()
            usuarios = [
                Usuario(*row).to_dict() for row in rows
            ]
            return usuarios
        except Exception as e:
            return str(e)

    @classmethod
    def crear_usuario_desde_invitacion(cls, mysql, invitacion_id):
        """Aceptar una invitación y crear un usuario nuevo"""
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("""
                SELECT id, correo_invitado, rol_destino, estado, usuario_id
                FROM invitaciones
                WHERE id=%s
            """, (invitacion_id,))
            invitacion = cursor.fetchone()

            if not invitacion:
                return {"error": "Invitación no encontrada"}

            invit_id, correo, rol_destino, estado, paciente_id = invitacion

            if estado != "pendiente":
                return {"error": "La invitación ya fue procesada"}

            rol = 3 if rol_destino == "familiar" else 4
            password = uuid.uuid4().hex[:8]  # contraseña aleatoria
            hashed_pw = hash_password(password)

            cursor.execute("""
                INSERT INTO usuarios (nombre, correo, fecha_nacimiento, contrasena_hash, id_rol, activo, debe_actualizar_datos)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, ("Usuario Invitado", correo, "2000-01-01", hashed_pw, rol, 1, 1))
            con.commit()

            nuevo_usuario_id = cursor.lastrowid  # ⚡️ IMPORTANTE

            cursor.execute("""
                UPDATE invitaciones SET estado='aceptada' WHERE id=%s
            """, (invitacion_id,))
            con.commit()

            return {
                "message": "Usuario creado con éxito",
                "correo": correo,
                "password": password,
                "nuevo_usuario_id": nuevo_usuario_id,  # <- NECESARIO para crear vínculo
                "paciente_id": paciente_id,            # <- viene de invitaciones.usuario_id
                "rol_destino": rol_destino             # <- familiar o medico
            }

        except Exception as e:
            print("Error en crear_usuario_desde_invitacion:", e)
            return {"error": str(e)}
        finally:
            cursor.close()
            con.close()

    @classmethod
    def actualizar_datos(cls, mysql, user_id, nombre, fecha_nacimiento, biografia, password):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            hashed_pw = hash_password(password)
            cursor.execute("""
                UPDATE usuarios
                SET nombre=%s, fecha_nacimiento=%s, biografia=%s, contrasena_hash=%s, debe_actualizar_datos=0
                WHERE id=%s
            """, (nombre, fecha_nacimiento, biografia, hashed_pw, user_id))
            con.commit()
            return {"message": "Datos actualizados correctamente"}
        except Exception as e:
            con.rollback()
            raise e
        finally:
            cursor.close()
            con.close()

    @classmethod
    def reset_password(cls, mysql, token, nueva_password):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            # Validar token y fecha de expiración
            cursor.execute("""
                SELECT id, reset_token_expira 
                FROM usuarios 
                WHERE reset_token = %s
            """, (token,))
            user = cursor.fetchone()

            if not user:
                return {"error": "Token inválido"}

            user_id, expira = user

            if expira < datetime.now():
                return {"error": "El token ha expirado"}

            # ✅ Hashear nueva contraseña con bcrypt
            hashed = hash_password(nueva_password)

            # Actualizar contraseña y limpiar token
            cursor.execute("""
                UPDATE usuarios 
                SET contrasena_hash = %s, reset_token = NULL, reset_token_expira = NULL 
                WHERE id = %s
            """, (hashed, user_id))
            con.commit()

            return {"message": "Contraseña actualizada correctamente"}
        except Exception as e:
            print("Error en reset_password:", e)
            return {"error": str(e)}
        finally:
            cursor.close()
            con.close()

    @classmethod
    def registrar_usuario(cls, mysql, data):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            hashed_pw = hash_password(data['password'])
            cursor.execute("""
                INSERT INTO usuarios (nombre, correo, fecha_nacimiento, contrasena_hash, debe_actualizar_datos)
                VALUES (%s, %s, %s, %s, 0)
            """, (data['nombre'], data['email'], data['fechaNacimiento'], hashed_pw))
            con.commit()
            return {"mensaje": "Usuario registrado correctamente"}
        except Exception as e:
            print(e)
            return {"error": str(e)}

    @classmethod
    def login_usuario(cls, mysql, data):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("""
                SELECT * 
                FROM usuarios WHERE correo = %s
            """, (data['correo'],))
            row = cursor.fetchone()
            if not row:
                return {"error": "Usuario no encontrado", "code": "not_found"}
            # row[4] = contrasena_hash   |  row[10] = activo  (ajusta índices si varían)
            if not check_password(data['password'], row[4]):
                return {"error": "Contraseña incorrecta", "code": "wrong_password"}

            # Si la contraseña es correcta, validamos estado activo
            if row[10] == 0:
                return {"error": "Cuenta deshabilitada", "code": "disabled"}

            user = Usuario(*row)
            return user.to_dict()
        except Exception as e:
            return {"error": str(e), "code": "server_error"}
        finally:
            cursor.close()
            con.close()
        
    @classmethod
    def update_usuario(cls, mysql, data):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("""
                UPDATE usuarios SET 
                nombre = %s,
                biografia = %s
                WHERE usuarios.id = %s

            """, (data['nombre'], data['biografia'], data['id'],))
            con.commit()
            return {"mensaje": "Usuario actualizado correctamente"}
        except Exception as e:
            print(e)
            return {"error": str(e)} 
    
    @classmethod
    def agregar_experiencia(cls, mysql, data):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            usuario_id = data['usuario_id']
            nivel_id = data['nivel_id']

            # 1. Obtener la experiencia que otorga ese nivel
            cursor.execute("SELECT experiencia_otorgada FROM niveles_juego WHERE id = %s", (nivel_id,))
            resultado = cursor.fetchone()
            if not resultado:
                return {"error": "Nivel no encontrado"}

            experiencia_otorgada = resultado[0]

            # 2. Obtener experiencia actual del usuario
            cursor.execute("SELECT experiencia FROM usuarios WHERE id = %s", (usuario_id,))
            resultado = cursor.fetchone()
            if not resultado:
                return {"error": "Usuario no encontrado"}

            experiencia_actual = resultado[0]

            # 3. Sumar y actualizar
            nueva_experiencia = experiencia_actual + experiencia_otorgada

            cursor.execute("UPDATE usuarios SET experiencia = %s WHERE id = %s", (nueva_experiencia, usuario_id))
            con.commit()

            return nueva_experiencia

        except Exception as e:
            print(e)
            return False
        finally:
            cursor.close()
            con.close()
    
    @staticmethod
    def eliminar_usuario(mysql, usuario_id):
        try:
            con = mysql.connect()
            cursor = con.cursor()

            # Eliminar usuario
            cursor.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
            con.commit()

            eliminado = cursor.rowcount > 0  # True si eliminó algo

            cursor.close()
            con.close()
            return eliminado

        except Exception as e:
            print("Error al eliminar usuario:", e)
            return False
    
    @staticmethod
    def desactivar_usuario(mysql, activo, usuario_id):
        try:
            con = mysql.connect()
            cursor = con.cursor()

            # Desactivar usuario
            cursor.execute("UPDATE usuarios SET activo = %s WHERE id = %s", (activo, usuario_id,))
            con.commit()

            desactivado = cursor.rowcount > 0  # True si eliminó algo

            cursor.close()
            con.close()
            return desactivado

        except Exception as e:
            print("Error al desactivar usuario:", e)
            return False
    
    @staticmethod
    def obtener_todos(mysql):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("""
                SELECT *
                FROM usuarios;
            """)
            rows = cursor.fetchall()
            usuarios = []
            for usuario in rows:
                usuarios_dict = Usuario(
                    usuario[0], usuario[1], usuario[2], usuario[3].strftime('%Y-%m-%d'), usuario[4], usuario[5].strftime('%Y-%m-%d'),
                    usuario[6], usuario[7], usuario[8], usuario[9], usuario[10], usuario[11], usuario[12], usuario[13], usuario[14]).to_dict()
                
                usuarios.append(usuarios_dict)
                
            return usuarios
        
        except Exception as e:
            return e
        finally:
            cursor.close()
            con.close()
            
    @staticmethod
    def obtener_estadisticas(mysql):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("""SELECT COUNT(*) FROM usuarios WHERE activo = 1""")
            usuarios_activos = cursor.fetchone()[0]

            cursor.execute("""SELECT COUNT(*) FROM usuarios""")
            total_usuarios = cursor.fetchone()[0]

            cursor.execute("""SELECT COUNT(*) FROM juegos""")
            total_juegos = cursor.fetchone()[0]

            # --- Totales
            cursor.execute("""SELECT COUNT(*) FROM incidencias""")
            total_incidencias = cursor.fetchone()[0]

            cursor.execute("""SELECT COUNT(*) FROM actividad_usuario""")
            total_actividades = cursor.fetchone()[0]
            
            cursor.execute("""SELECT SUM(tiempo_segundos) AS total_segundos FROM actividad_usuario""")
            total_tiempo = cursor.fetchone()[0]

            return ({
                "usuarios_activos": usuarios_activos,
                "total_usuarios": total_usuarios,
                "total_juegos": total_juegos,
                "total_incidencias": total_incidencias,
                "total_actividades": total_actividades,
                "total_tiempo": total_tiempo
            })

        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return jsonify({"error": str(e)}), 500

        
        finally:
            cursor.close()
            con.close() 
    
    @staticmethod
    def obtener_reporte_usuario(mysql, usuario_id):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            # --- Datos básicos del usuario ---
            cursor.execute("""
                SELECT 
                    id, nombre, correo, fecha_nacimiento, fecha_registro, 
                    id_rol, activo, experiencia
                FROM usuarios 
                WHERE id = %s;
            """, (usuario_id,))
            row = cursor.fetchone()

            if not row:
                return None

            keys = [desc[0] for desc in cursor.description]
            usuario = dict(zip(keys, row))

            # Calcular nivel y progreso desde la experiencia
            exp_total = usuario.get("experiencia", 0)
            nivel_calculado, progreso = calcular_nivel_y_progreso(exp_total)

            usuario["nivel_calculado"] = nivel_calculado
            usuario["progreso_nivel"] = progreso

            # --- Totales ---
            cursor.execute("""
                SELECT COUNT(*) 
                FROM actividad_usuario
                WHERE usuario_id = %s
                AND tipo_evento = 'Jugar';
            """, (usuario_id,))
            numero_jugadas = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COUNT(*)
                FROM actividad_usuario
                WHERE usuario_id = %s
                AND tipo_evento = 'Completar un nivel';
            """, (usuario_id,))
            numero_completados = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COALESCE(SUM(tiempo_segundos), 0)
                FROM actividad_usuario
                WHERE usuario_id = %s
                AND tipo_evento IN ('Jugar', 'Completar un nivel');
            """, (usuario_id,))
            numero_tiempo = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COUNT(*)
                FROM actividad_usuario
                WHERE usuario_id = %s
                AND tipo_evento = 'Iniciar sesión';
            """, (usuario_id,))
            numero_inicios = cursor.fetchone()[0]

            # --- Nivel alcanzado por juego ---
            cursor.execute("""
                SELECT nv.usuario_id, nv.nivel_id, j.nombre FROM niveles_juego_usuario nv
                INNER JOIN juegos j ON nv.juego_id = j.id WHERE nv.usuario_id = %s;
            """, (usuario_id,))
            niveles_alcanzados = cursor.fetchall()
            niveles_alcanzados = [
                {
                    "usuario_id": na[0],
                    "nivel_id": na[1],
                    "nombre": na[2]
                }
                for na in niveles_alcanzados
            ]

            # --- Reseñas del usuario ---
            cursor.execute("""
                SELECT v.id, v.juego_id, v.puntuacion, v.comentario, v.fecha, v.es_destacada, v.editada, j.nombre
                FROM valoraciones v INNER JOIN juegos j ON v.juego_id = j.id
                WHERE v.usuario_id = %s
                ORDER BY v.fecha DESC;
            """, (usuario_id,))
            reseñas = cursor.fetchall()
            reseñas = [
                {
                    "id": r[0],
                    "juego_id": r[1],
                    "puntuacion": r[2],
                    "comentario": r[3],
                    "fecha": str(r[4]),
                    "es_destacada": r[5],
                    "editada": r[6],
                    "nombre": r[7]
                }
                for r in reseñas
            ]

            # --- Últimas 50 actividades ---
            cursor.execute("""
                SELECT *
                FROM actividad_usuario
                WHERE usuario_id = %s
                ORDER BY fecha DESC
                LIMIT 50;
            """, (usuario_id,))
            actividades = cursor.fetchall()
            actividades = [
                {
                    "id": a[0],
                    "usuario_id": a[1],
                    "tipo_evento": a[2],
                    "descripcion": a[3],
                    "fecha": str(a[4]),
                    "tiempo_segundos": a[5]
                }
                for a in actividades
            ]

            return {
                **usuario,  # desestructura todo lo de usuarios
                "numero_jugadas": numero_jugadas,
                "numero_completados": numero_completados,
                "numero_tiempo": numero_tiempo,
                "numero_inicios": numero_inicios,
                "niveles_alcanzados": niveles_alcanzados,
                "valoraciones": reseñas,
                "actividades": actividades
            }

        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return {"error": str(e)}

        finally:
            cursor.close()
            con.close()

    
    @staticmethod
    def obtener_graficas(mysql, filtro='7d'):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            # --- Rango de fechas
            hoy = datetime.now().date()
            if filtro == '7d':
                desde = hoy - timedelta(days=6)
            elif filtro == '30d':
                desde = hoy - timedelta(days=29)
            else:
                desde = None  # global

            cursor.execute("""SELECT nombre, numero_jugadas FROM juegos ORDER BY numero_jugadas DESC LIMIT 5""")
            juegos_populares = cursor.fetchall()

            # --- Registros por día
            if desde:
                cursor.execute("""
                    SELECT DATE(fecha_registro) as fecha, COUNT(*) 
                    FROM usuarios 
                    WHERE fecha_registro >= %s
                    GROUP BY fecha ORDER BY fecha ASC
                """, (desde,))
                registros_raw = cursor.fetchall()
            else:
                cursor.execute("""
                    SELECT DATE(fecha_registro) as fecha, COUNT(*) 
                    FROM usuarios 
                    GROUP BY fecha ORDER BY fecha ASC
                """)
                registros_raw = cursor.fetchall()

            # --- Actividad por día
            if desde:
                cursor.execute("""
                    SELECT DATE(fecha) as groupfecha, COUNT(*) 
                    FROM actividad_usuario 
                    WHERE fecha >= %s
                    GROUP BY groupfecha ORDER BY groupfecha ASC
                """, (desde,))
                actividades_raw = cursor.fetchall()
            else:
                cursor.execute("""
                    SELECT DATE(fecha) as groupfecha, COUNT(*) 
                    FROM actividad_usuario 
                    GROUP BY groupfecha ORDER BY groupfecha ASC
                """)
                actividades_raw = cursor.fetchall()
                
            # --- Tiempo por día
            if desde:
                cursor.execute("""
                    SELECT DATE(fecha) as groupfecha, SUM(tiempo_segundos) 
                    FROM actividad_usuario 
                    WHERE fecha >= %s
                    GROUP BY groupfecha ORDER BY groupfecha ASC
                """, (desde,))
                tiempo_raw = cursor.fetchall()
            else:
                cursor.execute("""
                    SELECT DATE(fecha) as fechas, SUM(tiempo_segundos) 
                    FROM actividad_usuario 
                    GROUP BY fechas ORDER BY fechas ASC
                """)
                tiempo_raw = cursor.fetchall()

            # --- Rellenar días vacíos
            def rellenar_dias(desde, hasta, datos_raw):
                fechas_existentes = {
                    str(r[0]): (r[1] if r[1] is not None else 0)  # evita None en SUM
                    for r in datos_raw
                }
                return [
                    {"fecha": str((desde + timedelta(days=i))), "cantidad": fechas_existentes.get(str(desde + timedelta(days=i)), 0)}
                    for i in range((hasta - desde).days + 1)
                ]

            if desde:
                hasta = hoy
                registros_por_dia = rellenar_dias(desde, hasta, registros_raw)
                actividades_por_dia = rellenar_dias(desde, hasta, actividades_raw)
                tiempo_por_dia = rellenar_dias(desde, hasta, tiempo_raw)
            else:
                registros_por_dia = [{"fecha": str(r[0]), "cantidad": r[1]} for r in registros_raw]
                actividades_por_dia = [{"fecha": str(r[0]), "cantidad": r[1]} for r in actividades_raw]
                tiempo_por_dia = [{"fecha": str(r[0]), "cantidad": (r[1] if r[1] is not None else 0)} for r in tiempo_raw]


            return ({
                "actividades_por_dia": actividades_por_dia,
                "juegos_populares": [{"nombre": j[0], "jugadas": j[1]} for j in juegos_populares],
                "registros_por_dia": registros_por_dia,
                "tiempo_por_dia": tiempo_por_dia
            })

        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return jsonify({"error": str(e)}), 500

        finally:
            cursor.close()
            con.close()        
            
    @staticmethod
    def obtener_usuario_por_id(mysql, data): 
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("""
                SELECT id, nombre, correo, fecha_nacimiento, fecha_registro, avatar_url, 
                    biografia, ultima_conexion, activo, experiencia
                    FROM usuarios WHERE id = %s
            """, (data,))
            row = cursor.fetchone()
            if row:
                keys = [desc[0] for desc in cursor.description]
                usuario = dict(zip(keys, row))

                # Calcular nivel y progreso desde la experiencia
                exp_total = usuario.get("experiencia", 0)
                nivel_calculado, progreso = calcular_nivel_y_progreso(exp_total)

                # Agregar los campos calculados
                usuario["nivel_calculado"] = nivel_calculado
                usuario["progreso_nivel"] = progreso

                return usuario

            return None
        except Exception as e:
            return {"error": str(e)}
        
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

    