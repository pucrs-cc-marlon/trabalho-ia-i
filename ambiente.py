from random import randint

LIMPO = 0
PONTO_DE_INICIO = 1
PAREDE = 2
LIXO = 3
LIXEIRA = 4
CARREGADOR = 5


class Ambiente:

    def __init__(self, n=12, t=10, c=0):
        self.ambiente = self.gerar_ambiente(n)
        self.aspirador = self.criar_aspirador(t, c)

    def gerar_ambiente(self, n):
        mapa = [[LIMPO for cell in range(n)] for row in range(n)]

        mapa = self.colocar_paredes(mapa)

        mapa = self.colocar_lixo(mapa)
        return mapa

    def colocar_paredes(self, mapa):
        # TODO: Colocar as LIXEIRAS e o CARREGADOR
        ialtura_parede = len(mapa) / 3
        espaco_altura_parede = ialtura_parede/2

        ilargura_parede = len(mapa) / 3
        largura_parede = len(mapa) - ilargura_parede

        if len(mapa) > 5:
            for i in range(int(espaco_altura_parede), len(mapa)-int(espaco_altura_parede)):
                mapa[i][int(ilargura_parede) - 1] = PAREDE
                mapa[i][int(largura_parede)] = PAREDE
            # Colocando as Lixeiras
            for i in range(0, 3):
                mapa[randint(0, len(mapa) - 1)][randint(int(largura_parede) + 1, len(mapa) - 1)] = LIXEIRA
                mapa[randint(0, len(mapa) - 1)][randint(0, int(ilargura_parede) - 2)] = LIXEIRA

            for i in range(0, 2):
                mapa[randint(0, len(mapa) - 1)][randint(int(largura_parede) + 1, len(mapa) - 1)] = CARREGADOR
                mapa[randint(0, len(mapa) - 1)][randint(0, int(ilargura_parede) - 2)] = CARREGADOR
        else:
            for i in range(0, 3):
                mapa[randint(0, len(mapa) - 1)][randint(0, len(mapa) - 1)] = LIXEIRA
                mapa[randint(0, len(mapa) - 1)][randint(0, len(mapa) - 1)] = LIXEIRA

            for i in range(0, 2):
                mapa[randint(0, len(mapa) - 1)][randint(0, len(mapa) - 1)] = CARREGADOR
                mapa[randint(0, len(mapa) - 1)][randint(0, len(mapa) - 1)] = CARREGADOR

        return mapa

    def colocar_lixo(self, mapa):
        # Sorteia aleatóriamente a porcentagem de distribuição do Lixo
        total = len(mapa) * (randint(40, 85) / 100)
        for i in range(len(mapa)):
            for j in range(int(total)):
                pos = randint(0, len(mapa) - 1)
                if mapa[i][pos] != PAREDE and mapa[i][pos] != LIXEIRA and mapa[i][pos] != CARREGADOR:
                    mapa[i][pos] = LIXO
        return mapa

    def imprimir_ambiente(self):
        str_imprimir = ""
        for i in range(len(self.ambiente)):
            for j in range(len(self.ambiente[i])):
                str_imprimir += str(self.ambiente[i][j]) + " "
            print(str_imprimir)
            str_imprimir = ""

    def criar_aspirador(self, t, c):
        pass


if __name__ == '__main__':
    ambiente = Ambiente(n=12)
    ambiente.imprimir_ambiente()
