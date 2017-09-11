

MOVER_DIREITA = 0
MOVE_ESQUERDA = 1
MOVE_CIMA = 2
MOVE_BAIXO = 3


class Aspirador:

    def __init__(self, c, t):
        self.carga_maxima = c
        self.carga = c
        self.tamanho_repositorio = t
        self.repositorio = []

    def esta_cheio(self):
        return len(self.repositorio) >= self.tamanho_repositorio

    def nivel_critico_bateria(self):
        return ((self.carga/self.carga_maxima) * 100) <= 10.0
