from random import choice
from queue import PriorityQueue

from ambiente import Ponto, PAREDE, LIXEIRA, CARREGADOR

MOVER_DIREITA = 0
MOVER_ESQUERDA = 1
MOVER_CIMA = 2
MOVER_BAIXO = 3
PARADO = 4
DIRECOES = [MOVER_DIREITA, MOVER_ESQUERDA, MOVER_CIMA, MOVER_BAIXO]

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
        self.ultimo_movimento = PARADO

    def repositorio_cheio(self):
        return len(self.repositorio) >= self.tamanho_repositorio

    def nivel_critico_bateria(self):
        # Sendo 10% o nível crítico de bateria
        return ((self.carga/self.carga_maxima) * 100) <= PORCENTAGEM_CRITICA

    def mover_limpando(self, ambiente, direcao=MOVER_DIREITA):
        while len(ambiente.pontos_lixos) != 0:
            self.limpar(ambiente)
            print(ambiente)
            if direcao == MOVER_DIREITA:
                status = self.mover_direita(ambiente)
                if status is False:
                    self.mover_limpando(ambiente, choice(DIRECOES))
            if direcao == MOVER_ESQUERDA:
                status = self.mover_esquerda(ambiente)
                if status is False:
                    self.mover_limpando(ambiente, choice(DIRECOES))
            if direcao == MOVER_BAIXO:
                status = self.mover_baixo(ambiente)
                if status is False:
                    self.mover_limpando(ambiente, choice(DIRECOES))
            if direcao == MOVER_CIMA:
                status = self.mover_cima(ambiente)
                if status is False:
                    self.mover_limpando(ambiente, choice(DIRECOES))

    def mover_direita(self, ambiente):
        self.ultimo_movimento = MOVER_DIREITA
        if self.posicao.x + 1 < len(ambiente.ambiente):
            quadrado = ambiente.situacao(self.posicao.x + 1, self.posicao.y)
            if quadrado != PAREDE and quadrado != LIXEIRA and quadrado != CARREGADOR:
                self.posicao = Ponto(self.posicao.x + 1, self.posicao.y)
                return True
        return False

    def mover_esquerda(self, ambiente):
        self.ultimo_movimento = MOVER_ESQUERDA
        if self.posicao.x - 1 < 0:
            quadrado = ambiente.situacao(self.posicao.x - 1, self.posicao.y)
            if quadrado != PAREDE and quadrado != LIXEIRA and quadrado != CARREGADOR:
                self.posicao = Ponto(self.posicao.x - 1, self.posicao.y)
                return True
        return False

    def mover_baixo(self, ambiente):
        self.ultimo_movimento = MOVER_BAIXO
        if self.posicao.y + 1 < len(ambiente.ambiente):
            quadrado = ambiente.situacao(self.posicao.x, self.posicao.y + 1)
            if quadrado != PAREDE and quadrado != LIXEIRA and quadrado != CARREGADOR:
                self.posicao = Ponto(self.posicao.x, self.posicao.y + 1)
                return True
        return False

    def mover_cima(self, ambiente):
        self.ultimo_movimento = MOVER_CIMA
        if self.posicao.y - 1 < 0:
            quadrado = ambiente.situacao(self.posicao.x, self.posicao.y - 1)
            if quadrado != PAREDE and quadrado != LIXEIRA and quadrado != CARREGADOR:
                self.posicao = Ponto(self.posicao.x, self.posicao.y - 1)
                return True
        return False

    def limpar(self, ambiente):
        if ambiente.esta_sujo(self.posicao.x, self.posicao.y):
            ambiente.limpar(self.posicao.x, self.posicao.y)
            self.carga -= CUSTO_ASPIRAR
        if self.repositorio_cheio():
            pass  # TODO: Criar a função para ir descarregar o repositório

    def heuristica(self, p1, p2):
        # Manhattan distance
        return abs(p1.x - p2.x) + abs(p1.y - p2.y)

    def busca_a_estrela(self, _map, objetivo):
        queue = PriorityQueue()  # Fila de Prioridade
        queue.put(_map.inicio, 0)  # Adiciona o ponto de partida na fila
        custo = {_map.inicio: 0}  # Custo inicial do ponto de partida
        chegou_no_destino = False  # Variável de controle para identificar se o algoritmo chegou no destino
        caminho = {}  # Dicionário para armazenar o caminho percorrido
        while not queue.empty():  # Enquanto a fila não estiver vazia
            point = queue.get()  # Remove e pega o elemento da fila
            if point == objetivo:  # Se ponto for o destino, para a recursão
                chegou_no_destino = True  # E sinaliza a variável de controle
                break
            for proximo in _map.successors(point.x, point.y):  # Pega os pontos sucessores do point
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

    def solve(self, _map, objetivo):
        caminho, custo = self.busca_a_estrela(_map, objetivo)  # Executa o método de busca A*
        caminho_final = []  # Lista contendo o caminho
        node = objetivo  # O dicionário que é retornado começa do destino até a origem
        # (mas na pesquisa é feito da origem até o destino), então é armazenado o destino como ponto de partida
        if caminho is not None:  # Se o caminho for Nulo então não foi encontrado uma solução
            while node is not None and node in caminho:  # Enquanto o nó node não for nulo
                # (lembrando que vem de trás para frente) e o nó estiver no dicionário
                # (isso acontece no caso do ponto de partida já que ele não tem nó node a ele)
                atual = node  # Armazena o nó node
                node = caminho[node]  # armazena
                # caminho_final.insert(0, direction(node.x, node.y, atual.x, atual.y))  # Pega a direção de movimento
                caminho_final.insert(0, self.direction(node.x, node.y, atual.x, atual.y))  # Pega a direção de movimento
                # que o agente deve realizar através do método
                # auxiliar e armazena sempre no começo da lista
        return caminho_final if caminho is not None else None

    def direction(self, x1, y1, x2, y2):
        if x1 < x2:
            return MOVER_DIREITA
        elif x1 > x2:
            return MOVER_ESQUERDA
        elif y1 < y2:
            return MOVER_BAIXO
        elif y1 > y2:
            return MOVER_CIMA
        raise Exception("Unknown direction", x1, y1, x2, y2)
