from entities.ChatGeneral import Chat

class ModelChat:
    @classmethod
    def guardar_mensaje(cls, mysql, usuario_id, contenido):
        """Inserta un nuevo mensaje en la base de datos."""
        con = mysql.connect()
        cur = con.cursor()
        try:
            cur.execute("""
                INSERT INTO mensajes_chat (usuario_id, contenido)
                VALUES (%s, %s)
            """, (usuario_id, contenido))
            con.commit()
            return True
        except Exception as e:
            print("Error guardando mensaje:", e)
            return False
        finally:
            cur.close()
            con.close()

    @classmethod
    def obtener_mensajes(cls, mysql, limite=20):
        """Obtiene los últimos mensajes del chat global."""
        con = mysql.connect()
        cur = con.cursor()
        try:
            cur.execute("""
                SELECT m.id, m.usuario_id, m.contenido, m.fecha, u.nombre
                FROM mensajes_chat m
                LEFT JOIN usuarios u ON u.id = m.usuario_id
                ORDER BY m.fecha DESC
                LIMIT %s
            """, (limite,))
            rows = cur.fetchall()

            mensajes = []
            for r in rows:
                mensajes.append(Chat(*r).to_dict())

            # Invertimos para mostrar de más antiguo a más reciente
            return list(reversed(mensajes))
        except Exception as e:
            print("Error al obtener mensajes:", e)
            return []
        finally:
            cur.close()
            con.close()