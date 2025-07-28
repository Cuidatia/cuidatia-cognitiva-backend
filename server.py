from flask import Flask, jsonify, request, send_from_directory, Blueprint

from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_cors import cross_origin
import mysql.connector
from models.ModelJuegos import ModelJuegos
from models.ModelUsuarios import ModelUsuarios
from models.ModelValoraciones import ModelValoracion
from models.ModelNivelesJuego import ModelNivelesJuego
from models.ModelNivelesJuegoUsuario import ModelNivelJuegoUsuario
from models.ModelActividadUsuario import ModelActividadUsuario
from models.ModelIncidencias import ModelIncidencias
from flaskext.mysql import MySQL
from werkzeug.utils import secure_filename
import os

mysql = MySQL()
app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt()

app.config["MYSQL_DATABASE_HOST"]	= "localhost"
app.config["MYSQL_DATABASE_PORT"]	= 3306
app.config["MYSQL_DATABASE_USER"]	= "root"
app.config["MYSQL_DATABASE_PASSWORD"]	= "mipassword"
#app.config["MYSQL_DATABASE_PASSWORD"]	= "root"
app.config["MYSQL_DATABASE_DB"] = "cuidatiacogdb"

mysql.init_app(app)
CORS(app, supports_credentials=True, origins="http://localhost:3000")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AVATAR_FOLDER = os.path.join(BASE_DIR, 'public', 'avatars')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['AVATAR_FOLDER'] = AVATAR_FOLDER

# BACKEND DEL USUARIOS

## SUBIR AVATAR

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/avatars/<path:filename>')
def serve_avatar(filename):
    return send_from_directory(AVATAR_FOLDER, filename)

@app.route('/subirAvatar', methods=['POST'])
def subir_avatar():
    if 'avatar' not in request.files or 'user_id' not in request.form:
        return jsonify({'error': 'Falta avatar o user_id'}), 400

    file = request.files['avatar']
    user_id = request.form['user_id']

    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Archivo inválido'}), 400

    filename = secure_filename(f"{user_id}_{file.filename}")
    file_path = os.path.join(app.config['AVATAR_FOLDER'], filename)
    
    try:
        file.save(file_path)
        avatar_url = f"/avatars/{filename}"
        
        con = mysql.connect()
        cursor = con.cursor()
        cursor.execute("UPDATE usuarios SET avatar_url = %s WHERE id = %s", (avatar_url, user_id))
        con.commit()
        return jsonify({'message': 'Avatar actualizado', 'avatar_url': avatar_url}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

## ELIMINAR AVATAR

@app.route('/eliminarAvatar', methods=['POST'])
def eliminar_avatar():
    data = request.json
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({'error': 'Falta user_id'}), 400
    try:
        
        con = mysql.connect()
        cursor = con.cursor()
        
        # Verifica si el usuario existe (opcional pero recomendable)
        cursor.execute("SELECT id FROM usuarios WHERE id = %s", (user_id,))
        if cursor.fetchone() is None:
            return jsonify({'error': 'Usuario no encontrado'}), 404

        # Obtener la URL del avatar actual
        cursor.execute("SELECT avatar_url FROM usuarios WHERE id = %s", (user_id,))
        result = cursor.fetchone()

        if not result:
            return jsonify({'error': 'Usuario no encontrado'}), 404

        avatar_url = result[0]
        
        # Ruta absoluta donde se guardan los avatares
        avatar_folder = os.path.join(os.getcwd(), 'public')
        print(avatar_folder)
        default_avatar_url = '/avatars/default-avatar.png'

        # Eliminar la imagen si no es la predeterminada
        if avatar_url != default_avatar_url:
            avatar_path = os.path.join(avatar_folder, avatar_url.lstrip('/'))
            if os.path.exists(avatar_path):
                os.remove(avatar_path)
        
        # Actualiza el avatar
        cursor.execute("UPDATE usuarios SET avatar_url = %s WHERE id = %s", (default_avatar_url, user_id))
        con.commit()

        return jsonify({'message': 'Avatar restablecido', 'default_avatar_url': default_avatar_url}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

## REGISTRAR USUARIOS

@app.route("/registro", methods=["POST"])
def registro():
    data = request.get_json()
    resultado = ModelUsuarios.registrar_usuario(mysql, data)
    return jsonify(resultado)

## LOGEAR USUARIOS

@app.route("/inicioSesion", methods=["POST"])
def login():
    data = request.get_json()
    resultado = ModelUsuarios.login_usuario(mysql, data)
    return jsonify(resultado)

## MODIFICAR DATOS USAURIOS PERFIL

@app.route("/modificar", methods=["POST"])
def modificar():
    data = request.get_json()
    print(data)
    try:
        resultado = ModelUsuarios.update_usuario(mysql, data)
        return jsonify(resultado),200
    except Exception as e:
        return jsonify({'error': e}), 400   

## SACAR LOS DATOS DEL USUARIO EN SU PERFIL

@app.route('/perfil', methods=['GET'])
def obtener_usuario():
    user_id = request.args.get('id')  # lee ?id=123 desde la URL
    if not user_id:
        return jsonify({'error': 'ID de usuario no proporcionado'}), 400
    
    resultado = ModelUsuarios.obtener_usuario_por_id(mysql, user_id)
    if resultado:
        return jsonify(resultado)
    else:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
# BACKEND DE JUEGOS

@app.route("/juegos")
def juegos():
    try:
        juegos = ModelJuegos.get_all_juegos(mysql)
        
        return jsonify({'juegos': juegos})
    except Exception as e:
        return jsonify({'error': e}) 

@app.route('/usuarios/<int:usuario_id>/calcular_exp', methods=['POST'])
def calcular_experiencia():
    user_id = request.args.get('id')
    data = request.get_json()
    resultado = ModelUsuarios.calcular_nivel_y_progreso(mysql, data)
    return jsonify(resultado)
    
    
    
@app.route('/juegos/<int:juego_id>/agregar_experiencia', methods=['POST'])
def agregar_experiencia(juego_id):
    try:
        data = request.get_json()
        resultado = ModelUsuarios.agregar_experiencia(mysql, data)
        return jsonify({'res':resultado}), 200 
    except Exception as e:
        print(e)
        return jsonify({'error': 'error'}), 400 
    
## SACA LAS VALORACIONES DE UN JUEGO EN /JUEGOS

@app.route('/api/valoraciones/obtener', methods=['POST'])
def obtener_valoracion():
    data = request.get_json()
    juego_id = data.get('juego_id')
    usuario_id = data.get('usuario_id')
    
    if not juego_id or not usuario_id:
        return jsonify({'error': 'Faltan datos'}), 400

    valoracion = ModelValoracion.obtener_valoracion(mysql, juego_id, usuario_id)
    if valoracion:
        return jsonify(valoracion)
    return jsonify({'mensaje': 'No hay valoración'}), 200

## GUARDA LA VALORACION DE UN JUEGO DENTRO DE ESTE /JUEGOS/JUSGO_ID

@app.route('/api/valoraciones/guardar', methods=['POST'])
def guardar_valoracion():
    data = request.get_json()
    required_fields = ['juego_id', 'usuario_id', 'puntuacion', 'comentario']
    
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Datos incompletos'}), 400

    # Si existe, editar; si no, crear
    existente = ModelValoracion.obtener_valoracion(mysql, data['juego_id'], data['usuario_id'])
    
    if existente:
        resultado = ModelValoracion.editar_valoracion(mysql, data)
        return jsonify(resultado), 200
    else:
        resultado = ModelValoracion.crear_valoracion(mysql, data)
        return jsonify(resultado), 201 

## SACA UN JUEGO EN CONCRETO POR SU ID

@app.route('/juegos/<int:juego_id>', methods=['GET'])
def obtener_juego_por_id(juego_id):
    juego = ModelJuegos.get_juego_by_id(mysql, juego_id)
    
    if juego:
        return jsonify({"juego": juego}), 200
    else:
        return jsonify({"error": "Juego no encontrado"}), 404

## SACA VARIOS DATOS DE UN JUEGO EN /JUEGOS

@app.route('/sacar_favorito', methods=['GET'])
def get_favorito():
    juego_id = request.args.get('juego_id')
    usuario_id = request.args.get('usuario_id')

    if not juego_id or not usuario_id:
        return jsonify({'error': 'Faltan datos'}), 400

    resultado = ModelNivelJuegoUsuario.get_favorito(mysql, juego_id, usuario_id)
    return jsonify(resultado),200

@app.route('/info_completa', methods=['GET'])
def info_completa_juego():
    juego_id = request.args.get('juego_id')

    if not juego_id:
        return jsonify({'error': 'Faltan datos'}), 400

    resultado = ModelJuegos.get_info_completa(mysql, juego_id)
    return jsonify(resultado)

## CADA VEZ QUE UN JEUGO SE JUEGA POR UNA PERSONA LOGUEADA SUBE EN 1 LAS VACES QUE SE HA JUGADO

@app.route('/jugar', methods=['POST'])
def jugar_juego():
    data = request.json
    juego_id = data.get('juego_id')

    if not juego_id:
        return jsonify({'error': 'Falta juego_id'}), 400

    resultado = ModelJuegos.incrementar_jugadas(mysql, juego_id)
    return jsonify(resultado)

@app.route('/juegos/<int:juego_id>/nivel-usuario', methods=['GET'])
def sacar_nivel(juego_id):
    usuario_id = request.args.get('usuario_id')

    if not usuario_id:
        return jsonify({'error': 'Falta usuario_id'}), 400
    
    resultado = ModelNivelJuegoUsuario.sacar_nivel(mysql, usuario_id, juego_id)
    return jsonify({'res':resultado}), 200

@app.route('/api/juegos/favorito', methods=['POST'])
def toggle_favorito():
    data = request.get_json()

    usuario_id = data.get('usuario_id')
    juego_id = data.get('juego_id')

    if not usuario_id or not juego_id:
        return jsonify({'error': 'Faltan datos'}), 400

    resultado = ModelNivelJuegoUsuario.toggle_favorito(mysql, usuario_id, juego_id)

    if 'error' in resultado:
        return jsonify(resultado), 500
    else:
        return jsonify(resultado), 200

@app.route('/juegos/<int:juego_id>/nivel-usuario', methods=['POST'])
def aumentar_nivel(juego_id):
    data = request.json
    nivel_id = data.get('nuevo_nivel')
    usuario_id = data.get('usuario_id')
    juego_id = data.get('juego_id')
    
    print(juego_id, usuario_id, nivel_id)

    if not usuario_id or not nivel_id:
        return jsonify({'error': 'Datos incompletos'}), 400
    
    resultado = ModelNivelJuegoUsuario.aumentar_nivel(mysql, juego_id, usuario_id, nivel_id)
    return jsonify({'mensaje': 'Nivel actualizado correctamente'}), 200


usuarios_admin = Blueprint('usuarios_admin', __name__)

@app.route('/admin/usuarios', methods=['GET'])
def get_usuarios():
    try:
        usuarios = ModelUsuarios.obtener_todos(mysql)
        return jsonify({"usuarios": usuarios}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

@app.route('/admin/estadisticas', methods=['GET'])
def get_estadisticas():
    try:
        estadisticas = ModelUsuarios.obtener_estadisticas(mysql)
        print(estadisticas)
        return jsonify({"usuarios": estadisticas}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

@app.route('/admin/actividad-reciente', methods=['GET'])
def obtener_actividad_reciente():
    try:
        actividad = ModelActividadUsuario.obtener_actividad_reciente(mysql)
        print(actividad)
        return jsonify({"actividad": actividad}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

@app.route('/incidencias', methods=['GET'])
def obtener_todas():
    try:
        incidencias = ModelIncidencias.obtener_todas(mysql)
        print(incidencias)
        return jsonify({"actividad": incidencias}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

@app.route('/admin/actividad-reciente', methods=['GET'])
def insertar_incidencia():
    try:
        data = request.json
        nombre = data.get('nombre')
        email = data.get('email')
        tipo = data.get('tipo')
        mensaje = data.get('mensaje')
    
        print(nombre, email, tipo, mensaje)
        
        actividad = ModelIncidencias.insertar_incidencia(mysql)
        print(actividad)
        return jsonify({"actividad": actividad}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
