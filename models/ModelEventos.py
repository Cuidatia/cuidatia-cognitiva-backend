from entities.Eventos import Evento

### AÑADIR INACTIVO O ACTIVO COMO COLUMNA A EVENTO

class ModelEvento:
    @classmethod
    def get_all_eventos(cls,mysql):
        conn = mysql.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(""" SELECT * FROM eventos """)
            rows = cursor.fetchall()
            eventos= []
            for row in rows:
                evento = Evento(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],
                                    row[9],row[10],row[11])
                eventos.append(evento.to_dict())
            return eventos
        except Exception as e:
            return e
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def get_evento(cls, mysql, evento_id):
        conn = mysql.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(""" SELECT * FROM eventos WHERE id = %s """, (evento_id,))
            row = cursor.fetchone()
            fecha_evento_str = row[9].strftime('%Y-%m-%dT%H:%M:%S') if row[9] else '2000-01-01T00:00:00'
            evento= Evento(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],
                               fecha_evento_str,row[10],row[11])
            return evento.to_dict()
        except Exception as e:
            return e
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def registrar_evento(cls,mysql,nombre,descripcion,categoria,plazas_ocupadas,plazas_totales,imagen,
                         ubicacion,localidad,fecha_evento,activo):
        
        conn = mysql.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                           INSERT INTO eventos (nombre,descripcion,categoria,plazas_ocupadas,plazas_totales,imagen,
                         ubicacion,localidad,fecha_evento,activo,momento_insercion)
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW())
                           """, (nombre,descripcion,categoria,plazas_ocupadas,plazas_totales,imagen,
                         ubicacion,localidad,fecha_evento,activo))
            conn.commit()
            usuario_id = cursor.lastrowid
            return usuario_id
        except Exception as e:
            return e
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def modificar_evento(cls,mysql,evento_id,nombre,descripcion,categoria,plazas_ocupadas,plazas_totales,imagen,
                         ubicacion,localidad,fecha_evento,activo):
        conn = mysql.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                           UPDATE eventos SET nombre = %s, descripcion = %s, categoria = %s, plazas_ocupadas = %s, plazas_totales = %s,
                           imagen = %s, ubicacion = %s, localidad = %s, fecha_evento = %s, activo = %s WHERE id = %s
                           """, (nombre,descripcion,categoria,plazas_ocupadas,plazas_totales,imagen,
                         ubicacion,localidad,fecha_evento,activo, evento_id))
            conn.commit()
            return True
        except Exception as e:
            return e
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def eliminar_evento(cls,mysql,evento_id):
        conn = mysql.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(""" DELETE FROM eventos WHERE id = %s """, (evento_id))
            conn.commit()
            return True
        except Exception as e:
            return e
        finally:
            cursor.close()
            conn.close()