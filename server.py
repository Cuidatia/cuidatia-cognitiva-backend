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
from models.ModelSeguimiento import ModelSeguimiento
from models.ModelInvitaciones import ModelInvitacion
from models.ModelBloqueos import ModelBloqueos
from models.ModelVinculosUsuarios import ModelVinculoUsuario
from flaskext.mysql import MySQL
from werkzeug.utils import secure_filename
import os
import uuid 
from datetime import datetime, timedelta
from flask_socketio import SocketIO, emit, join_room, leave_room
from models.ModelChat import ModelChat

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
CORS(app, supports_credentials=True, origins=[
         "http://localhost:3000",   # solo sirve en tu PC
         "https://cuidatiacognitiva.adiper.es"  # producción real
     ])

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AVATAR_FOLDER = os.path.join(BASE_DIR, 'public', 'avatars')
IMAGE_FOLDER = os.path.join(BASE_DIR, 'public', 'events')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['AVATAR_FOLDER'] = AVATAR_FOLDER
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER

# === SocketIO ===
socketio = SocketIO(
    app,
    cors_allowed_origins=[
        "http://localhost:3000", "http://127.0.0.1:3000",
        "https://cuidatiacognitiva.adiper.es"
    ],
    async_mode="eventlet"  # usa eventlet
)

# Canal global (sin salas por ahora)
@socketio.on('connect')
def handle_connect():
    print("Cliente conectado al chat.")

@socketio.on('disconnect')
def handle_disconnect():
    print("Cliente desconectado del chat.")

@socketio.on('send_message')
def handle_send_message(data):
    usuario_id = data.get('usuario_id')
    usuario_nombre = data.get('usuario', 'Anónimo')
    mensaje = data.get('mensaje')

    print(f"📩 Nuevo mensaje de {usuario_nombre}: {mensaje}")

    # Guardar en BD
    ok = ModelChat.guardar_mensaje(mysql, usuario_id, mensaje)

    if ok:
        emit('receive_message', {
            "usuario": usuario_nombre,
            "usuario_id": usuario_id,
            "mensaje": mensaje
        }, broadcast=True)
    else:
        emit('error', {"error": "No se pudo guardar el mensaje."})

# BACKEND DEL USUARIOS

@app.route("/chat/mensajes", methods=["GET"])
def obtener_mensajes_chat():
    try:
        mensajes = ModelChat.obtener_mensajes(mysql, limite=20)
        return jsonify({"mensajes": mensajes}), 200
    except Exception as e:
        print("Error en obtener_mensajes_chat:", e)
        return jsonify({"error": str(e)}), 500

## SUBIR AVATAR

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/avatars/<path:filename>')
def serve_avatar(filename):
    return send_from_directory(AVATAR_FOLDER, filename)

@app.route('/events/<path:filename>')
def serve_image(filename):
    return send_from_directory(IMAGE_FOLDER, filename)

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
        avatar_url = f"avatars/{filename}"
        
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
    
    if "error" in resultado:
        status = 403 if resultado.get("code") == "disabled" else 401
        return jsonify(resultado), status

    
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
        usuario_id = request.args.get("usuario_id", type=int)
        juegos = ModelJuegos.get_all_juegos(mysql, usuario_id)
        return jsonify({'juegos': juegos})
    except Exception as e:
        return jsonify({'error': str(e)})

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
    nivel_id = data.get('nivel_id')
    usuario_id = data.get('usuario_id')
    juego_id = data.get('juego_id')

    if not usuario_id or not nivel_id:
        return jsonify({'error': 'Datos incompletos'}), 400
    
    resultado = ModelNivelJuegoUsuario.aumentar_nivel(mysql, juego_id, usuario_id, nivel_id)
    
    if 'error' in resultado:
        return jsonify(resultado), 500
    else:
        return jsonify({'mensaje': 'Nivel actualizado correctamente'}), 200
    


usuarios_admin = Blueprint('usuarios_admin', __name__)

@app.route('/admin/usuarios', methods=['GET'])
def get_usuarios():
    try:
        usuarios = ModelUsuarios.obtener_todos(mysql)
        return jsonify(usuarios), 200  # 👈 devuelve array directo
    except Exception as e:
        print(e)
        return jsonify([]), 500

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

@app.route('/reseñas/destacadas', methods=['GET'])
def get_reseñas_destacadas():
    try:
        reseñas = ModelValoracion.obtener_reseñas_destacadas(mysql, limite=10)
        return jsonify({"reseñas": reseñas}), 200
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

@app.route('/admin/usuario/<int:id>', methods=['GET'])
def get_usuario_reporte(id):
    try:
        data = ModelUsuarios.obtener_reporte_usuario(mysql, id)
        return jsonify(data), 200
    except Exception as e:
        print("Error en get_usuario_reporte:", e)
        return jsonify({"error": str(e)}), 500

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

# Toggle resuelta
@app.route('/incidencias/<int:id>/toggle', methods=['PUT'])
def toggle_incidencia(id):
    con = mysql.connect()
    cursor = con.cursor()
    try:
        cursor.execute("SELECT resuelta FROM incidencias WHERE id = %s", (id,))
        current = cursor.fetchone()
        if not current:
            return jsonify({"error": "Incidencia no encontrada"}), 404

        nuevo_estado = 0 if current[0] else 1
        cursor.execute("UPDATE incidencias SET resuelta = %s WHERE id = %s", (nuevo_estado, id))
        con.commit()
        return jsonify({"id": id, "resuelta": nuevo_estado})
    finally:
        cursor.close()
        con.close()

# Eliminar incidencia
@app.route('/incidencias/<int:id>', methods=['DELETE'])
def delete_incidencia(id):
    con = mysql.connect()
    cursor = con.cursor()
    try:
        cursor.execute("DELETE FROM incidencias WHERE id = %s", (id,))
        con.commit()
        return jsonify({"message": "Incidencia eliminada", "id": id})
    finally:
        cursor.close()
        con.close()
        
# Invitar familiar desde el perfil de un usuario normal
@app.route("/invitar-familiar", methods=["POST"])
def invitar_familiar():
    data = request.get_json()
    correo = data.get("correo")
    usuario_id = data.get("usuario_id")

    if not correo or not usuario_id:
        return jsonify({"error": "Datos incompletos"}), 400

    try:
        ModelInvitacion.invitar_usuario(mysql, usuario_id, correo, "familiar")
        return jsonify({"message": "Invitación a familiar registrada correctamente"}), 200
    except Exception as e:
        print("Error al invitar familiar:", e)
        return jsonify({"error": "Error al registrar invitación"}), 500

# Invitar médico desde el panel del administrador
@app.route("/admin/invitar-medico", methods=["POST"])
def invitar_medico():
    data = request.get_json()
    correo = data.get("correo")

    if not correo:
        return jsonify({"error": "Correo requerido"}), 400

    try:
        ModelInvitacion.invitar_usuario(mysql, None, correo, "medico")
        return jsonify({"message": "Invitación a médico registrada correctamente"}), 200
    except Exception as e:
        print("Error al invitar médico:", e)
        return jsonify({"error": "Error al registrar invitación"}), 500

# Crear usuario a partir de una invitación (acción del admin)
@app.route("/admin/crear-usuario-invitado", methods=["POST"])
def crear_usuario_invitado():
    data = request.get_json()
    invitacion_id = data.get("invitacion_id")

    if not invitacion_id:
        return jsonify({"error": "ID de invitación requerido"}), 400

    try:
        resultado = ModelUsuarios.crear_usuario_desde_invitacion(mysql, invitacion_id)
        if "error" in resultado:
            return jsonify(resultado), 400
        return jsonify(resultado), 200
    except Exception as e:
        print("Error al crear usuario desde invitación:", e)
        return jsonify({"error": "Error interno del servidor"}), 500

# ==========================
# INVITACIONES (ADMIN)
# ==========================

# 📌 Listar invitaciones
@app.route("/admin/invitaciones", methods=["GET"])
def listar_invitaciones():
    try:
        resultado = ModelInvitacion.listar_invitaciones(mysql)
        return jsonify({"invitaciones": resultado}), 200
    except Exception as e:
        print("Error en /admin/invitaciones:", e)
        return jsonify({"error": str(e)}), 500


# 📌 Rechazar invitación
@app.route("/admin/rechazar-invitacion", methods=["POST"])
def rechazar_invitacion():
    data = request.get_json()
    invitacion_id = data.get("invitacion_id")

    if not invitacion_id:
        return jsonify({"error": "Falta el ID de la invitación"}), 400

    try:
        resultado = ModelInvitacion.rechazar_invitacion(mysql, invitacion_id)
        if "error" in resultado:
            return jsonify(resultado), 400
        return jsonify({"message": "Invitación rechazada correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/admin/buscar-usuarios", methods=["GET"])
def buscar_usuarios():
    nombre = request.args.get("nombre", "")
    con = mysql.connect()
    cursor = con.cursor()
    try:
        cursor.execute("""
            SELECT id, nombre, correo 
            FROM usuarios 
            WHERE id_rol = 1 AND nombre LIKE %s
        """, (f"%{nombre}%",))
        rows = cursor.fetchall()
        usuarios = [{"id": r[0], "nombre": r[1], "correo": r[2]} for r in rows]
        return jsonify({"usuarios": usuarios}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        con.close()

@app.route("/admin/crear-invitacion", methods=["POST"])
def crear_invitacion_admin():
    data = request.get_json()
    correo = data.get("correo")
    rol_destino = data.get("rol_destino")
    usuario_id = data.get("usuario_id")

    if not correo or not rol_destino or not usuario_id:
        return jsonify({"error": "Faltan datos"}), 400

    try:
        resultado = ModelInvitacion.invitar_usuario(mysql, usuario_id, correo, rol_destino)
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
    try:
        # Datos de texto desde FormData
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        categoria = request.form.get('categoria')
        plazas_totales = request.form.get('plazas_totales')
        ubicacion = request.form.get('ubicacion')
        localidad = request.form.get('localidad')
        fecha_evento = request.form.get('fecha_evento')
        activo = request.form.get('activo', 0)
        plazas_ocupadas = 0  # por defecto

        # Archivo
        if 'imagen' not in request.files:
            return jsonify({'error': 'Falta imagen'}), 400

        file = request.files['imagen']

        if file.filename == '' or not allowed_file(file.filename):
            return jsonify({'error': 'Archivo inválido'}), 400

        # Guardar la imagen
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['IMAGE_FOLDER'], filename)
        file.save(filepath)

        # Ruta relativa que guardarás en la BD
        imagen = f"events/{filename}"

        # Insertar en la BD
        evento_id = ModelEvento.registrar_evento(
            mysql, nombre, descripcion, categoria,
            plazas_ocupadas, plazas_totales, imagen,
            ubicacion, localidad, fecha_evento, activo
        )

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

@app.route("/usuarios/actualizar-datos", methods=["POST"])
def actualizar_datos_usuario():
    data = request.get_json()

    user_id = data.get("user_id")
    nombre = data.get("nombre")
    fecha_nacimiento = data.get("fecha_nacimiento")
    biografia = data.get("biografia")
    nueva_password = data.get("password")
    
    if not user_id:
        return jsonify({"error": "Usuario no autenticado"}), 401

    if not nombre or not fecha_nacimiento or not nueva_password:
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    try:
        resultado = ModelUsuarios.actualizar_datos(mysql, user_id, nombre, fecha_nacimiento, biografia, nueva_password)
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Panel de seguimiento: lista de pacientes vinculados a un supervisor (rol 3/4)
@app.route('/seguimiento/pacientes', methods=['GET'])
def get_pacientes_vinculados():
    supervisor_id = request.args.get('supervisor_id', type=int)
    if not supervisor_id:
        return jsonify({"error": "Falta supervisor_id"}), 400
    try:
        pacientes = ModelSeguimiento.obtener_pacientes_vinculados(mysql, supervisor_id)
        return jsonify({"pacientes": pacientes}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- Resumen detallado de un paciente (para tarjetas y modal)
@app.route('/seguimiento/paciente/<int:usuario_id>/resumen', methods=['GET'])
def get_resumen_paciente(usuario_id):
    try:
        resumen = ModelSeguimiento.obtener_resumen_paciente(mysql, usuario_id)
        return jsonify(resumen), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- Series (tiempo, actividad, registros) para gráficas con filtro
@app.route('/seguimiento/paciente/<int:usuario_id>/series', methods=['GET'])
def get_series_paciente(usuario_id):
    filtro = request.args.get('filtro', '7d')  # 7d | 30d | global
    try:
        series = ModelSeguimiento.obtener_series_paciente(mysql, usuario_id, filtro)
        return jsonify(series), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ====== Endpoints ADMIN para gestionar vínculos ======

# # Crear vínculo (ADMIN)
# @app.route('/admin/vinculos', methods=['POST'])
# def crear_vinculo():
#     data = request.get_json()
#     paciente_id = data.get('paciente_id')
#     supervisor_id = data.get('supervisor_id')
#     tipo_vinculo = data.get('tipo_vinculo')  # 'familiar' | 'medico'
    
#     print(data)

#     if not all([paciente_id, supervisor_id, tipo_vinculo]):
#         return jsonify({"error": "Faltan datos"}), 400

#     try:
#         ok = ModelSeguimiento.crear_vinculo(mysql, paciente_id, supervisor_id, tipo_vinculo)
#         if ok:
#             return jsonify({"message": "Vínculo creado"}), 201
#         return jsonify({"error": "No se pudo crear vínculo (¿duplicado?)"}), 409
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# Eliminar vínculo (ADMIN)
@app.route('/admin/vinculos', methods=['DELETE'])
def eliminar_vinculo():
    data = request.get_json()
    paciente_id = data.get('paciente_id')
    supervisor_id = data.get('supervisor_id')

    if not all([paciente_id, supervisor_id]):
        return jsonify({"error": "Faltan datos"}), 400

    try:
        ok = ModelSeguimiento.eliminar_vinculo(mysql, paciente_id, supervisor_id)
        if ok:
            return jsonify({"message": "Vínculo eliminado"}), 200
        return jsonify({"error": "Vínculo no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json()
    correo = data.get("correo")

    con = mysql.connect()
    cursor = con.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE correo = %s", (correo,))
    user = cursor.fetchone()

    if not user:
        return jsonify({"error": "Correo no registrado"}), 404

    # ✅ Generar token único con uuid
    token = str(uuid.uuid4())
    expira = datetime.now() + timedelta(hours=1)

    cursor.execute("""
        UPDATE usuarios 
        SET reset_token = %s, reset_token_expira = %s 
        WHERE correo = %s
    """, (token, expira, correo))
    con.commit()

    enlace = f"http://localhost:3000/resetear-contrasena?token={token}"
    print("🔗 Enlace de recuperación:", enlace)

    return jsonify({"message": "Se ha enviado un enlace de recuperación a tu correo (simulado)."}), 200

@app.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json()
    token = data.get("token")
    nueva_password = data.get("password")

    if not token or not nueva_password:
        return jsonify({"error": "Token y contraseña son obligatorios"}), 400

    try:
        result = ModelUsuarios.reset_password(mysql, token, nueva_password)
        if "error" in result:
            return jsonify(result), 400
        return jsonify(result), 200
    except Exception as e:
        print("Error en reset-password:", e)
        return jsonify({"error": "Error interno"}), 500

# === PER-USUARIO: listar bloqueos activos con búsqueda y paginación
@app.route('/admin/juegos-bloqueados', methods=['GET'])
def listar_bloqueos():
    search = request.args.get('q')
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    offset = (page - 1) * limit

    try:
        data = ModelBloqueos.listar(mysql, search, limit, offset)
        total = ModelBloqueos.contar(mysql, search)
        return jsonify({"data": data, "page": page, "limit": limit, "total": total}), 200
    except Exception as e:
        print("Error en listar_bloqueos:", e)
        return jsonify({"error": "Error interno"}), 500


# === PER-USUARIO: crear/reativar bloqueo
@app.route('/admin/juegos-bloqueados', methods=['POST'])
def crear_bloqueo():
    body = request.get_json() or {}
    usuario_id = body.get('usuario_id')
    juego_id   = body.get('juego_id')
    motivo     = body.get('motivo')

    if not usuario_id or not juego_id:
        return jsonify({"error": "usuario_id y juego_id son requeridos"}), 400

    try:
        creado_por = session.get('usuario_id')  # opcional: qué admin lo hizo
        res = ModelBloqueos.crear_bloqueo(mysql, int(usuario_id), int(juego_id), motivo, creado_por)

        if not res.get("ok") and res.get("reason") == "already_active":
            return jsonify({"ok": False, "message": "Ya estaba bloqueado", "id": res.get("id")}), 200

        return jsonify(res), 200
    except Exception as e:
        print("Error en crear_bloqueo:", e)
        return jsonify({"error": "Error interno"}), 500


# === PER-USUARIO: desbloquear
@app.route('/admin/juegos-bloqueados/<int:bloqueo_id>/desbloquear', methods=['PATCH'])
def desbloquear_bloqueo(bloqueo_id):
    try:
        ok = ModelBloqueos.desbloquear(mysql, bloqueo_id)
        if not ok:
            return jsonify({"error": "No se encontró el bloqueo o ya estaba inactivo"}), 404
        return jsonify({"ok": True}), 200
    except Exception as e:
        print("Error en desbloquear_bloqueo:", e)
        return jsonify({"error": "Error interno"}), 500

@app.route('/admin/vinculos', methods=['GET'])
def listar_vinculos():
    try:
        vinculos = ModelVinculoUsuario.listar(mysql)
        return jsonify(vinculos), 200
    except Exception as e:
        print("Error en listar_vinculos:", e)
        return jsonify({"error": str(e)}), 500

# --- Listar supervisores (roles 3 = familiar, 4 = medico)
@app.route("/admin/vinculos/supervisores", methods=["GET"])
def vinculos_supervisores():
    try:
        data = ModelVinculoUsuario.obtener_supervisores(mysql)  # [{id, nombre, email, id_rol}]
        return jsonify(data), 200
    except Exception as e:
        print("Error en vinculos_supervisores:", e)
        return jsonify({"error": "Error interno"}), 500

# --- Listar pacientes (rol 1)
@app.route("/admin/vinculos/pacientes", methods=["GET"])
def vinculos_pacientes():
    try:
        data = ModelVinculoUsuario.obtener_pacientes(mysql)  # [{id, nombre, email}]
        return jsonify(data), 200
    except Exception as e:
        print("Error en vinculos_pacientes:", e)
        return jsonify({"error": "Error interno"}), 500

# --- Crear vínculos en lote
@app.route("/admin/vinculos", methods=["POST"])
def crear_vinculos():
    body = request.get_json() or {}
    supervisor_id = body.get("supervisor_id")
    paciente_ids = body.get("paciente_ids")  # array de ints

    if not supervisor_id or not isinstance(paciente_ids, list) or len(paciente_ids) == 0:
        return jsonify({"error": "supervisor_id y paciente_ids[] son requeridos"}), 400

    try:
        res = ModelVinculoUsuario.crear_vinculos_bulk(mysql, int(supervisor_id), [int(x) for x in paciente_ids])
        return jsonify(res), 200
    except Exception as e:
        print("Error en crear_vinculos:", e)
        return jsonify({"error": "Error interno"}), 500

# === APOYO PARA SELECTS DEL PANEL ===
@app.route('/admin/usuarios/select', methods=['GET'])
def admin_listar_usuarios():
    try:
        usuarios = ModelBloqueos.obtener_usuarios(mysql)
        return jsonify(usuarios), 200
    except Exception as e:
        print("Error en admin_listar_usuarios:", e)
        return jsonify({"error": "Error interno"}), 500


@app.route('/admin/juegos', methods=['GET'])
def admin_listar_juegos():
    try:
        juegos = ModelBloqueos.obtener_juegos(mysql)
        return jsonify(juegos), 200
    except Exception as e:
        print("Error en admin_listar_juegos:", e)
        return jsonify({"error": "Error interno"}), 500

if __name__ == '__main__':
    
    cert="/home/ubuntu/fullchain.pem"
    key="/home/ubuntu/privkey.pem"
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5002, certfile=cert, keyfile=key)
    #socketio.run(app, debug=True, host='0.0.0.0', port=5002)
    #app.run(debug=True, host='127.0.0.1', port=5002)