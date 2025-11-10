import secrets

from database import Database
from flask import Flask, jsonify, render_template, request
from game import TicTacToe

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Inicializar base de datos
db = Database()
db.connect()

# Diccionario para almacenar juegos activos en memoria
juegos_activos = {}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/jugadores", methods=["GET"])
def obtener_jugadores():
    jugadores = db.obtener_jugadores()
    return jsonify(jugadores)


@app.route("/api/jugadores", methods=["POST"])
def crear_jugador():
    data = request.json
    nombre = data.get("nombre")

    if not nombre:
        return jsonify({"error": "El nombre es requerido"}), 400

    jugador_id = db.crear_jugador(nombre)

    if jugador_id:
        return jsonify(
            {
                "id": jugador_id,
                "nombre": nombre,
                "mensaje": "Jugador creado exitosamente",
            }
        )
    else:
        return jsonify(
            {"error": "No se pudo crear el jugador. Puede que el nombre ya exista."}
        ), 400


@app.route("/api/partida/nueva", methods=["POST"])
def nueva_partida():
    data = request.json
    jugador1_id = data.get("jugador1_id")
    jugador2_id = data.get("jugador2_id")

    if not jugador1_id or not jugador2_id:
        return jsonify({"error": "Se requieren dos jugadores"}), 400

    if jugador1_id == jugador2_id:
        return jsonify({"error": "Los jugadores deben ser diferentes"}), 400

    # Crear nueva instancia del juego
    juego = TicTacToe()

    # Guardar en base de datos
    partida_id = db.crear_partida(
        jugador1_id, jugador2_id, juego.tablero, juego.turno_actual
    )

    # Guardar en memoria
    juegos_activos[partida_id] = juego

    # Obtener nombres de jugadores
    jugador1 = db.obtener_jugador_por_id(jugador1_id)
    jugador2 = db.obtener_jugador_por_id(jugador2_id)

    return jsonify(
        {
            "partida_id": partida_id,
            "jugador1": jugador1,
            "jugador2": jugador2,
            "estado": juego.obtener_estado(),
        }
    )


@app.route("/api/partida/<int:partida_id>", methods=["GET"])
def obtener_partida(partida_id):
    # Buscar en memoria primero
    if partida_id in juegos_activos:
        juego = juegos_activos[partida_id]
    else:
        # Si no está en memoria, cargar de base de datos
        partida = db.obtener_partida(partida_id)
        if not partida:
            return jsonify({"error": "Partida no encontrada"}), 404

        juego = TicTacToe()
        juego.cargar_estado(partida["tablero"], partida["turno_actual"])
        juegos_activos[partida_id] = juego

    partida = db.obtener_partida(partida_id)
    jugador1 = db.obtener_jugador_por_id(partida["jugador1_id"])
    jugador2 = db.obtener_jugador_por_id(partida["jugador2_id"])

    return jsonify(
        {
            "partida_id": partida_id,
            "jugador1": jugador1,
            "jugador2": jugador2,
            "estado": juego.obtener_estado(),
        }
    )


@app.route("/api/partida/<int:partida_id>/movimiento", methods=["POST"])
def hacer_movimiento(partida_id):
    data = request.json
    posicion = data.get("posicion")

    if posicion is None:
        return jsonify({"error": "La posición es requerida"}), 400

    if partida_id not in juegos_activos:
        partida = db.obtener_partida(partida_id)
        if not partida:
            return jsonify({"error": "Partida no encontrada"}), 404

        juego = TicTacToe()
        juego.cargar_estado(partida["tablero"], partida["turno_actual"])
        juegos_activos[partida_id] = juego

    juego = juegos_activos[partida_id]
    exito, mensaje = juego.hacer_movimiento(posicion)

    if not exito:
        return jsonify({"error": mensaje}), 400

    # Actualizar en base de datos
    ganador_id = None
    estado = "en_curso"

    if juego.juego_terminado:
        estado = "finalizada"
        partida = db.obtener_partida(partida_id)

        if juego.ganador:
            # Determinar el ID del ganador
            if juego.ganador == "X":
                ganador_id = partida["jugador1_id"]
            else:
                ganador_id = partida["jugador2_id"]

        # Actualizar estadísticas
        db.actualizar_estadisticas(
            partida["jugador1_id"], partida["jugador2_id"], ganador_id
        )

    db.actualizar_partida(
        partida_id, juego.tablero, juego.turno_actual, estado, ganador_id
    )

    return jsonify({"mensaje": mensaje, "estado": juego.obtener_estado()})


@app.route("/api/partidas/activas", methods=["GET"])
def obtener_partidas_activas():
    partidas = db.obtener_partidas_activas()
    return jsonify(partidas)


@app.route("/api/estadisticas", methods=["GET"])
def obtener_estadisticas():
    stats = db.obtener_todas_estadisticas()
    return jsonify(stats)


@app.route("/api/estadisticas/<int:jugador_id>", methods=["GET"])
def obtener_estadisticas_jugador(jugador_id):
    stats = db.obtener_estadisticas(jugador_id)
    if stats:
        return jsonify(stats)
    else:
        return jsonify({"error": "Jugador no encontrado"}), 404


if __name__ == "__main__":
    app.run(debug=True, port=5000)
