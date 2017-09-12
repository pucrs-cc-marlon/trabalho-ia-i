from collections import namedtuple
from random import randint

LIMPO = 0
PONTO_DE_INICIO = 1
PAREDE = 2
LIXO = 3
LIXEIRA = 4
CARREGADOR = 5

ASPIRADOR = 7

Ponto = namedtuple('Ponto', ['x', 'y'])


class Ambiente:

    def __init__(self, n=12, qtd_lixeiras=2, qtd_recargas=2):
        self.pontos_lixos = set()
        self.pontos_lixeiras = set()
        self.pontos_recargas = set()
        self.tamanho = n
        self.ambiente = self.gerar_ambiente(n, qtd_lixeiras, qtd_recargas)
        self.inicio = Ponto(0, 0)
        if self.inicio in self.pontos_lixos:
            self.pontos_lixos.remove(self.inicio)
        self.ambiente[self.inicio.y][self.inicio.x] = ASPIRADOR
        self.ambiente[n-1][n-1] = LIMPO

    def gerar_ambiente(self, n, qtd_lixeiras, qtd_recargas):
        ambiente = [[LIMPO for cell in range(n)] for row in range(n)]
        ambiente = self.colocar_materiais(ambiente, qtd_lixeiras, qtd_recargas)
        ambiente = self.colocar_lixo(ambiente)
        return ambiente

    def colocar_materiais(self, ambiente, qtd_lixeiras, qtd_recargas):
        ialtura_parede = self.tamanho / 3
        espaco_altura_parede = ialtura_parede/2

        ilargura_parede = self.tamanho / 3
        largura_parede = self.tamanho - ilargura_parede

        if self.tamanho > 5:
            for i in range(int(espaco_altura_parede), self.tamanho-int(espaco_altura_parede)):
                ambiente[i][int(ilargura_parede) - 1] = PAREDE
                ambiente[i][int(largura_parede)] = PAREDE
            # Colocando as Lixeiras
            for i in range(0, qtd_lixeiras):
                x1 = randint(0, self.tamanho - 1)
                y1 = randint(int(largura_parede) + 1, self.tamanho - 1)

                x2 = randint(0, self.tamanho - 1)
                y2 = randint(0, int(ilargura_parede) - 2)

                ambiente[x1][y1] = LIXEIRA
                ambiente[x2][y2] = LIXEIRA

                self.pontos_lixeiras.add(Ponto(x1, y1))
                self.pontos_lixeiras.add(Ponto(x2, y2))

            for i in range(0, qtd_recargas):
                x1 = randint(0, self.tamanho - 1)
                y1 = randint(int(largura_parede) + 1, self.tamanho - 1)

                x2 = randint(0, self.tamanho - 1)
                y2 = randint(0, int(ilargura_parede) - 2)

                ambiente[x1][y1] = CARREGADOR
                ambiente[x2][y2] = CARREGADOR

                self.pontos_recargas.add(Ponto(x1, y1))
                self.pontos_recargas.add(Ponto(x2, y2))

        else:
            for i in range(0, qtd_lixeiras):
                x1 = randint(0, self.tamanho - 1)
                y1 = randint(0, self.tamanho - 1)

                x2 = randint(0, self.tamanho - 1)
                y2 = randint(0, self.tamanho - 1)

                ambiente[x1][y1] = LIXEIRA
                ambiente[x2][y2] = LIXEIRA
                self.pontos_lixeiras.add(Ponto(x1, y1))
                self.pontos_lixeiras.add(Ponto(x2, y2))

            for i in range(0, qtd_recargas):
                x1 = randint(0, self.tamanho - 1)
                y1 = randint(0, self.tamanho - 1)

                x2 = randint(0, self.tamanho - 1)
                y2 = randint(0, self.tamanho - 1)

                ambiente[x1][y1] = CARREGADOR
                ambiente[x2][y2] = CARREGADOR

                self.pontos_recargas.add(Ponto(x1, y1))
                self.pontos_recargas.add(Ponto(x2, y2))
        return ambiente

    def colocar_lixo(self, ambiente):
        # Sorteia aleatóriamente a porcentagem de distribuição do Lixo
        total = self.tamanho * (randint(40, 85) / 100)
        for i in range(self.tamanho):
            for j in range(int(total)):
                pos = randint(0, self.tamanho - 1)
                if ambiente[i][pos] != PAREDE and ambiente[i][pos] != LIXEIRA and ambiente[i][pos] != CARREGADOR:
                    ambiente[i][pos] = LIXO
                    self.pontos_lixos.add(Ponto(pos, i))
        return ambiente

    def sucessores(self, x, y):
        n = []
        if x - 1 >= 0 and self.ambiente[y][x - 1] != PAREDE and self.ambiente[y][x - 1] != LIXEIRA \
                and self.ambiente[y][x - 1] != CARREGADOR:
            n.append(Ponto(x - 1, y))
        if x + 1 < len(self.ambiente) and self.ambiente[y][x + 1] != PAREDE and self.ambiente[y][x + 1] != LIXEIRA \
                and self.ambiente[y][x + 1] != CARREGADOR:
            n.append(Ponto(x + 1, y))
        if y - 1 >= 0 and self.ambiente[y - 1][x] != PAREDE and self.ambiente[y - 1][x] != LIXEIRA \
                and self.ambiente[y - 1][x] != CARREGADOR:
            n.append(Ponto(x, y - 1))
        if y + 1 < len(self.ambiente) and self.ambiente[y + 1][x] != PAREDE and self.ambiente[y + 1][x] != LIXEIRA \
                and self.ambiente[y + 1][x] != CARREGADOR:
            n.append(Ponto(x, y + 1))
        return n

    def situacao(self, x, y):
        if x >= 0 and y < len(self.ambiente):
            return self.ambiente[y][x]

    def limpar(self, x, y):
        if x >= 0 and y < len(self.ambiente):
            self.ambiente[y][x] = LIMPO
            self.pontos_lixos.remove(Ponto(x, y))

    def esta_sujo(self, x, y):
        if x >= 0 and y < len(self.ambiente):
            return self.ambiente[y][x] == LIXO

    def __str__(self):
        str_imprimir = "    "
        str_imprimir += " ".join([str(i) for i in range(self.tamanho)])
        str_imprimir += "\n    "
        str_imprimir += " ".join(["-" for i in range(self.tamanho)])
        str_imprimir += "\n"
        for i in range(len(self.ambiente)):
            str_imprimir += "{} - ".format(str(i))
            for j in range(len(self.ambiente[i])):
                # str_imprimir += "{}\n -\n ".format(str(j+1))
                str_imprimir += str(self.ambiente[i][j]) + " "
            str_imprimir += "\n"
        return str_imprimir


if __name__ == '__main__':
    ambiente = Ambiente(11, 2, 2)
    print(ambiente)
