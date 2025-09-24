# models/ModelBloqueos.py
from entities.JuegosBloqueados import BloqueoJuego

class ModelBloqueos:
    @classmethod
    def obtener_usuarios(cls, mysql):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("SELECT id, nombre, correo FROM usuarios ORDER BY nombre ASC LIMIT 1000")
            rows = cursor.fetchall()
            
            resultado = []
            for row in rows:
                resultado.append({
                    "id": row[0],
                    "nombre": row[1],
                    "correo": row[2]
                })
            return resultado
        
        except Exception as e:
            print("Error en obtener_usuarios:", e)
            return []
        finally:
            cursor.close()
            con.close()

    @classmethod
    def obtener_juegos(cls, mysql):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("SELECT id, nombre FROM juegos ORDER BY nombre ASC")
            rows = cursor.fetchall()
            return rows
        except Exception as e:
            print("Error en obtener_juegos:", e)
            return []
        finally:
            cursor.close()
            con.close()
            
    @classmethod
    def crear_bloqueo(cls, mysql, usuario_id: int, juego_id: int, motivo: str = None, creado_por: int = None):
        """
        Crea un bloqueo activo para (usuario, juego).
        - Si ya existía activo: no hace nada y devuelve {"ok": False, "reason": "already_active"}.
        - Si existía inactivo: lo reactiva.
        - Si no existía: lo crea.
        """
        con = mysql.connect()
        cur = con.cursor()

        cur.execute("""
            SELECT id, activo FROM juegos_bloqueados
            WHERE usuario_id=%s AND juego_id=%s
        """, (usuario_id, juego_id))
        row = cur.fetchone()

        if row:
            bloqueo_id, activo = row
            if int(activo) == 1:
                cur.close()
                return {"ok": False, "reason": "already_active", "id": bloqueo_id}
            else:
                cur.execute("""
                    UPDATE juegos_bloqueados
                    SET activo=1, motivo=%s, creado_por=%s
                    WHERE id=%s
                """, (motivo, creado_por, bloqueo_id))
                con.commit()
                cur.close()
                return {"ok": True, "reactivado": True, "id": bloqueo_id}
        else:
            cur.execute("""
                INSERT INTO juegos_bloqueados (usuario_id, juego_id, motivo, creado_por, activo)
                VALUES (%s, %s, %s, %s, 1)
            """, (usuario_id, juego_id, motivo, creado_por))
            con.commit()
            bloqueo_id = cur.lastrowid
            cur.close()
            return {"ok": True, "reactivado": False, "id": bloqueo_id}

    @classmethod
    def listar(cls, mysql, search: str = None, limit: int = 50, offset: int = 0):
        """
        Lista bloqueos ACTIVOS, con datos de usuario y juego, para pintar la tabla del panel.
        Sigue el mismo estilo que get_all_juegos (cursor normal, acceso por índices).
        """
        con = mysql.connect()
        cursor = con.cursor()
        try:
            sql = """
                SELECT jb.id, jb.usuario_id, jb.juego_id, jb.activo, jb.motivo, jb.creado_por,
                    jb.created_at, jb.updated_at,
                    u.nombre AS usuario_nombre, u.correo AS usuario_email,
                    j.nombre AS juego_nombre
                FROM juegos_bloqueados jb
                JOIN usuarios u ON u.id = jb.usuario_id
                JOIN juegos j   ON j.id = jb.juego_id
                WHERE jb.activo = 1
            """
            params = []
            if search:
                sql += " AND (u.nombre LIKE %s OR u.correo LIKE %s OR j.nombre LIKE %s)"
                like = f"%{search}%"
                params.extend([like, like, like])

            sql += " ORDER BY jb.updated_at DESC LIMIT %s OFFSET %s"
            params.extend([limit, offset])

            cursor.execute(sql, tuple(params))
            rows = cursor.fetchall()

            bloqueos = []
            for row in rows:
                # Los primeros 8 campos son de la tabla juegos_bloqueados
                entidad = BloqueoJuego(
                    id=row[0],
                    usuario_id=row[1],
                    juego_id=row[2],
                    activo=row[3],
                    motivo=row[4],
                    creado_por=row[5],
                    created_at=row[6],
                    updated_at=row[7]
                ).to_dict()

                # Añadimos los alias del JOIN (índices 8, 9, 10)
                entidad["usuario_nombre"] = row[8]
                entidad["usuario_email"] = row[9]
                entidad["juego_nombre"] = row[10]

                bloqueos.append(entidad)

            return bloqueos
        except Exception as e:
            print("Error en listar bloqueos:", e)
            return []
        finally:
            cursor.close()
            con.close()

    @classmethod
    def contar(cls, mysql, search: str = None):
        con = mysql.connect()
        cur = con.cursor()
        sql = """
            SELECT COUNT(*)
            FROM juegos_bloqueados jb
            JOIN usuarios u ON u.id = jb.usuario_id
            JOIN juegos j   ON j.id = jb.juego_id
            WHERE jb.activo = 1
        """
        params = []
        if search:
            sql += " AND (u.nombre LIKE %s OR u.email LIKE %s OR j.nombre LIKE %s)"
            like = f"%{search}%"
            params.extend([like, like, like])

        cur.execute(sql, tuple(params))
        total = cur.fetchone()[0]
        cur.close()
        return total

    @classmethod
    def desbloquear(cls, mysql, bloqueo_id: int) -> bool:
        """
        Marca el bloqueo como inactivo (no borra la fila → deja historial).
        """
        con = mysql.connect()
        cur = con.cursor()
        cur.execute("UPDATE juegos_bloqueados SET activo=0 WHERE id=%s", (bloqueo_id,))
        con.commit()
        ok = cur.rowcount > 0
        cur.close()
        return ok

    @classmethod
    def esta_bloqueado(cls, mysql, usuario_id: int, juego_id: int) -> bool:
        """
        True si el juego está bloqueado para ese usuario (bloqueo individual activo).
        """
        con = mysql.connect()
        cur = con.cursor()
        cur.execute("""
            SELECT 1 FROM juegos_bloqueados
            WHERE usuario_id=%s AND juego_id=%s AND activo=1
            LIMIT 1
        """, (usuario_id, juego_id))
        row = cur.fetchone()
        cur.close()
        return bool(row)