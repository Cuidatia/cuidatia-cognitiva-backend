from flask import Flask, jsonify, session, request, send_from_directory, Blueprint

from flask_bcrypt import Bcrypt
from flask_cors import CORS, cross_origin
import mysql.connector
from models.ModelJuegos import ModelJuegos
from models.ModelUsuarios import ModelUsuarios
from models.ModelValoraciones import ModelValoracion
from models.ModelNivelesJuego import ModelNivelesJuego
from models.ModelNivelesJuegoUsuario import ModelNivelJuegoUsuario
from models.ModelActividadUsuario import ModelActividadUsuario
from models.ModelIncidencias import ModelIncidencias
from models.ModelEventos import ModelEvento
from models.ModelEventosUsuario import ModelEventosUsuario
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
    # ✅ Si contiene error, devolver 401
    if "error" in resultado:
        return jsonify(resultado), 401  # <- MUY IMPORTANTE

    # ✅ Si todo bien, devolver 200 OK
    return jsonify(resultado), 200
## MODIFICAR DATOS USAURIOS PERFIL

@app.route("/modificar", methods=["POST"])
def modificar():
    data = request.get_json()
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
        return jsonify({"usuarios": estadisticas}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
    
@app.route('/admin/graficas', methods=['GET'])
def get_graficas():
    try:
        filtro = request.args.get('filtro', '7d')
        graficas = ModelUsuarios.obtener_graficas(mysql, filtro)
        return jsonify({"graficas": graficas}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

@app.route('/admin/actividad-reciente', methods=['GET'])
def obtener_actividad_reciente():
    try:
        actividad = ModelActividadUsuario.obtener_actividad_reciente(mysql)
        return jsonify({"actividad": actividad}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

@app.route('/admin/incidencias', methods=['GET'])
def obtener_todas():
    try:
        incidencias = ModelIncidencias.obtener_todas(mysql)
        return jsonify({"incidencias": incidencias}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
    
@app.route("/admin/registrar-actividad", methods=["POST"])
def registrar_actividad():
    try:
        data = request.get_json()
        tipo_evento = data.get("tipo_evento")
        descripcion = data.get("descripcion")
        user = data.get("user")
        tiempo = data.get("tiempo")
    
        if not tipo_evento or not descripcion or not user: #or not usuario_correo
            return jsonify({"error": "Faltan campos requeridos"}), 400

        resultado = ModelActividadUsuario.registrar_actividad(mysql, user, tipo_evento, descripcion, tiempo) #, usuario_correo

        if "error" in resultado:
            return jsonify(resultado), 400

        return jsonify(resultado), 200

    except Exception as e:
        print("Error en /admin/registrar-actividad:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/mas-jugados', methods=['GET'])
def obtener_juegos_mas_jugados():
    try:
        juegos = ModelJuegos.obtener_mas_jugados(mysql)
        return jsonify({"juegos": juegos}), 200
    except Exception as e:
        print("Error al obtener juegos más jugados:", e)
        return jsonify({"error": "Error al obtener los juegos más jugados"}), 500

@app.route('/incidencias', methods=['POST'])
def insertar_incidencia():
    try:
        data = request.json
        nombre = data.get('nombre')
        email = data.get('email')
        tipo = data.get('tipo')
        mensaje = data.get('mensaje')
        
        actividad = ModelIncidencias.insertar_incidencia(mysql, nombre, email, tipo, mensaje)
        return jsonify({"actividad": actividad}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

@app.route('/api/valoraciones/eliminar', methods=['POST'])
def eliminar_valoracion():
    data = request.get_json()
    juego_id = data.get('juego_id')
    usuario_id = data.get('usuario_id')

    if not juego_id or not usuario_id:
        return jsonify({"error": "Faltan parámetros"}), 400

    try:
        resultado = ModelValoracion.eliminar_valoracion(mysql, juego_id, usuario_id)
        if resultado:
            return jsonify({"mensaje": "Reseña eliminada correctamente"}), 200
        else:
            return jsonify({"mensaje": "No se encontró reseña para eliminar"}), 404
    except Exception as e:
        print("Error al eliminar valoración:", e)
        return jsonify({"error": "Error al eliminar valoración"}), 500

@app.route('/usuario/actividad', methods=['GET'])
def obtener_actividad_usuario():
    usuario_id = request.args.get('usuario_id')  # Lo pasas en la URL, ej: /usuario/actividad?usuario_id=123

    if not usuario_id:
        return jsonify({'error': 'Falta usuario_id'}), 400

    try:
        actividad = ModelActividadUsuario.obtener_por_usuario(mysql, usuario_id)
        return jsonify(actividad), 200
    except Exception as e:
        print("Error al cargar registros:", e)
        return jsonify({"error": "Error al cargar registros"}), 500

@app.route('/juegos/todos', methods=['GET'])
def obtener_todos_los_juegos():
    try:
        juegos = ModelJuegos.obtener_todos(mysql)
        return jsonify({'juegos': juegos}), 200
    except Exception as e:
        print("Error al obtener juegos:", e)
        return jsonify({'error': 'Error interno'}), 500

@app.route('/admin/eliminar', methods=['POST'])
def eliminar_usuario():
    try:

        data = request.get_json()
        usuario_id = data.get("id")

        if not usuario_id:
            return jsonify({"error": "Falta el ID del usuario"}), 400

        eliminado = ModelUsuarios.eliminar_usuario(mysql, usuario_id)

        if eliminado:
            return jsonify({"message": "Usuario eliminado correctamente", "id": usuario_id}), 200
        else:
            return jsonify({"error": "Usuario no encontrado o no eliminado"}), 404

    except Exception as e:
        print("Error en /admin/eliminar:", e)
        return jsonify({"error": str(e)}), 500
    
@app.route('/admin/desactivar', methods=['POST'])
def desactivar_usuario():
    try:

        data = request.get_json()
        usuario_id = data.get("id")
        activo = data.get("activo")

        nuevo_estado = not activo
        eliminado = ModelUsuarios.desactivar_usuario(mysql, nuevo_estado, usuario_id)

        if eliminado:
            return jsonify({"message": "Usuario desactivado correctamente", "id": usuario_id}), 200
        else:
            return jsonify({"error": "Usuario no encontrado o no desactivado"}), 404

    except Exception as e:
        print("Error en /admin/desactivar:", e)
        return jsonify({"error": str(e)}), 500    
    
@app.route('/admin/bloquear-juego', methods=['POST'])
def bloquear_juego():
    data = request.get_json()
    juego_id = data.get('juego_id')
    bloquear = data.get('bloquear')

    if juego_id is None or bloquear is None:
        return jsonify({'error': 'Faltan datos'}), 400

    try:
        resultado = ModelJuegos.bloquear_juego(mysql, juego_id, bloquear)
        return jsonify({'success': True}), 200
    except Exception as e:
        print("Error al bloquear juego:", e)
        return jsonify({'error': 'Error interno'}), 500


# @app.route('/admin/crear-invitacion', methods=['POST'])
# def crear_invitacion():
#     data = request.get_json()
#     rol = data.get('rol')

#     if rol not in [3, 4]:
#         return jsonify({'error': 'Rol no permitido'}), 400

#     try:
#         import secrets
#         token = secrets.token_urlsafe(16)

#         # Guarda el token con el rol asociado (en tabla invitaciones)
#         resultado = ModelInvitaciones.guardar_invitacion(mysql, token, rol)
#         return jsonify({'token': token}), 200
#     except Exception as e:
#         print("Error al crear invitación:", e)
#         return jsonify({'error': 'Error interno'}), 500

# BACKEND DE EVENTOS
@app.route('/eventos', methods=['GET'])
def obtener_todos_eventos():
    try:
        eventos = ModelEvento.get_all_eventos(mysql)
        return jsonify({'eventos': eventos}), 200
    except Exception as e:
        print("Error al obtener eventos:", e)
        return jsonify({'error': 'Error al obtener eventos'}), 500

@app.route('/eventos/<int:evento_id>', methods=['GET'])
def obtener_evento(evento_id):
    try:
        evento = ModelEvento.get_evento(mysql, evento_id)
        return jsonify(evento), 200
    except Exception as e:
        print("Error al obtener el evento:", e)
        return jsonify({"error": "Error al obtener el evento"}), 500

@app.route('/eventos', methods=['POST'])
def registrar_evento():
    data = request.get_json()
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')
    categoria = data.get('categoria')
    plazas_ocupadas = data.get('plazas_ocupadas')
    plazas_totales = data.get('plazas_totales')
    imagen = data.get('imagen')
    ubicacion = data.get('ubicacion')
    localidad = data.get('localidad')
    fecha_evento = data.get('fecha_evento')
    activo = data.get('activo')

    try:        
        evento_id = ModelEvento.registrar_evento(mysql, nombre, descripcion, categoria, plazas_ocupadas, plazas_totales, imagen, ubicacion, localidad, fecha_evento, activo)
        return jsonify({"evento": {"id": evento_id}}), 201
    except Exception as e:
        print("Error al crear el evento:", e)
        return jsonify({"error": "Error al crear el evento"}), 500

@app.route('/eventos/<int:evento_id>', methods=['PUT'])
def modificar_evento(evento_id):
    evento = request.get_json()
    nombre = evento.get('nombre')
    descripcion = evento.get('descripcion')
    categoria = evento.get('categoria')
    plazas_ocupadas = evento.get('plazas_ocupadas', 0)
    plazas_totales = evento.get('plazas_totales')
    imagen = evento.get('imagen', '')
    ubicacion = evento.get('ubicacion')
    localidad = evento.get('localidad')
    fecha_evento = evento.get('fecha_evento')
    activo = evento.get('activo', 1)

    try:        
        success = ModelEvento.modificar_evento(mysql, evento_id, nombre, descripcion, categoria, plazas_ocupadas, plazas_totales, imagen, ubicacion, localidad, fecha_evento, activo)
        if success:
            evento_actualizado = ModelEvento.get_evento(mysql, evento_id)
            return jsonify({"success": True, "evento": evento_actualizado}), 200
        else:
            return jsonify({"success": False, "error": "No se pudo modificar el evento"}), 400
    except Exception as e:
        print("Error al crear el evento:", e)
        return jsonify({"error": "Error al crear el evento"}), 500

@app.route('/eventos/<int:evento_id>', methods=['DELETE'])
def eliminar_evento(evento_id):

    try:
        ModelEvento.eliminar_evento(mysql, evento_id)
        return jsonify({'message': 'Evento eliminado correctamente'}), 200
    except Exception as e:
        return jsonify({"error": "Error al eliminar evento"}), 500

# BACKEND DE EVENTOS USUARIO
@app.route('/inscripciones', methods=['GET'])
def obtener_todas_inscripciones():
    try:
        inscripciones = ModelEventosUsuario.get_all_eventos_usuario(mysql)
        return jsonify({'inscripciones': inscripciones}), 200
    except Exception as e:
        print("Error al obtener inscripciones:", e)
        return jsonify({'error': 'Error al obtener inscripciones'}), 500
    
@app.route('/inscripciones', methods=['GET'])
def obtener_inscripcion_usuario_evento():
    usuario_id = request.args.get('usuario_id')
    evento_id = request.args.get('evento_id')

    if not usuario_id or not evento_id:
        return jsonify({'error': 'Faltan parámetros usuario_id o evento_id'}), 400

    try:
        inscripcion = ModelEventosUsuario.get_inscripcion_usuario_evento(mysql, usuario_id, evento_id)
        if inscripcion is None:
            return jsonify([]), 200
        return jsonify([inscripcion]), 200
    except Exception as e:
        print("Error al obtener inscripción:", e)
        return jsonify({'error': 'Error al obtener inscripción'}), 500

@app.route('/eventos/<int:evento_id>/inscripciones', methods=['GET'])
def obtener_inscripciones_evento(evento_id):

    if not evento_id:
        return jsonify({'error': 'Falta evento_id'}), 400

    try:
        inscripciones = ModelEventosUsuario.obtener_inscritos_evento(mysql, evento_id)
        return jsonify(inscripciones), 200
    except Exception as e:
        print("Error al obtener usuarios inscritos:", e)
        return jsonify({"error": "Error al obtener usuarios inscritos"}), 500

@app.route('/usuarios/<int:usuario_id>/inscripciones', methods=['GET'])
def obtener_inscripciones_usuario(usuario_id):

    if not usuario_id:
        return jsonify({'error': 'Falta usuario_id'}), 400

    try:
        inscripciones = ModelEventosUsuario.obtener_eventos_usuario(mysql, usuario_id)
        return jsonify(inscripciones), 200
    except Exception as e:
        print("Error al obtener eventos inscritos:", e)
        return jsonify({"error": "Error al obtener eventos inscritos"}), 500

@app.route('/inscripciones', methods=['POST'])
def inscribir_usuario():
    data = request.get_json()
    evento_id = data.get('evento_id')
    usuario_id = data.get('usuario_id')
    participacion = data.get('participacion')

    try:        
        evento = ModelEventosUsuario.registrar_inscripcion(mysql, usuario_id, evento_id,  participacion)
        return jsonify(evento), 201
    except Exception as e:
        print("Error al crear la inscripcion:", e)
        return jsonify({"error": "Error al crear la inscripcion"}), 500

@app.route('/inscripciones/<int:inscripcion_id>/participacion', methods=['PUT'])
def participacion_usuario(inscripcion_id):
    data = request.get_json()
    inscripcion = data.get('mostrarInscripcion')
    participacion = inscripcion['participacion']

    try:        
        evento = ModelEventosUsuario.marcar_participacion(mysql, inscripcion_id, participacion)
        return jsonify(evento), 201
    except Exception as e:
        print("Error al marcar la participacion:", e)
        return jsonify({"error": "Error al marcar la participacion"}), 500

@app.route('/inscripciones', methods=['DELETE'])
def anular_inscripcion():
    data = request.get_json()
    usuario_id = data.get('usuario_id')
    evento_id = data.get('evento_id')

    try:
        ModelEventosUsuario.eliminar_inscripcion(mysql,usuario_id, evento_id)
        return jsonify({'message': 'Inscripcion anulada correctamente'}), 200
    except Exception as e:
        return jsonify({"error": "Error al anular la inscripcion"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
    #app.run(debug=True, host='127.0.0.1', port=5002)
