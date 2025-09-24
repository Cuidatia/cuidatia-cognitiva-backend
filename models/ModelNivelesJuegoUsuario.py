from flask import Flask, jsonify, request
from entities.NivelesJuegoUsuario import NivelJuegoUsuario

class ModelNivelJuegoUsuario:
    @classmethod
    def get_all_niveles_juego_usuario(cls, mysql):
        con= mysql.connect()
        cursor = con.cursor()
        
        try:
            cursor.execute(""" 

                select * from niveles_juego_usuario;

            """)

            rows=cursor.fetchall()
            
            niveles = []
            for nivel in rows:
                nivel.append(NivelJuegoUsuario(nivel[0],nivel[1],nivel[2],nivel[3],nivel[4],nivel[5],nivel[6]).to_dict())

            return niveles
        except Exception as e:
            return e
        
    @classmethod
    def sacar_nivel(cls, mysql, usuario_id, juego_id):
        con= mysql.connect()
        cursor = con.cursor()
        
        try:
            cursor.execute("""
                           
            SELECT nivel_id FROM niveles_juego_usuario
            WHERE usuario_id = %s AND juego_id = %s
        
            """, (usuario_id, juego_id))
            
            result = cursor.fetchone()
            nivel = result[0] if result else 1  # Por defecto, nivel 1

            return nivel
        except Exception as e:
            return e
        finally:
            cursor.close()
            con.close()
    
    @classmethod
    def get_favorito(cls, mysql, juego_id, usuario_id):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("""
                SELECT es_favorito
                FROM niveles_juego_usuario
                WHERE juego_id = %s AND usuario_id = %s
            """, (juego_id, usuario_id))
            
            favorito = cursor.fetchone()

            return {"es_favorito": bool(favorito[0])} if favorito else {"es_favorito": False}
        except Exception as e:
            print("Error en get_favorito:", e)
            return {'error': str(e)}
        finally:
            cursor.close()
            con.close()
      
    @classmethod
    def toggle_favorito(cls, mysql, usuario_id, juego_id):
        con = mysql.connect()
        cursor = con.cursor()

        try:
            # Buscar la fila del usuario y juego, sin importar el nivel
            cursor.execute("""
                SELECT id, es_favorito FROM niveles_juego_usuario 
                WHERE usuario_id = %s AND juego_id = %s 
                ORDER BY nivel_id ASC LIMIT 1
            """, (usuario_id, juego_id))
            row = cursor.fetchone()

            if row:
                id_registro, es_favorito_actual = row
                nuevo_valor = not es_favorito_actual

                cursor.execute("""
                    UPDATE niveles_juego_usuario 
                    SET es_favorito = %s 
                    WHERE id = %s
                """, (nuevo_valor, id_registro))
            else:
                # Si no hay registro, crear uno con nivel_id = 1 (nivel más bajo por defecto)
                cursor.execute("""
                    INSERT INTO niveles_juego_usuario (usuario_id, juego_id, nivel_id, es_favorito)
                    VALUES (%s, %s, 1, TRUE)
                """, (usuario_id, juego_id))
                nuevo_valor = True

            con.commit()
            return {'success': True, 'es_favorito': nuevo_valor}

        except Exception as e:
            print("Error en toggle_favorito:", e)
            return {'error': str(e)}
        finally:
            cursor.close()
            con.close()  
        
    @classmethod
    def aumentar_nivel(cls, mysql, juego_id, usuario_id, nivel_id):
        con= mysql.connect()
        cursor = con.cursor()
        
        try:
            # Primero, comprobar si ya existe una fila para ese usuario y juego
            cursor.execute("""
                SELECT nivel_id FROM niveles_juego_usuario
                WHERE usuario_id = %s AND juego_id = %s
            """, (usuario_id, juego_id))

            existe = cursor.fetchone()
            nivel_actual = existe[0] if existe else 1

            if nivel_id == nivel_actual + 1:
                if existe:
                    cursor.execute("""
                        UPDATE niveles_juego_usuario
                        SET nivel_id = %s
                        WHERE usuario_id = %s AND juego_id = %s
                    """, (nivel_id, usuario_id, juego_id))
                else:
                    cursor.execute("""
                        INSERT INTO niveles_juego_usuario (usuario_id, juego_id, nivel_id)
                        VALUES (%s, %s, %s)
                    """, (usuario_id, juego_id, nivel_id))

                con.commit()
                return {'mensaje': 'Nivel actualizado correctamente'}
            else:
                return {'mensaje': 'Nivel no actualizado porque no se completó el último desbloqueado'}

        except Exception as e:
            return {'error': str(e)}, 500
        finally:
            cursor.close()
            con.close()