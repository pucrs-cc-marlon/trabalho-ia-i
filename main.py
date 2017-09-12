from aspirador import *
from ambiente import *


class Main:
    def __init__(self):
        self.ambiente = Ambiente(12, 1, 1)
        self.aspirador = Aspirador(10, 10)
        self.aspirador.mover_limpando(self.ambiente)

        print(self.ambiente)


if __name__ == "__main__":
    main = Main()
