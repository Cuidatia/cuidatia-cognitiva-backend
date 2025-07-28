from flask import Flask, jsonify, request
from entities.Juegos import Juego

class ModelJuegos:
    @classmethod
    def get_all_juegos(cls, mysql):
        con= mysql.connect()
        cursor = con.cursor()
        
        try:
            cursor.execute(""" 

                select * from juegos;

            """)

            rows=cursor.fetchall()
            
            juegos = []
            for juego in rows:
                juego_dict = Juego(
                    juego[0], juego[1], juego[2], juego[3], juego[4], juego[5], juego[6], juego[7]
                ).to_dict()

                # Obtener puntuación promedio y número de valoraciones
                info_valoracion = cls.get_info_completa(mysql, juego_dict["id"])
                juego_dict["puntuacion_promedia"] = info_valoracion.get("puntuacion_promedia", 0)
                juego_dict["numero_valoraciones"] = info_valoracion.get("numero_valoraciones", 0)

                juegos.append(juego_dict)

            return juegos
        except Exception as e:
            return e
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
                juego = Juego(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
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
            
    @classmethod        
    def obtener_juegos_mas_jugados(cls, mysql):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            
            cursor.execute("""
                SELECT id, nombre, descripcion, imagen, icono, categoria, numero_jugadas
                FROM juegos
                ORDER BY numero_jugadas DESC
                LIMIT 4
            """)
            
            juegos = cursor.fetchall()
            cursor.close()

            juegos_lista = []
            for juego in juegos:
                juegos_lista.append({
                    "id": juego[0],
                    "nombre": juego[1],
                    "descripcion": juego[2],
                    "imagen": juego[3],
                    "icono": juego[4],  # URL o nombre del ícono
                    "categoria": juego[5],
                    "numero_jugadas": juego[6],
                })

            return juegos_lista
        except Exception as e:
            print("Error al obtener juegos más jugados:", e)
            return []