import pygame


def mil(n):
    return f"{n:,}".replace(",", ".")


CELULA = 58
PAINEL = 74
COR_FUNDO = (16, 16, 22)
COR_GRADE = (60, 62, 78)
COR_GRADE_FORTE = (120, 124, 148)
COR_FIXO = (215, 218, 230)
COR_NOVO = (90, 220, 140)
COR_ATUAL = (250, 200, 80)
COR_APAGADO = (232, 78, 92)
COR_TEXTO = (215, 218, 230)
COR_FRACO = (130, 134, 155)


class Visual:
    def __init__(self, grade_inicial, titulo="Sudoku", passos_por_quadro=1):
        self.fixos = {
            (i, j) for i in range(9) for j in range(9)
            if grade_inicial[i][j] not in ".0"
        }
        self.titulo = titulo
        self.passos_por_quadro = passos_por_quadro

        pygame.init()
        lado = 9 * CELULA
        self.tela = pygame.display.set_mode((lado, lado + PAINEL))
        pygame.display.set_caption(titulo)
        self.relogio = pygame.time.Clock()
        self.fonte = pygame.font.SysFont("Consolas", 34, bold=True)
        self.fonte_p = pygame.font.SysFont("Consolas", 15)
        self.fonte_m = pygame.font.SysFont("Consolas", 19, bold=True)

        self.pausado = False
        self.fechado = False
        self.contador = 0
        self.ultimo = None
        self.ultimo_ok = True
        self.nos = 0
        self.retrocessos = 0
        self.mais_fundo = {}

    def ao_passo(self, atribuicao, var, valor, colocou):
        if self.fechado:
            return
        self.contador += 1
        self.ultimo = var
        self.ultimo_ok = colocou
        if colocou:
            self.nos += 1
            if len(atribuicao) > len(self.mais_fundo):
                self.mais_fundo = dict(atribuicao)
        else:
            self.retrocessos += 1

        if self.contador % self.passos_por_quadro:
            return

        self._eventos()
        while self.pausado and not self.fechado:
            self._eventos()
            self._desenhar(atribuicao)
            self.relogio.tick(30)
        self._desenhar(atribuicao)

    def segurar(self, atribuicao, rodape=""):
        self.rodape = rodape
        while not self.fechado:
            self._eventos()
            self._desenhar(atribuicao, rodape)
            self.relogio.tick(30)
        pygame.quit()

    def _eventos(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.fechado = True
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.fechado = True
                elif e.key == pygame.K_SPACE:
                    self.pausado = not self.pausado
                elif e.key == pygame.K_UP:
                    self.passos_por_quadro = min(500, self.passos_por_quadro * 2)
                elif e.key == pygame.K_DOWN:
                    self.passos_por_quadro = max(1, self.passos_por_quadro // 2)

    def _desenhar(self, atribuicao, rodape=""):
        self.tela.fill(COR_FUNDO)

        for i in range(9):
            for j in range(9):
                x, y = j * CELULA, PAINEL + i * CELULA
                valor = atribuicao.get((i, j))
                if valor is None:
                    continue
                if (i, j) in self.fixos:
                    cor = COR_FIXO
                elif (i, j) == self.ultimo:
                    cor = COR_ATUAL if self.ultimo_ok else COR_APAGADO
                else:
                    cor = COR_NOVO
                t = self.fonte.render(str(valor), True, cor)
                self.tela.blit(t, (x + CELULA // 2 - t.get_width() // 2,
                                   y + CELULA // 2 - t.get_height() // 2))

        for k in range(10):
            forte = k % 3 == 0
            cor = COR_GRADE_FORTE if forte else COR_GRADE
            largura = 3 if forte else 1
            pygame.draw.line(self.tela, cor, (k * CELULA, PAINEL),
                             (k * CELULA, PAINEL + 9 * CELULA), largura)
            pygame.draw.line(self.tela, cor, (0, PAINEL + k * CELULA),
                             (9 * CELULA, PAINEL + k * CELULA), largura)

        self.tela.blit(self.fonte_m.render(self.titulo, True, COR_TEXTO), (10, 8))
        info = f"escritos: {mil(self.nos)}    apagados: {mil(self.retrocessos)}"
        self.tela.blit(self.fonte_p.render(info, True, COR_TEXTO), (10, 34))
        if rodape:
            self.tela.blit(self.fonte_p.render(rodape, True, COR_NOVO), (10, 52))
        else:
            ajuda = (f"espaço=pausa  ↑↓=velocidade ({self.passos_por_quadro}x)"
                     "  ESC=fecha")
            self.tela.blit(self.fonte_p.render(ajuda, True, COR_FRACO), (10, 52))

        pygame.display.flip()
        self.relogio.tick(240)


def animar(grade_inicial, problema, titulo, usar_mrv=True, usar_fc=True,
           passos_por_quadro=1, limite_nos=None):
    vis = Visual(grade_inicial, titulo, passos_por_quadro)
    problema.ao_passo = vis.ao_passo
    resultado = problema.resolver(
        usar_mrv=usar_mrv, usar_fc=usar_fc, limite_nos=limite_nos
    )
    if problema.estourou:
        rodape = (f"NÃO TERMINOU — parei em {mil(problema.nos)} tentativas,"
                  f" com {len(vis.mais_fundo)} casas de 81")
    elif resultado:
        rodape = (f"resolvido em {mil(problema.nos)} tentativas · "
                  f"{mil(problema.retrocessos)} retrocessos")
    else:
        rodape = "SEM SOLUÇÃO"
    vis.segurar(resultado or vis.mais_fundo, rodape)
    return resultado
