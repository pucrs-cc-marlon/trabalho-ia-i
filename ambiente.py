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
        data = [[LIMPO for cell in range(n)] for row in range(n)]

        data = self.colocar_paredes(data)

        data = self.colocar_lixo(data)
        return data

    def colocar_paredes(self, data):
        # TODO: Colocar as LIXEIRAS e o CARREGADOR
        ialtura_parede = len(data)/3
        espaco_altura_parede = ialtura_parede/2

        ilargura_parede = len(data)/3
        largura_parede = len(data) - ilargura_parede
        # Colocando Paredes
        for i in range(int(espaco_altura_parede), len(data)-int(espaco_altura_parede)):
            data[i][int(ilargura_parede)-1] = PAREDE
            data[i][int(largura_parede)] = PAREDE

        return data

    def colocar_lixo(self, data):
        total = len(data) * (randint(40, 85) / 100)
        for i in range(len(data)):
            for j in range(int(total)):
                pos = randint(0, len(data) - 1)
                if data[i][pos] != PAREDE:
                    data[i][pos] = LIXO

        return data

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
