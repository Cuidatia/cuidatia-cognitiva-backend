from flask import Flask, jsonify, request
from entities.Roles import Rol

class ModelRol:
    @classmethod
    def get_all_roles(cls, mysql):
        con= mysql.connect()
        cursor = con.cursor()
        
        try:
            cursor.execute(""" 

                select * from roles;

            """)

            rows=cursor.fetchall()
            
            roles = []
            for rol in rows:
                rol.append(Rol(rol[0],rol[1]).to_dict())

            return roles
        except Exception as e:
            return e