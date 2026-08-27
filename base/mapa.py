

PAREDE = "#"
GRAMA = "."
LAMA = "~"
AGUA = "*"
INICIO = "S"
FIM = "E"


# ==================================================================
# TODO 1 — CUSTOS                                      [Bloco 1.1]
# ==================================================================
CUSTOS = {
    GRAMA: 1,
    LAMA: 5,
    AGUA: 10,
    INICIO: 1,
    FIM: 1
}


class Mapa:

    def __init__(self, linhas):
        self.largura = max(len(linha) for linha in linhas)
        # O ljust neste vai completar a linha com a largura
        # exigida com o tile da PAREDE
        self.grade = [list(linha.ljust(self.largura, PAREDE))
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
        
        if self.inicio is None or self.fim is None:
            raise ValueError("O mapa precisa ter um 'S' e um 'E'")

    def eh_parede(self, pos):
        i, j = pos
        return self.grade[i][j] == PAREDE

    def dentro(self, pos):
        # Essa posição existe no mapa?
        i, j = pos
        return 0 <= i < self.altura and 0 <= j < self.largura


    def custo(self, pos):
        i, j = pos
        return CUSTOS.get(self.grade[i][j], 1)


    def vizinhos(self, pos):
        i, j = pos
        possiveis_vizinhos = [(i - 1, j), (i + 1, j), (i, j+ 1), (i, j - 1)]
        # [EXPRESSAO FOR CONDICAO]
        return [p for p in possiveis_vizinhos if self.dentro(p) and not self.eh_parede(p)]


    def custo_do_caminho(self, caminho):
        if not caminho:
            return None
        return sum(self.custo(p) for p in caminho[1:])

    # --------------------------------------------------------------
    # Daqui para baixo já está pronto. Não precisa digitar.
    # --------------------------------------------------------------
    @classmethod
    def de_texto(cls, texto):
        linhas = [linha for linha in texto.strip("\n").split("\n") if linha]
        return cls(linhas)

    @classmethod
    def da_matricula(cls, ra, largura=45, altura=25):
        """Gera o mapa do Trabalho 01 a partir do RA."""
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
            for _ in range(quantas):
                ci = rng.randint(2, altura - 3)
                cj = rng.randint(2, largura - 3)
                r = rng.randint(1, raio_max)
                for i in range(max(1, ci - r), min(altura - 1, ci + r + 1)):
                    for j in range(max(1, cj - r), min(largura - 1, cj + r + 1)):
                        if abs(i - ci) + abs(j - cj) <= r:
                            g[i][j] = simbolo

        mancha(AGUA, 9, 4)
        mancha(LAMA, 11, 4)
        mancha(PAREDE, 16, 3)

        ini = (1, 1)
        fim = (altura - 2, largura - 2)
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


def manhattan(a, b):
    # recebo A (linha) e B (coluna)
    # A[0] menos B[0] é quantas linhas separam duas casas
    # A[1] menos B[1] é quantas colunas separam.
    # EX: (2,3) até (5,8) = São 3 linhas e 5 colunas = total 8
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
    # Para que serve? Responde a essa pergunta:
    # 'Se não tivesse parede nenhuma e tudo fosse grama, 
    # quantos passos faltariam
    # Apesar de ela não ser 100% precisa pois não olha para o mapa
    # nem para custos, ela sempre erra para o mesmo lado, que é pra menos
    # Porque se há parede o caminho cresce. A unica coisa que o tipo
    # do tile altera é o preço da visita naquele tile, e não a quantidade
    # de passos


# ------------------------------------------------------------------
# TODO 8 — zero                                        [Bloco 3.2]
# ------------------------------------------------------------------
def zero(a, b):
    raise NotImplementedError("TODO 8")


# ------------------------------------------------------------------
# TODO 9 — manhattan_inflada                           [Bloco 3.3]
# ------------------------------------------------------------------
def manhattan_inflada(a, b):
    raise NotImplementedError("TODO 9")


# ------------------------------------------------------------------
# TODO 10 — manhattan_desempate                        [Bloco 3.4]
# ------------------------------------------------------------------
def manhattan_desempate(a, b):
    raise NotImplementedError("TODO 10")


# ==================================================================
# OS MAPAS — já prontos
# ==================================================================

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
