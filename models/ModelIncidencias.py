from entities.Incidencias import Incidencia

class ModelIncidencias:

    @classmethod
    def insertar_incidencia(cls, mysql, nombre, email, tipo, mensaje):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("""
                INSERT INTO incidencias (nombre, email, tipo, mensaje)
                VALUES (%s, %s, %s, %s)
            """, (nombre, email, tipo, mensaje))
            con.commit()
            return {'mensaje': 'Incidencia registrada correctamente'}
        except Exception as e:
            print("Error al insertar incidencia:", e)
            return {'error': str(e)}
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
                incidencias_dict = Incidencia(
                    incidencia[0], incidencia[1], incidencia[2], incidencia[3], incidencia[4], incidencia[5].strftime('%Y-%m-%d'), incidencia[6]).to_dict()
                
                incidencias.append(incidencias_dict)
                
            return incidencias
        
        except Exception as e:
            print("Error en obtener_todas:", e)
            return []
        finally:
            cursor.close()
            con.close()