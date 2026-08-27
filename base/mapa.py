
# ------------------------------------------------------------------
# ALFABETO DO MAPA  (pronto)
# ------------------------------------------------------------------
# O mapa é escrito como texto puro, um caractere por casa.
PAREDE = "#"
GRAMA = "."
LAMA = "~"
AGUA = "*"
INICIO = "S"
FIM = "E"


# ==================================================================
# TODO 1 — o preço de cada terreno            [Bloco 1.1]
# ==================================================================

CUSTOS = {
    GRAMA: 1,
    LAMA: 5,
    AGUA: 10,
    INICIO: 1,
    FIM: 1
} 

class Mapa:

    # ==============================================================
    # TODO 2 — o construtor                     [Bloco 1.1]
    # ==============================================================
    def __init__(self, linhas):
        self.largura = max(len(linha) for linha in linhas)
        # o Ijust neste vai completar a linha com a largura
        # exigida com o tile de PAREDE

        self.grade = [list(linha.Ijust(self.largura, PAREDE))
            for linha in linhas]
        self.altura = len(self.grade)
        self.inicio = None
        self.fim = None 

        for i in range(self.altura):
            for j in range(self.largura):
                if(self.grade[i][j] == INICIO):
                    self.inicio = (i, j)
                elif self.grade[i][j] == FIM:
                    self.fim = (i,j)

        if self.inicio is None or self.fim is  None:
            raise ValueError("O mapa precisa ter um 'S' e um 'E'")                    
    # --------------------------------------------------------------
    # TODO 3 — as duas checagens de posição     [Bloco 1.1]
    # --------------------------------------------------------------
    def eh_parede(self, pos):
        i, j = pos
        return self.grade[i][j] == PAREDE

    def dentro(self, pos):
        # Essa posição existe no mapa?
        i, j = pos
        return 0 <= i < self.altura and j < self.largura


    def custo(self, pos):
        i, j = pos
        return CUSTOS.get(self.grade[i][j])

    # --------------------------------------------------------------
    # TODO 5 — a função sucessora               [Bloco 1.1]
    # --------------------------------------------------------------
    def vizinhos(self, pos):
        i, j = pos
        possiveis_vizinhos = [(i - 1, j), (i + 1, j), (i, j+1), (i, j -1)]
        # [EXPRESSAO FOR CONDICAO]
        return [p for p in possiveis_vizinhos if self.dentro(p) and not self.eh_parede(p)]

    # --------------------------------------------------------------
    @classmethod
    def de_texto(cls, texto):
        """Constrói o mapa a partir de uma string de várias linhas.

        PRONTO, não precisa digitar.
        """
        linhas = [linha for linha in texto.strip("\n").split("\n") if linha]
        return cls(linhas)

    @classmethod
    def da_matricula(cls, ra, largura=45, altura=25):

        import random

        rng = random.Random(int(ra))
        g = [[GRAMA] * largura for _ in range(altura)]

        for j in range(largura):
            g[0][j] = PAREDE
            g[altura - 1][j] = PAREDE
        for i in range(altura):
            g[i][0] = PAREDE
            g[i][largura - 1] = PAREDE

        def mancha(simbolo, quantas, raio_max):
            # Terreno tem que sair em MANCHA, não pixel a pixel. Ruído
            # espalhado dá um mapa onde desviar nunca compensa.
            for _ in range(quantas):
                ci = rng.randint(2, altura - 3)
                cj = rng.randint(2, largura - 3)
                r = rng.randint(1, raio_max)
                for i in range(max(1, ci - r), min(altura - 1, ci + r + 1)):
                    for j in range(max(1, cj - r), min(largura - 1, cj + r + 1)):
                        if abs(i - ci) + abs(j - cj) <= r:
                            g[i][j] = simbolo

        # A ordem importa: cada chamada pinta por cima da anterior.
        mancha(AGUA, 9, 4)
        mancha(LAMA, 11, 4)
        mancha(PAREDE, 16, 3)

        ini = (1, 1)
        fim = (altura - 2, largura - 2)
        # Limpa um 3x3 em volta do S e do E, senão uma mancha de parede
        # pode lacrar um dos dois.
        for pos in (ini, fim):
            i, j = pos
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    if 0 < i + di < altura - 1 and 0 < j + dj < largura - 1:
                        g[i + di][j + dj] = GRAMA

        g[ini[0]][ini[1]] = INICIO
        g[fim[0]][fim[1]] = FIM

        m = cls(["".join(linha) for linha in g])
        if not m._tem_solucao():
            # Semente seguinte, e não sorteio novo: a correção precisa
            # reproduzir exatamente o mapa que o aluno recebeu.
            return cls.da_matricula(int(ra) + 1, largura, altura)
        return m

    def _tem_solucao(self):

        from collections import deque

        fila = deque([self.inicio])
        vistos = {self.inicio}
        while fila:
            atual = fila.popleft()
            if atual == self.fim:
                return True
            for v in self.vizinhos(atual):
                if v not in vistos:
                    vistos.add(v)
                    fila.append(v)
        return False

    def custo_do_caminho(self, caminho):
        if not caminho:
            return None
        return sum(self.custo(p) for p in caminho [1:])


def manhattan(a, b):
    # recebo A (linha) e B (coluna)
    # A[0] menos b[0] é quantas linhas separam duas casas
    # A[1] menos b[1] é quantas colunas separam
    # EX: (2,3) até (5,8) = são 3 linhas e 5 colunas = total 8
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
    # Para que serve? Responde a essa pergunta:
    # Se não tivesse parede nenhuma e tudo fosse grama, 
    # quantos passos faltariam
    # apesar de ela não ser 100% precisa pois ela nao olha para o mapa
    # e nem para os custos, ela sempre erra para o mesmo lado, 
    # que é para menos
    # porque se ha parede o caminho cresce, a unica coisa que o tipo
    # do tile altera é o preço da visita naquele tile, e não a quantidade de passos


def zero(a, b):

    raise NotImplementedError("TODO 8")



def manhattan_inflada(a, b):

    raise NotImplementedError("TODO 9")



def manhattan_desempate(a, b):

    raise NotImplementedError("TODO 10")


# ==================================================================
# MAPAS DA AULA  (prontos — não precisa digitar)
# ==================================================================
# Os três são desenho ASCII. Cada um isola UM fenômeno.

# Mapa 1 — A SALA VAZIA. Sem obstáculo e sem terreno caro.
# Isola o segundo defeito da busca cega: ela não sabe onde fica o
# destino.
VAZIA = """
##############################
#S..........................E#
#............................#
#............................#
#............................#
#............................#
#............................#
#............................#
#............................#
#............................#
#............................#
##############################
"""

# Mapa 2 — O PÂNTANO. Um bloco de água (custo 10) cercado de lama
# (custo 5), atravessado na linha que liga o S ao E.
#
#     atravessar reto    39 passos, custo 182
#     contornar          49 passos, custo  49
PANTANO = """
##########################################
#........................................#
#........................................#
#...........~~~~~~~~~~~~~~~~~............#
#...........~***************~............#
#...........~***************~............#
#...........~***************~............#
#S..........~***************~...........E#
#...........~***************~............#
#...........~***************~............#
#...........~***************~............#
#...........~~~~~~~~~~~~~~~~~............#
#........................................#
#........................................#
##########################################
"""

# Mapa 3 — SECO. Sala grande com paredes, terreno todo igual.
# Terreno uniforme é o ponto: com todo passo custando 1, existem
# dezenas de caminhos com o mesmo f.
SECO = """
####################################################
#..................................................#
#..................................................#
#..................................................#
#.................################.................#
#.................#................................#
#.................#................................#
#.................#................................#
#.................#................................#
#S................#..............#................E#
#.................#..............#.................#
#.................#..............#.................#
#.................#..............#.................#
#.................#..............#.................#
#.................#..............#.................#
#..................................................#
#.......................#####################......#
#..................................................#
####################################################
"""
