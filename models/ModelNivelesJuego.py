from flask import Flask, jsonify, request
from entities.NivelesJuego import NivelJuego

class ModelNivelesJuego:

    @staticmethod
    def obtener_nivel_desbloqueado(mysql, usuario_id, juego_id):
        try:
            cursor = mysql.connection.cursor()
            sql = """
                SELECT MAX(nj.id)
                FROM niveles_juego_usuario nju
                JOIN niveles_juego nj ON nju.nivel_id = nj.id
                WHERE nju.usuario_id = %s AND nju.juego_id = %s
            """
            cursor.execute(sql, (usuario_id, juego_id))
            result = cursor.fetchone()
            return result[0] if result[0] is not None else 1
        except Exception as e:
            print("Error obteniendo nivel desbloqueado:", e)
            return 1

    @staticmethod
    def completar_nivel(mysql, usuario_id, juego_id, nivel_id):
        try:
            cursor = mysql.connection.cursor()

            # 1. Registrar el nivel si no existe
            cursor.execute("""
                SELECT id FROM niveles_juego_usuario
                WHERE usuario_id = %s AND nivel_id = %s AND juego_id = %s
            """, (usuario_id, nivel_id, juego_id))
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO niveles_juego_usuario (usuario_id, nivel_id, juego_id)
                    VALUES (%s, %s, %s)
                """, (usuario_id, nivel_id, juego_id))

            # 2. Obtener experiencia del nivel actual
            cursor.execute("SELECT experiencia_otorgada FROM niveles_juego WHERE id = %s", (nivel_id,))
            xp = cursor.fetchone()
            xp = xp[0] if xp else 0

            # 3. Sumar experiencia al usuario
            cursor.execute("UPDATE usuarios SET experiencia = experiencia + %s WHERE id = %s", (xp, usuario_id))

            # 4. Desbloquear el siguiente nivel (si existe)
            cursor.execute("SELECT id FROM niveles_juego WHERE id = %s + 1", (nivel_id,))
            siguiente_nivel = cursor.fetchone()
            if siguiente_nivel:
                siguiente_nivel_id = siguiente_nivel[0]

                cursor.execute("""
                    SELECT id FROM niveles_juego_usuario
                    WHERE usuario_id = %s AND nivel_id = %s AND juego_id = %s
                """, (usuario_id, siguiente_nivel_id, juego_id))
                if not cursor.fetchone():
                    cursor.execute("""
                        INSERT INTO niveles_juego_usuario (usuario_id, nivel_id, juego_id)
                        VALUES (%s, %s, %s)
                    """, (usuario_id, siguiente_nivel_id, juego_id))

            mysql.connection.commit()

            return {
                "mensaje": "Nivel completado y experiencia otorgada",
                "exp_añadida": xp,
                "nivel_desbloqueado": nivel_id + 1 if siguiente_nivel else nivel_id
            }

        except Exception as e:
            mysql.connection.rollback()
            print("Error completando nivel:", e)
            return {"error": "Error completando nivel"}