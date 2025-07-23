from flask import request, jsonify
from entities.Usuarios import Usuario, hash_password, check_password

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
    def registrar_usuario(cls, mysql, data):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            hashed_pw = hash_password(data['password'])
            cursor.execute("""
                INSERT INTO usuarios (nombre, correo, fecha_nacimiento, contrasena_hash)
                VALUES (%s, %s, %s, %s)
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
            if row:
                user = Usuario(*row)
                if check_password(data['password'], row[4]):
                    return user.to_dict()
                else:
                    return {"error": "Contraseña incorrecta"}
            else:
                return {"error": "Usuario no encontrado"}
        except Exception as e:
            return {"error": str(e)}
        
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
            for juego in rows:
                usuarios_dict = Usuario(
                    juego[0], juego[1], juego[2], juego[3].strftime('%Y-%m-%d'), juego[4], juego[5].strftime('%Y-%m-%d'),
                    juego[6], juego[7], juego[8], juego[9], juego[10], juego[11]).to_dict()
                
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

            cursor.execute("""SELECT nombre, numero_jugadas FROM juegos ORDER BY numero_jugadas DESC LIMIT 5""")
            juegos_populares = cursor.fetchall()

            cursor.execute("""SELECT DATE(fecha_registro) as fecha, COUNT(*) FROM usuarios GROUP BY fecha ORDER BY fecha DESC LIMIT 7""")
            registros_por_dia = cursor.fetchall()

            return ({
                "usuarios_activos": usuarios_activos,
                "total_usuarios": total_usuarios,
                "total_juegos": total_juegos,
                "juegos_populares": [{"nombre": j[0], "jugadas": j[1]} for j in juegos_populares],
                "registros_por_dia": [{"fecha": str(r[0]), "cantidad": r[1]} for r in registros_por_dia]
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

    