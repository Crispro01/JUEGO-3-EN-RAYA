import mysql.connector
from mysql.connector import Error


class Database:
    def __init__(
        self,
        host="localhost",
        user="root",
        password="Root@Pass123",
        database="tictactoe",
    ):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host, user=self.user, password=self.password
            )
            if self.connection.is_connected():
                cursor = self.connection.cursor()
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
                cursor.close()
                self.connection.close()

                self.connection = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                )
                self.create_tables()
                return True
        except Error as e:
            print(f"Error conectando a MySQL: {e}")
            return False

    def create_tables(self):
        cursor = self.connection.cursor()

        # Tabla de jugadores
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jugadores (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) UNIQUE NOT NULL,
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Tabla de partidas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS partidas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                jugador1_id INT,
                jugador2_id INT,
                ganador_id INT NULL,
                estado VARCHAR(20) DEFAULT 'en_curso',
                tablero TEXT,
                turno_actual VARCHAR(1),
                fecha_inicio DATETIME DEFAULT CURRENT_TIMESTAMP,
                fecha_fin DATETIME NULL,
                FOREIGN KEY (jugador1_id) REFERENCES jugadores(id),
                FOREIGN KEY (jugador2_id) REFERENCES jugadores(id),
                FOREIGN KEY (ganador_id) REFERENCES jugadores(id)
            )
        """)

        # Tabla de estadísticas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS estadisticas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                jugador_id INT,
                partidas_jugadas INT DEFAULT 0,
                partidas_ganadas INT DEFAULT 0,
                partidas_perdidas INT DEFAULT 0,
                empates INT DEFAULT 0,
                FOREIGN KEY (jugador_id) REFERENCES jugadores(id),
                UNIQUE KEY (jugador_id)
            )
        """)

        self.connection.commit()
        cursor.close()

    def crear_jugador(self, nombre):
        cursor = self.connection.cursor()
        try:
            cursor.execute("INSERT INTO jugadores (nombre) VALUES (%s)", (nombre,))
            jugador_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO estadisticas (jugador_id) VALUES (%s)", (jugador_id,)
            )
            self.connection.commit()
            return jugador_id
        except Error as e:
            print(f"Error creando jugador: {e}")
            return None
        finally:
            cursor.close()

    def obtener_jugadores(self):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM jugadores ORDER BY nombre")
        jugadores = cursor.fetchall()
        cursor.close()
        return jugadores

    def obtener_jugador_por_id(self, jugador_id):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM jugadores WHERE id = %s", (jugador_id,))
        jugador = cursor.fetchone()
        cursor.close()
        return jugador

    def crear_partida(self, jugador1_id, jugador2_id, tablero, turno_actual):
        cursor = self.connection.cursor()
        tablero_str = ",".join(tablero)
        cursor.execute(
            """
            INSERT INTO partidas (jugador1_id, jugador2_id, tablero, turno_actual, estado)
            VALUES (%s, %s, %s, %s, 'en_curso')
        """,
            (jugador1_id, jugador2_id, tablero_str, turno_actual),
        )
        partida_id = cursor.lastrowid
        self.connection.commit()
        cursor.close()
        return partida_id

    def actualizar_partida(
        self, partida_id, tablero, turno_actual, estado="en_curso", ganador_id=None
    ):
        cursor = self.connection.cursor()
        tablero_str = ",".join(tablero)

        if estado == "finalizada":
            cursor.execute(
                """
                UPDATE partidas 
                SET tablero = %s, turno_actual = %s, estado = %s, ganador_id = %s, fecha_fin = NOW()
                WHERE id = %s
            """,
                (tablero_str, turno_actual, estado, ganador_id, partida_id),
            )
        else:
            cursor.execute(
                """
                UPDATE partidas 
                SET tablero = %s, turno_actual = %s, estado = %s
                WHERE id = %s
            """,
                (tablero_str, turno_actual, estado, partida_id),
            )

        self.connection.commit()
        cursor.close()

    def obtener_partida(self, partida_id):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM partidas WHERE id = %s", (partida_id,))
        partida = cursor.fetchone()
        if partida and partida["tablero"]:
            partida["tablero"] = partida["tablero"].split(",")
        cursor.close()
        return partida

    def obtener_partidas_activas(self):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.*, 
                   j1.nombre as jugador1_nombre, 
                   j2.nombre as jugador2_nombre
            FROM partidas p
            JOIN jugadores j1 ON p.jugador1_id = j1.id
            JOIN jugadores j2 ON p.jugador2_id = j2.id
            WHERE p.estado = 'en_curso'
            ORDER BY p.fecha_inicio DESC
        """)
        partidas = cursor.fetchall()
        cursor.close()
        return partidas

    def actualizar_estadisticas(self, jugador1_id, jugador2_id, ganador_id):
        cursor = self.connection.cursor()

        # Actualizar estadísticas del jugador 1
        if ganador_id == jugador1_id:
            cursor.execute(
                """
                UPDATE estadisticas 
                SET partidas_jugadas = partidas_jugadas + 1,
                    partidas_ganadas = partidas_ganadas + 1
                WHERE jugador_id = %s
            """,
                (jugador1_id,),
            )
        elif ganador_id is None:  # Empate
            cursor.execute(
                """
                UPDATE estadisticas 
                SET partidas_jugadas = partidas_jugadas + 1,
                    empates = empates + 1
                WHERE jugador_id = %s
            """,
                (jugador1_id,),
            )
        else:
            cursor.execute(
                """
                UPDATE estadisticas 
                SET partidas_jugadas = partidas_jugadas + 1,
                    partidas_perdidas = partidas_perdidas + 1
                WHERE jugador_id = %s
            """,
                (jugador1_id,),
            )

        # Actualizar estadísticas del jugador 2
        if ganador_id == jugador2_id:
            cursor.execute(
                """
                UPDATE estadisticas 
                SET partidas_jugadas = partidas_jugadas + 1,
                    partidas_ganadas = partidas_ganadas + 1
                WHERE jugador_id = %s
            """,
                (jugador2_id,),
            )
        elif ganador_id is None:  # Empate
            cursor.execute(
                """
                UPDATE estadisticas 
                SET partidas_jugadas = partidas_jugadas + 1,
                    empates = empates + 1
                WHERE jugador_id = %s
            """,
                (jugador2_id,),
            )
        else:
            cursor.execute(
                """
                UPDATE estadisticas 
                SET partidas_jugadas = partidas_jugadas + 1,
                    partidas_perdidas = partidas_perdidas + 1
                WHERE jugador_id = %s
            """,
                (jugador2_id,),
            )

        self.connection.commit()
        cursor.close()

    def obtener_estadisticas(self, jugador_id):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT e.*, j.nombre
            FROM estadisticas e
            JOIN jugadores j ON e.jugador_id = j.id
            WHERE e.jugador_id = %s
        """,
            (jugador_id,),
        )
        stats = cursor.fetchone()
        cursor.close()
        return stats

    def obtener_todas_estadisticas(self):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT e.*, j.nombre
            FROM estadisticas e
            JOIN jugadores j ON e.jugador_id = j.id
            ORDER BY e.partidas_ganadas DESC
        """)
        stats = cursor.fetchall()
        cursor.close()
        return stats

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()


# FLUSH PRIVILEGES;
# ALTER USER 'root'@'localhost' IDENTIFIED BY 'Root@Pass123';
# FLUSH PRIVILEGES;
# exit;
