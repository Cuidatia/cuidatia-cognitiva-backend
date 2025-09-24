from entities.Incidencias import Incidencia

class ModelIncidencias:

    @classmethod
    def insertar_incidencia(cls, mysql, nombre, email, tipo, mensaje):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("""
                INSERT INTO incidencias (nombre, email, tipo, mensaje, fecha)
                VALUES (%s, %s, %s, %s, NOW())
            """, (nombre, email, tipo, mensaje))
            con.commit()
            return {'mensaje': 'Incidencia registrada correctamente'}
        except Exception as e:
            print("Error al insertar incidencia:", e)
            return {'error': str(e)}
        finally:
            cursor.close()
            con.close()
         
    @staticmethod
    def toggle_resuelta(mysql, incidencia_id):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("SELECT resuelta FROM incidencias WHERE id = %s", (incidencia_id,))
            row = cursor.fetchone()
            if not row:
                return None

            nuevo_estado = 0 if row[0] else 1
            cursor.execute("UPDATE incidencias SET resuelta = %s WHERE id = %s", (nuevo_estado, incidencia_id))
            con.commit()
            return {"id": incidencia_id, "resuelta": nuevo_estado}
        finally:
            cursor.close()
            con.close()

    @staticmethod
    def eliminar_incidencia(mysql, incidencia_id):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("DELETE FROM incidencias WHERE id = %s", (incidencia_id,))
            con.commit()
            return {"id": incidencia_id}
        finally:
            cursor.close()
            con.close()
            
    @classmethod
    def obtener_todas(cls, mysql):
        con = mysql.connect()
        cursor = con.cursor()  # Para que devuelva dicts y no tuplas
        try:
            cursor.execute("""
                SELECT id, nombre, email, tipo, mensaje, 
                fecha, resuelta FROM incidencias ORDER BY fecha DESC;
            """)
            rows = cursor.fetchall()
            incidencias = []
            for incidencia in rows:
                fecha_formateada = incidencia[5].strftime('%Y-%m-%d %H:%M') if incidencia[5] else None
                incidencias_dict = Incidencia(
                    incidencia[0], incidencia[1], incidencia[2], incidencia[3], incidencia[4], fecha_formateada, incidencia[6]).to_dict()
                
                incidencias.append(incidencias_dict)
                
            return incidencias
        
        except Exception as e:
            print("Error en obtener_todas:", e)
            return []
        finally:
            cursor.close()
            con.close()