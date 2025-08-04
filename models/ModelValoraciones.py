class ModelValoracion:
    @classmethod
    def obtener_valoracion(cls, mysql, juego_id, usuario_id):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("""
                SELECT id, juego_id, usuario_id, puntuacion, comentario, fecha, es_destacada, editada
                FROM valoraciones
                WHERE juego_id = %s AND usuario_id = %s
            """, (juego_id, usuario_id))
            row = cursor.fetchone()
            if row:
                keys = [desc[0] for desc in cursor.description]
                return dict(zip(keys, row))
            return None
        except Exception as e:
            return {"error": str(e)}

    @classmethod
    def crear_valoracion(cls, mysql, data):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("""
                INSERT INTO valoraciones (juego_id, usuario_id, puntuacion, comentario)
                VALUES (%s, %s, %s, %s)
            """, (data['juego_id'], data['usuario_id'], data['puntuacion'], data['comentario']))
            con.commit()
            return {"mensaje": "Valoración creada correctamente"}
        except Exception as e:
            return {"error": str(e)}

    @classmethod
    def eliminar_valoracion(cls, mysql, juego_id, usuario_id):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("""
                DELETE FROM valoraciones WHERE juego_id = %s 
                AND usuario_id = %s""", (juego_id, usuario_id))
            con.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print("Error en eliminar_valoracion:", e)
            return False
    
    @classmethod
    def editar_valoracion(cls, mysql, data):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("""
                UPDATE valoraciones
                SET puntuacion = %s, comentario = %s, editada = TRUE
                WHERE juego_id = %s AND usuario_id = %s
            """, (data['puntuacion'], data['comentario'], data['juego_id'], data['usuario_id']))
            con.commit()
            return {"mensaje": "Valoración actualizada correctamente"}
        except Exception as e:
            return {"error": str(e)}