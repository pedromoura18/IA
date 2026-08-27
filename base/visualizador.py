"""
Visualizador com TERRENO — pygame.

Aula 04 · Busca heurística · IA 6P

É o visualizador da Aula 04 com uma diferença: cada tipo de terreno
tem uma cor, e a cor fica mais escura quanto mais caro for andar ali.
Assim dá pra ver, no projetor, POR QUE o caminho desviou.

VOCÊ NÃO PRECISA ESCREVER ESTE ARQUIVO.

CONTROLES
    ESPAÇO  pausa / continua
    ↑ ↓     velocidade
    D       pula a animação
    ESC     fecha
"""

import pygame

import mapa as mp

COR_FUNDO = (16, 16, 22)
COR_TEXTO = (215, 218, 230)
COR_TEXTO_FRACO = (130, 134, 155)

# Terreno: quanto mais caro, mais escuro/azulado.
COR_TERRENO = {
    mp.PAREDE: (46, 48, 62),
    mp.GRAMA: (30, 42, 32),  # custo 1  — verde escuro
    mp.LAMA: (74, 58, 30),  # custo 5  — marrom
    mp.AGUA: (20, 40, 78),  # custo 10 — azul profundo
    mp.INICIO: (30, 42, 32),
    mp.FIM: (30, 42, 32),
}

COR_VISITADO = (52, 88, 130)
COR_FRONTEIRA = (240, 190, 70)
COR_ATUAL = (255, 255, 255)
COR_CAMINHO = (90, 220, 140)
COR_INICIO = (110, 200, 255)
COR_FIM = (250, 100, 120)


class Visualizador:
    def __init__(self, m, titulo="Busca", celula=20, fps=60):
        self.m = m
        self.celula = celula
        self.fps = fps
        self.titulo = titulo

        self.altura_painel = 78
        pygame.init()
        self.tela = pygame.display.set_mode(
            (m.largura * celula, m.altura * celula + self.altura_painel)
        )
        pygame.display.set_caption(titulo)
        self.relogio = pygame.time.Clock()
        self.fonte = pygame.font.SysFont("Consolas", 19, bold=True)
        self.fonte_peq = pygame.font.SysFont("Consolas", 13)

        self.pausado = False
        self.pular = False
        self.fechado = False

    # --------------------------------------------------------------
    def ao_passo(self, visitados, fronteira, atual):
        if self.fechado or self.pular:
            return
        self._eventos()
        while self.pausado and not self.fechado and not self.pular:
            self._eventos()
            self._desenhar(visitados, fronteira, atual, None, pausado=True)
            self.relogio.tick(30)
        self._desenhar(visitados, fronteira, atual, None)
        self.relogio.tick(self.fps)

    def mostrar_resultado(self, visitados, caminho, rodape=""):
        self.pular = False
        while not self.fechado:
            self._eventos()
            self._desenhar(visitados, [], None, caminho, rodape=rodape)
            self.relogio.tick(30)
        pygame.quit()

    # --------------------------------------------------------------
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
                    self.fps = min(600, self.fps + 30)
                elif e.key == pygame.K_DOWN:
                    self.fps = max(1, self.fps - 30)
                elif e.key == pygame.K_d:
                    self.pular = True
                    self.pausado = False

    def _rect(self, pos):
        i, j = pos
        return pygame.Rect(
            j * self.celula, i * self.celula + self.altura_painel,
            self.celula - 1, self.celula - 1,
        )

    def _desenhar(self, visitados, fronteira, atual, caminho, pausado=False, rodape=""):
        self.tela.fill(COR_FUNDO)

        # terreno
        for i in range(self.m.altura):
            for j in range(self.m.largura):
                simbolo = self.m.grade[i][j]
                cor = COR_TERRENO.get(simbolo, COR_TERRENO[mp.GRAMA])
                pygame.draw.rect(self.tela, cor, self._rect((i, j)))

        # visitados: mistura com o terreno para o custo continuar visível
        for pos in visitados:
            r = self._rect(pos)
            s = pygame.Surface((r.width, r.height))
            s.set_alpha(165)
            s.fill(COR_VISITADO)
            self.tela.blit(s, r.topleft)

        for pos in fronteira:
            pygame.draw.rect(self.tela, COR_FRONTEIRA, self._rect(pos))

        if caminho:
            for pos in caminho:
                pygame.draw.rect(self.tela, COR_CAMINHO, self._rect(pos))

        if atual is not None:
            pygame.draw.rect(self.tela, COR_ATUAL, self._rect(atual))

        pygame.draw.rect(self.tela, COR_INICIO, self._rect(self.m.inicio))
        pygame.draw.rect(self.tela, COR_FIM, self._rect(self.m.fim))

        self._painel(visitados, fronteira, caminho, pausado, rodape)
        pygame.display.flip()

    def _painel(self, visitados, fronteira, caminho, pausado, rodape):
        self.tela.blit(self.fonte.render(self.titulo, True, COR_TEXTO), (10, 6))

        linha = f"expandidos: {len(visitados):>5}   fronteira: {len(fronteira):>4}"
        if caminho:
            passos = len(caminho) - 1
            custo = self.m.custo_do_caminho(caminho)
            linha += f"   passos: {passos}   CUSTO: {custo}"
        self.tela.blit(self.fonte_peq.render(linha, True, COR_TEXTO), (10, 32))

        # legenda de terreno — o projetor come cor, então escreve
        legenda = "terreno:  grama=1   lama=5   água=10"
        self.tela.blit(self.fonte_peq.render(legenda, True, COR_TEXTO_FRACO), (10, 48))

        if rodape:
            self.tela.blit(self.fonte_peq.render(rodape, True, COR_CAMINHO), (10, 62))
        elif pausado:
            self.tela.blit(
                self.fonte_peq.render("PAUSADO — espaço continua", True, COR_FRONTEIRA),
                (10, 62),
            )
        else:
            self.tela.blit(
                self.fonte_peq.render(
                    "espaço=pausa  ↑↓=velocidade  D=pular  ESC=fecha",
                    True, COR_TEXTO_FRACO,
                ),
                (10, 62),
            )


def animar(m, algoritmo, titulo, fps=120, celula=20, **kwargs):
    vis = Visualizador(m, titulo=titulo, fps=fps, celula=celula)
    caminho, visitados = algoritmo(m, vis.ao_passo, **kwargs)
    if caminho:
        rodape = (
            f"{len(visitados)} expansões · {len(caminho) - 1} passos · "
            f"custo {m.custo_do_caminho(caminho)}"
        )
    else:
        rodape = "SEM CAMINHO"
    vis.mostrar_resultado(visitados, caminho, rodape)
    return caminho, visitados
