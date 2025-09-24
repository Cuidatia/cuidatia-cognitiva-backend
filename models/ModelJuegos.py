from flask import Flask, jsonify, request
from entities.Juegos import Juego

class ModelJuegos:
    @classmethod
    def get_all_juegos(cls, mysql, usuario_id=None):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            if usuario_id:  
                # Usuario logueado → filtra global + individual
                cursor.execute("""
                    SELECT j.*
                    FROM juegos j
                    WHERE j.bloqueado = 0
                    AND NOT EXISTS (
                        SELECT 1
                        FROM juegos_bloqueados jb
                        WHERE jb.juego_id = j.id
                        AND jb.usuario_id = %s
                        AND jb.activo = 1
                    )
                """, (usuario_id,))
            else:
                # Usuario anónimo → solo filtra global
                cursor.execute("""
                    SELECT *
                    FROM juegos
                    WHERE bloqueado = 0
                """)

            rows = cursor.fetchall()

            juegos = []
            for juego in rows:
                juego_dict = Juego(
                    juego[0], juego[1], juego[2], juego[3], juego[4],
                    juego[5], juego[6], juego[7], juego[8]
                ).to_dict()

                # Obtener puntuación promedio y número de valoraciones
                info_valoracion = cls.get_info_completa(mysql, juego_dict["id"])
                juego_dict["puntuacion_promedia"] = info_valoracion.get("puntuacion_promedia", 0)
                juego_dict["numero_valoraciones"] = info_valoracion.get("numero_valoraciones", 0)

                juegos.append(juego_dict)

            return juegos
        except Exception as e:
            print("Error en get_all_juegos:", e)
            return []
        finally:
            cursor.close()
            con.close()
    
    @classmethod
    def get_juego_by_id(cls, mysql, juego_id):
        con = mysql.connect()
        cursor = con.cursor()

        try:
            cursor.execute("SELECT * FROM juegos WHERE id = %s", (juego_id,))
            row = cursor.fetchone()

            if row:
                juego = Juego(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
                return juego.to_dict()
            else:
                return None
        except Exception as e:
            return {"error": str(e)}
        
    @classmethod
    def get_info_completa(cls, mysql, juego_id):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            # Valoraciones con comentarios (reseñas)
            cursor.execute("""
                SELECT 
                    AVG(puntuacion) AS puntuacion_promedia,
                    COUNT(*) AS numero_valoraciones
                FROM valoraciones
                WHERE juego_id = %s
            """, (juego_id,))
            valoracion = cursor.fetchone()
            # print(valoracion)

            return {
                "puntuacion_promedia": float(valoracion[0]) if valoracion[0] else 0,
                "numero_valoraciones": valoracion[1] or 0
            }
        except Exception as e:
            print("Error en get_info_completa:", e)
            return {'error': str(e)}
        finally:
            cursor.close()
            con.close()

    @classmethod
    def incrementar_jugadas(cls, mysql, juego_id):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("""
                UPDATE juegos
                SET numero_jugadas = numero_jugadas + 1
                WHERE id = %s
            """, (juego_id,))
            con.commit()
            return {'mensaje': 'Jugadas actualizadas'}
        except Exception as e:
            print("Error en incrementar_jugadas:", e)
            return {'error': str(e)}
        finally:
            cursor.close()
            con.close()
            
    @staticmethod
    def obtener_mas_jugados(mysql, limite=4):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("""
                SELECT id, nombre, imagen, descripcion, categoria, numero_jugadas, icono
                FROM juegos
                ORDER BY numero_jugadas DESC
                LIMIT %s
            """, (limite,))
            resultados = cursor.fetchall()
            juegos = []
            for row in resultados:
                juegos.append({
                    "id": row[0],
                    "nombre": row[1],
                    "imagen": row[2],
                    "descripcion": row[3],
                    "categoria": row[4],
                    "numero_jugadas": row[5],
                    "icono": row[6]
                })
            return juegos
        except Exception as e:
            print("Error en obtener_mas_jugados:", e)
            return []
        finally:
            cursor.close()
            con.close()
            
            
            
            
    @staticmethod
    def obtener_todos(mysql):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("""
                SELECT * FROM juegos
            """)
            
            rows=cursor.fetchall()
            juegos = []
            for juego in rows:
                juego_dict = Juego(
                    juego[0], juego[1], juego[2], juego[3], juego[4], juego[5], juego[6], juego[7], juego[8]
                ).to_dict()

                juegos.append(juego_dict)

            return juegos
        except Exception as e:
            print("Error en :", e)
            return []
        finally:
            cursor.close()
            con.close()

    @staticmethod
    def bloquear_juego(mysql, juego_id, bloquear):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("UPDATE juegos SET bloqueado = %s WHERE id = %s", (bloquear, juego_id))
            con.commit()
            cursor.close()
        except Exception as e:
            print("Error en obtener_mas_jugados:", e)
            return []
        finally:
            cursor.close()
            con.close()