from queue import PriorityQueue

from copy import copy

from ambiente import Ponto, PAREDE, LIXEIRA, CARREGADOR, ASPIRADOR, LIMPO

MOVER_DIREITA = 0
MOVER_ESQUERDA = 1
MOVER_CIMA = 2
MOVER_BAIXO = 3
PARADO = 4

OBSTACULO = 8
FIM_AMBIENTE = 6

INFERIOR = 1
SUPERIOR = 2

CUSTO_MOVIMENTO = 0.5
CUSTO_ASPIRAR = 0.5

PORCENTAGEM_CRITICA = 10.0


class Aspirador:

    def __init__(self, c, t):
        self.carga_maxima = c
        self.carga = c
        self.tamanho_repositorio = t
        self.repositorio = []
        self.posicao = Ponto(0, 0)

    def repositorio_cheio(self):
        status = len(self.repositorio) >= self.tamanho_repositorio
        return status

    def nivel_critico_bateria(self):
        # Sendo 10% o nível crítico de bateria
        return ((self.carga/self.carga_maxima) * 100) <= PORCENTAGEM_CRITICA

    def mover_limpando(self, ambiente, direcao=MOVER_BAIXO):
        direcao = direcao
        while len(ambiente.pontos_lixos) != 0:
            if self.repositorio_cheio():
                self.descarregar(ambiente)
            if self.posicao == Ponto(ambiente.tamanho-1, ambiente.tamanho-1):
                self.buscar_lixo_restante(ambiente)
                break
            if direcao == MOVER_DIREITA:
                self.mover_direita(ambiente)
                if direcao == MOVER_CIMA:
                    self.mover_cima(ambiente)
                    direcao = MOVER_CIMA
                elif direcao == MOVER_BAIXO:
                    self.mover_baixo(ambiente)
                    direcao = MOVER_BAIXO
            elif direcao == MOVER_BAIXO:
                status = self.mover_baixo(ambiente)
                if status[0] is False:
                    if status[1] == OBSTACULO:
                        direcao = self.contornar_obstaculo_baixo(ambiente)
                    else:
                        self.mover_direita(ambiente)
                        direcao = MOVER_CIMA
            elif direcao == MOVER_CIMA:
                status = self.mover_cima(ambiente)
                if status[0] is False:
                    if status[1] == OBSTACULO:
                        direcao = self.contornar_obstaculo_cima(ambiente)
                    else:
                        self.mover_direita(ambiente)
                        direcao = MOVER_BAIXO

    def buscar_lixo_restante(self, ambiente):
        print("Buscando lixo restante")
        pontos_lixo = copy(ambiente.pontos_lixos)
        for i in pontos_lixo:
            caminho = self.solucao_a_estrela(ambiente, i)[1]
            for j in caminho:
                if j == MOVER_BAIXO:
                    self.mover_baixo(ambiente)
                elif j == MOVER_CIMA:
                    self.mover_cima(ambiente)
                elif j == MOVER_DIREITA:
                    self.mover_direita(ambiente)
                elif j == MOVER_ESQUERDA:
                    self.mover_esquerda(ambiente)

    def descarregar(self, ambiente):
        print("Deslocando para a lixeira")
        menor_distancia_lixeira = min(ambiente.pontos_lixos, key=self.heuristica_posicao)
        caminho = self.solucao_a_estrela(ambiente, menor_distancia_lixeira)[1]

        for j in caminho:
            if j == MOVER_BAIXO:
                self.mover_baixo(ambiente, False)
            elif j == MOVER_CIMA:
                self.mover_cima(ambiente, False)
            elif j == MOVER_DIREITA:
                self.mover_direita(ambiente, False)
            elif j == MOVER_ESQUERDA:
                self.mover_esquerda(ambiente, False)

        print("Descarregando o lixo")
        self.repositorio.clear()
        caminho.reverse()
        print("Voltando para o ponto de origem")
        for j in caminho:
            if j == MOVER_BAIXO:
                self.mover_baixo(ambiente, False)
            elif j == MOVER_CIMA:
                self.mover_cima(ambiente, False)
            elif j == MOVER_DIREITA:
                self.mover_direita(ambiente, False)
            elif j == MOVER_ESQUERDA:
                self.mover_esquerda(ambiente, False)

    def contornar_obstaculo_baixo(self, ambiente):
        status = self.mover_direita(ambiente)
        if status[0] is True:
            self.mover_baixo(ambiente)
            status = self.mover_baixo(ambiente)
            if status[1] == FIM_AMBIENTE:
                return MOVER_CIMA
            self.mover_baixo(ambiente)
            self.mover_esquerda(ambiente)
            return MOVER_BAIXO
        else:
            self.mover_esquerda(ambiente)
            self.mover_baixo(ambiente)
            status = self.mover_baixo(ambiente)
            if status[1] == FIM_AMBIENTE:
                return MOVER_CIMA
            self.mover_baixo(ambiente)
            self.mover_direita(ambiente)
            return MOVER_BAIXO

    def contornar_obstaculo_cima(self, ambiente):
        status = self.mover_direita(ambiente)
        if status[0] is True:
            self.mover_cima(ambiente)
            status = self.mover_cima(ambiente)
            if status[1] == FIM_AMBIENTE:
                return MOVER_BAIXO
            self.mover_cima(ambiente)
            self.mover_esquerda(ambiente)
            return MOVER_CIMA
        else:
            self.mover_esquerda(ambiente)
            self.mover_cima(ambiente)
            status = self.mover_baixo(ambiente)
            if status[1] == FIM_AMBIENTE:
                return MOVER_BAIXO
            self.mover_cima(ambiente)
            self.mover_direita(ambiente)
            return MOVER_CIMA

    def mover_direita(self, ambiente, limpar=True):
        if self.posicao.x + 1 < ambiente.tamanho:
            quadrado = ambiente.situacao(self.posicao.x + 1, self.posicao.y)
            if quadrado != PAREDE and quadrado != LIXEIRA and quadrado != CARREGADOR:
                antiga_posicao = self.posicao
                self.posicao = Ponto(self.posicao.x + 1, self.posicao.y)
                if limpar:
                    self.limpar(ambiente)
                ambiente.ambiente[self.posicao.y][self.posicao.x] = ASPIRADOR
                ambiente.ambiente[antiga_posicao.y][antiga_posicao.x] = LIMPO
                print(ambiente)
                return True, None
            else:
                return False, OBSTACULO
        return False, FIM_AMBIENTE

    def mover_esquerda(self, ambiente, limpar=True):
        if self.posicao.x - 1 >= 0:
            quadrado = ambiente.situacao(self.posicao.x - 1, self.posicao.y)
            if quadrado != PAREDE and quadrado != LIXEIRA and quadrado != CARREGADOR:
                antiga_posicao = self.posicao
                self.posicao = Ponto(self.posicao.x - 1, self.posicao.y)
                if limpar:
                    self.limpar(ambiente)
                ambiente.ambiente[self.posicao.y][self.posicao.x] = ASPIRADOR
                ambiente.ambiente[antiga_posicao.y][antiga_posicao.x] = LIMPO
                print(ambiente)
                return True, None
            else:
                return False, OBSTACULO
        return False, FIM_AMBIENTE

    def mover_baixo(self, ambiente, limpar=True):
        if self.posicao.y + 1 < ambiente.tamanho:
            quadrado = ambiente.situacao(self.posicao.x, self.posicao.y + 1)
            if quadrado != PAREDE and quadrado != LIXEIRA and quadrado != CARREGADOR:
                antiga_posicao = self.posicao
                self.posicao = Ponto(self.posicao.x, self.posicao.y + 1)
                if limpar:
                    self.limpar(ambiente)
                ambiente.ambiente[self.posicao.y][self.posicao.x] = ASPIRADOR
                ambiente.ambiente[antiga_posicao.y][antiga_posicao.x] = LIMPO
                print(ambiente)
                return True, None
            else:
                return False, OBSTACULO
        return False, FIM_AMBIENTE

    def mover_cima(self, ambiente, limpar=True):
        if self.posicao.y - 1 >= 0:
            quadrado = ambiente.situacao(self.posicao.x, self.posicao.y - 1)
            if quadrado != PAREDE and quadrado != LIXEIRA and quadrado != CARREGADOR:
                antiga_posicao = self.posicao
                self.posicao = Ponto(self.posicao.x, self.posicao.y - 1)
                if limpar:
                    self.limpar(ambiente)
                ambiente.ambiente[self.posicao.y][self.posicao.x] = ASPIRADOR
                ambiente.ambiente[antiga_posicao.y][antiga_posicao.x] = LIMPO
                print(ambiente)
                return True, None
            else:
                return False, OBSTACULO
        return False, FIM_AMBIENTE

    def limpar(self, ambiente):
        if ambiente.esta_sujo(self.posicao.x, self.posicao.y):
            ambiente.limpar(self.posicao.x, self.posicao.y)
            self.carga -= CUSTO_ASPIRAR
            self.repositorio.append(self.posicao)
            print("Limpou o {}".format(self.posicao))
            print("Repositório: {}".format(self.repositorio))

    def heuristica(self, p1, p2):
        # Manhattan distance
        return abs(p1.x - p2.x) + abs(p1.y - p2.y)

    def heuristica_posicao(self, p2):
        # Manhattan distance
        return abs(self.posicao.x - p2.x) + abs(self.posicao.y - p2.y)

    def busca_a_estrela(self, ambiente, objetivo):
        queue = PriorityQueue()  # Fila de Prioridade
        queue.put(self.posicao, 0)  # Adiciona o ponto de partida na fila
        custo = {self.posicao: 0}  # Custo inicial do ponto de partida
        chegou_no_destino = False  # Variável de controle para identificar se o algoritmo chegou no destino
        caminho = {}  # Dicionário para armazenar o caminho percorrido
        while not queue.empty():  # Enquanto a fila não estiver vazia
            point = queue.get()  # Remove e pega o elemento da fila
            if point == objetivo:  # Se ponto for o destino, para a recursão
                chegou_no_destino = True  # E sinaliza a variável de controle
                break
            for proximo in ambiente.sucessores(point.x, point.y):  # Pega os pontos sucessores do point
                n_custo = custo[point] + self.heuristica(point, proximo)  # f(n) = g(n) + h(n)
                if proximo not in custo or n_custo < custo[proximo]:  # Se o elemento não estiver no dicionário
                    # custo (ele não foi percorrido) OU se o custo atual for menor do custo armazenado
                    custo[proximo] = n_custo  # Armazena o custo do próximo nó
                    prioridade = n_custo + self.heuristica(objetivo, proximo)  #
                    queue.put(proximo, prioridade)  # Adiciona o nó na fila
                    caminho[proximo] = point  # Adiciona o nó no dicionário do caminho apontando para o próximo nó
        return caminho if chegou_no_destino else None, \
               custo[objetivo] if chegou_no_destino else None

    # ------------------------------------------
    # Solve
    # ------------------------------------------

    def solucao_a_estrela(self, ambiente, objetivo):
        caminho, custo = self.busca_a_estrela(ambiente, objetivo)  # Executa o método de busca A*
        caminho_final = []  # Lista contendo o caminho
        caminho_final_comandos = []  # Lista contendo o caminho
        node = objetivo  # O dicionário que é retornado começa do destino até a origem
        # (mas na pesquisa é feito da origem até o destino), então é armazenado o destino como ponto de partida
        if caminho is not None:  # Se o caminho for Nulo então não foi encontrado uma solução
            while node is not None and node in caminho:  # Enquanto o nó node não for nulo
                # (lembrando que vem de trás para frente) e o nó estiver no dicionário
                # (isso acontece no caso do ponto de partida já que ele não tem nó node a ele)
                atual = node  # Armazena o nó node
                node = caminho[node]  # armazena
                caminho_final_comandos.insert(0, self.direcao(node.x, node.y, atual.x, atual.y))  # Pega a direção de movimento
                caminho_final.insert(0, {"origem": node, "destino": atual})  # Pega a direção de movimento
        return caminho_final, caminho_final_comandos if caminho is not None else None, None

    def direcao(self, x1, y1, x2, y2):
        if x1 < x2:
            return MOVER_DIREITA
        elif x1 > x2:
            return MOVER_ESQUERDA
        elif y1 < y2:
            return MOVER_BAIXO
        elif y1 > y2:
            return MOVER_CIMA
        raise Exception("Unknown direction", x1, y1, x2, y2)
