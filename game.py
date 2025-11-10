class TicTacToe:
    def __init__(self):
        self.tablero = [" "] * 9
        self.turno_actual = "X"
        self.ganador = None
        self.juego_terminado = False

    def reiniciar(self):
        self.tablero = [" "] * 9
        self.turno_actual = "X"
        self.ganador = None
        self.juego_terminado = False

    def cargar_estado(self, tablero, turno_actual):
        self.tablero = tablero
        self.turno_actual = turno_actual
        self.verificar_ganador()
        self.verificar_empate()

    def hacer_movimiento(self, posicion):
        if self.juego_terminado:
            return False, "El juego ya terminó"

        if posicion < 0 or posicion > 8:
            return False, "Posición inválida"

        if self.tablero[posicion] != " ":
            return False, "Esa casilla ya está ocupada"

        self.tablero[posicion] = self.turno_actual

        if self.verificar_ganador():
            self.juego_terminado = True
            self.ganador = self.turno_actual
            return True, f"¡Jugador {self.turno_actual} gana!"

        if self.verificar_empate():
            self.juego_terminado = True
            return True, "¡Es un empate!"

        self.turno_actual = "O" if self.turno_actual == "X" else "X"
        return True, "Movimiento válido"

    def verificar_ganador(self):
        # Combinaciones ganadoras
        combinaciones = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],  # Filas
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],  # Columnas
            [0, 4, 8],
            [2, 4, 6],  # Diagonales
        ]

        for combo in combinaciones:
            if (
                self.tablero[combo[0]]
                == self.tablero[combo[1]]
                == self.tablero[combo[2]]
                != " "
            ):
                return True
        return False

    def verificar_empate(self):
        return " " not in self.tablero and not self.verificar_ganador()

    def obtener_estado(self):
        return {
            "tablero": self.tablero.copy(),
            "turno_actual": self.turno_actual,
            "ganador": self.ganador,
            "juego_terminado": self.juego_terminado,
        }

    def imprimir_tablero(self):
        print("\n")
        for i in range(0, 9, 3):
            print(
                f" {self.tablero[i]} | {self.tablero[i + 1]} | {self.tablero[i + 2]} "
            )
            if i < 6:
                print("-----------")
        print("\n")
