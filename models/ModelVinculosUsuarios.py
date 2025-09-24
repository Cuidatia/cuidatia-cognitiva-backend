from flask import Flask, jsonify, request
from entities.VinculosUsuarios import VinculoUsuario

class ModelVinculoUsuario:

    @classmethod
    def _rol_de_usuario(cls, mysql, usuario_id: int):
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("SELECT id_rol FROM usuarios WHERE id = %s", (usuario_id,))
            row = cursor.fetchone()
            return row[0] if row else None
        finally:
            cursor.close()
            con.close()

    @classmethod
    def obtener_supervisores(cls, mysql):
        """
        Devuelve usuarios con id_rol 3 (familiar) o 4 (medico)
        """
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("""
                SELECT id, nombre, correo, id_rol
                FROM usuarios
                WHERE id_rol IN (3,4)
                ORDER BY nombre ASC
            """)
            rows = cursor.fetchall()
            # (id, nombre, email, id_rol) -> dict
            data = [
                {"id": r[0], "nombre": r[1], "correo": r[2], "id_rol": r[3]}
                for r in rows
            ]
            return data
        finally:
            cursor.close()
            con.close()

    @classmethod
    def obtener_pacientes(cls, mysql):
        """
        Devuelve usuarios con id_rol 1 (paciente/usuario)
        """
        con = mysql.connect()
        cursor = con.cursor()
        try:
            cursor.execute("""
                SELECT id, nombre, correo
                FROM usuarios
                WHERE id_rol = 1
                ORDER BY nombre ASC
            """)
            rows = cursor.fetchall()
            data = [{"id": r[0], "nombre": r[1], "correo": r[2]} for r in rows]
            return data
        finally:
            cursor.close()
            con.close()

    @classmethod
    def crear_vinculos_bulk(cls, mysql, supervisor_id, paciente_ids: list):
        """
        Crea vínculos (paciente -> supervisor) en lote:
        - Deduces tipo_vinculo desde id_rol del supervisor (3=familiar, 4=medico).
        - Evita duplicados: no inserta los que ya existan.
        - Devuelve cantidad insertada e ignorada.
        """
        # 1) Determinar tipo_vinculo por rol del supervisor
        id_rol = cls._rol_de_usuario(mysql, supervisor_id)
        if id_rol not in (3, 4):
            return {"error": "El supervisor no es familiar(3) ni médico(4)"}

        tipo_vinculo = "familiar" if id_rol == 3 else "medico"

        con = mysql.connect()
        cursor = con.cursor()
        try:
            # 2) Buscar vínculos ya existentes para este supervisor y tipo
            format_ids = ",".join(["%s"] * len(paciente_ids))
            cursor.execute(f"""
                SELECT paciente_id
                FROM vinculos_usuario
                WHERE supervisor_id = %s
                  AND tipo_vinculo = %s
                  AND paciente_id IN ({format_ids})
            """, (supervisor_id, tipo_vinculo, *paciente_ids))
            existentes = {row[0] for row in cursor.fetchall()}

            # 3) Calcular nuevos (los que no están)
            nuevos = [pid for pid in paciente_ids if pid not in existentes]
            if not nuevos:
                return {"insertados": 0, "ignorados": len(paciente_ids)}

            # 4) Insertar en lote
            valores = [(pid, supervisor_id, tipo_vinculo) for pid in nuevos]
            cursor.executemany("""
                INSERT INTO vinculos_usuario (paciente_id, supervisor_id, tipo_vinculo, fecha_vinculo)
                VALUES (%s, %s, %s, NOW())
            """, valores)
            con.commit()

            return {"insertados": cursor.rowcount, "ignorados": len(paciente_ids) - len(nuevos)}
        except Exception as e:
            print("Error en crear_vinculos_bulk:", e)
            return {"error": str(e)}
        finally:
            cursor.close()
            con.close()
    
    @classmethod
    def listar(cls, mysql):
        con = mysql.connect()
        cur = con.cursor()
        try:
            cur.execute("""
                SELECT v.id, v.paciente_id, v.supervisor_id, v.tipo_vinculo, v.fecha_vinculo,
                    u_sup.nombre AS supervisor_nombre,
                    u_sup.correo  AS supervisor_email,
                    u_pac.nombre AS paciente_nombre,
                    u_pac.correo  AS paciente_email
                FROM vinculos_usuario v
                JOIN usuarios u_sup ON u_sup.id = v.supervisor_id
                JOIN usuarios u_pac ON u_pac.id = v.paciente_id
                ORDER BY v.fecha_vinculo DESC
            """)
            rows = cur.fetchall()

            resultado = []
            for row in rows:
                resultado.append({
                    "id": row[0],
                    "paciente_id": row[1],
                    "supervisor_id": row[2],
                    "tipo_vinculo": row[3],
                    "fecha_vinculo": row[4],
                    "supervisor_nombre": row[5],
                    "supervisor_email": row[6],
                    "paciente_nombre": row[7],
                    "paciente_email": row[8],
                })
            return resultado
        finally:
            cur.close()
            con.close()

            
    @classmethod
    def eliminar_vinculo(cls, mysql, paciente_id, supervisor_id):
        con = mysql.connect()
        cur = con.cursor()
        try:
            cur.execute("""
                DELETE FROM vinculos_usuario
                WHERE paciente_id = %s AND supervisor_id = %s
            """, (paciente_id, supervisor_id))
            con.commit()
            return cur.rowcount > 0  # True si eliminó algo
        finally:
            cur.close()
            con.close()
    