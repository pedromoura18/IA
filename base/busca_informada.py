"""
Aula 04 — busca informada: Dijkstra, Guloso e A*.
ESQUELETO. É aqui que fica o Bloco 2 da aula.

Já vem pronto:
    bfs_que_voces_ja_conhecem()  — o BFS de referência

------------------------------------------------------------------
AS TRÊS LETRAS
------------------------------------------------------------------
    g(n)  quanto JÁ CUSTOU para chegar em n        (fato medido)
    h(n)  quanto se ESTIMA que ainda falta de n    (palpite)
    f(n)  g + h, a estimativa do custo total

------------------------------------------------------------------
OS TRÊS ALGORITMOS SÃO UM SÓ
------------------------------------------------------------------
    Dijkstra  ordena por  g       -> só o passado
    Guloso    ordena por  h       -> só o futuro
    A*        ordena por  g + h   -> os dois

Os três saem de UMA função, com pesos diferentes.
"""

import heapq  # fila de prioridade da biblioteca padrão


# ==================================================================
# TODO 1 — o algoritmo (um só)                [Bloco 2.2]
# ==================================================================
def busca_por_prioridade(mapa, ao_passo=None, peso_g=1, peso_h=1, h=None):
    """Busca em grade com fila de prioridade.

        peso_g=1, peso_h=0  ->  Dijkstra
        peso_g=0, peso_h=1  ->  Guloso
        peso_g=1, peso_h=1  ->  A*

    Devolve (caminho, visitados):
        caminho    lista de posições de S até E, ou None
        visitados  posições NA ORDEM em que foram expandidas. O
                   tamanho desta lista é a medida de trabalho.

    ==================================================================
    ROTEIRO, linha a linha
    ==================================================================

    1)  contador = 0
        fronteira = [(0, contador, inicio)]

        A fronteira é uma LISTA COMUM, mas a gente só vai mexer nela
        pelo heapq. O heapq mantém a lista com a propriedade de heap:
        o menor elemento fica sempre no índice 0.

        Cada item é uma TUPLA DE TRÊS: (prioridade, contador, posição)

        POR QUE TUPLA: o heapq compara os itens entre si para saber
        quem é o menor, e comparação de tupla em Python é
        lexicográfica. Ele olha o primeiro elemento; só se empatar é
        que olha o segundo; só se empatar de novo é que olha o
        terceiro. Ou seja, ele ordena pela prioridade, que é o que a
        gente quer.

        POR QUE O CONTADOR NO MEIO: por causa do empate. Se dois nós
        tiverem a mesma prioridade, o Python passa a comparar o
        SEGUNDO elemento. Sem o contador ali, o segundo elemento
        seria a posição, e ele compararia tuplas de coordenadas: o
        desempate viraria "quem tem a linha menor", que não tem
        relação nenhuma com o problema, e a animação mudaria a cada
        execução. Com o contador, empate se resolve por ordem de
        chegada.

        O primeiro item entra com prioridade 0 porque chegar no
        início não custou nada.

    2)  g = {inicio: 0}

        Dicionário posição -> melhor custo conhecido até ela.

        ISTO SUBSTITUI O `visitados` DO BFS, e a troca é obrigatória.
        No BFS bastava um conjunto, porque a primeira vez que se
        alcança uma casa já é pelo melhor caminho. Com custo isso
        deixa de valer: dá para chegar numa casa por um caminho caro
        e, dez iterações depois, descobrir um caminho barato para a
        mesma casa. Para comparar os dois é preciso saber POR QUANTO
        se chegou, e conjunto não guarda valor, só guarda presença.

    3)  veio_de = {inicio: None}
        ja_expandido = set()
        visitados = []

        `veio_de` é a árvore de caminhos: para cada casa, de qual
        casa se chegou nela. O início aponta para None, que é a
        marca da raiz. É só com isso que dá para refazer o trajeto
        no fim.

    4)  while fronteira:
            _, _, atual = heapq.heappop(fronteira)

        `heappop` remove e devolve o item de MENOR prioridade, não o
        primeiro que entrou. É a única diferença estrutural em
        relação ao BFS.

        Os dois `_` descartam prioridade e contador. Eles serviram
        para ordenar; depois de sair, não interessam mais. `_` é
        nome de variável comum, é só a convenção de "não vou usar".

            if atual in ja_expandido:
                continue
            ja_expandido.add(atual)

        POR QUE ISSO EXISTE: um mesmo nó pode entrar no heap mais de
        uma vez, por caminhos diferentes, com prioridades diferentes.
        O heap não sabe remover um elemento do meio, então a entrada
        velha fica lá e é descartada quando sai. Quando o nó sai pela
        segunda vez, a primeira saída já era a melhor. O nome disso é
        lazy deletion.

            visitados.append(atual)

            if ao_passo:
                ao_passo(visitados,
                         [p for _, _, p in fronteira],
                         atual)

        `ao_passo` é a função de desenho do visualizador. Ela vem
        como None quando a gente só quer o número, e aí nada é
        desenhado. A lista de dentro extrai só as POSIÇÕES das
        tuplas da fronteira, porque o desenho não quer prioridade
        nem contador.

            if atual == fim:
                return reconstruir(veio_de, fim), visitados

        O TESTE DO OBJETIVO FICA NA SAÍDA DO HEAP, NÃO NA ENTRADA.
        Testar ao inserir devolveria o primeiro caminho que chega ao
        destino, e não o mais barato: no momento em que o E entra na
        fronteira, ainda pode existir na fila um caminho melhor até
        ele, ainda não explorado. No BFS os dois testes dão no mesmo,
        porque todo passo custa 1. Aqui não dão.

    5)      for viz in mapa.vizinhos(atual):
                novo_g = g[atual] + mapa.custo(viz)

        LEIA ESTA LINHA EM VOZ ALTA: o custo de chegar no vizinho
        POR ESTE caminho é o que já custou chegar em `atual`, mais o
        preço de entrar em `viz`. É a definição de g, escrita em
        código.

                if viz not in g or novo_g < g[viz]:

        Duas situações passam por aqui, e é uma condição só para as
        duas:
            viz not in g      casa nova, nunca alcançada
            novo_g < g[viz]   casa conhecida, mas por um caminho
                              pior do que este

        A segunda metade não existia no BFS. É ela que permite ao
        algoritmo substituir um caminho já registrado por um melhor.

                    g[viz] = novo_g
                    veio_de[viz] = atual

        As duas andam juntas: se o custo melhorou, a rota que leva
        até lá mudou também.

                    prioridade = (peso_g * novo_g
                                  + peso_h * h(viz, fim))

        ESTA É A ÚNICA LINHA QUE DIFERENCIA OS TRÊS ALGORITMOS:
            peso_g=1, peso_h=0  ->  prioridade = g        Dijkstra
            peso_g=0, peso_h=1  ->  prioridade = h        Guloso
            peso_g=1, peso_h=1  ->  prioridade = g + h    A*

        Repare que h(viz, fim) é AVALIADO mesmo quando peso_h vale
        zero. O Python calcula a chamada antes de multiplicar. Por
        isso a heurística precisa existir até para rodar o Dijkstra.

                    contador += 1
                    heapq.heappush(fronteira,
                                   (prioridade, contador, viz))

        `heappush` insere mantendo a propriedade de heap. Custa
        O(log n), contra O(n log n) de reordenar a lista inteira a
        cada inserção.

    6)  return None, visitados

        A fronteira esvaziou sem alcançar o destino: não existe
        caminho. `visitados` volta assim mesmo, porque registra o
        esforço gasto para concluir isso.
    """
    if h is None:
        # Import adiado, aqui dentro: se estivesse no topo do
        # arquivo, mapa.py e este arquivo importariam um ao outro.
        from mapa import manhattan

        h = manhattan

    inicio, fim = mapa.inicio, mapa.fim

    raise NotImplementedError("TODO 1 — implemente busca_por_prioridade")


# ==================================================================
# TODO 2 — os três algoritmos, UMA linha cada  [Bloco 2.3]
# ==================================================================
# Se ficou mais de uma linha, o TODO 1 não ficou certo.

def dijkstra(mapa, ao_passo=None):
    """Ordena só por g. Acha o mais barato examinando muito.

        return busca_por_prioridade(mapa, ao_passo,
                                    peso_g=1, peso_h=0)

    peso_h=0 apaga a heurística da conta. Sobra a prioridade sendo
    o custo acumulado, e o algoritmo passa a expandir sempre o nó
    mais barato de alcançar entre todos os conhecidos.

    Sem informação sobre a direção do destino, ele espalha em ondas
    de custo crescente, para todos os lados.

    Edsger W. Dijkstra, 1959, "A Note on Two Problems in Connexion
    with Graphs", Numerische Mathematik 1.
    """
    raise NotImplementedError("TODO 2")


def guloso(mapa, ao_passo=None):
    """Ordena só por h. Corre na direção do destino e ignora o custo.

        return busca_por_prioridade(mapa, ao_passo,
                                    peso_g=0, peso_h=1)

    peso_g=0 apaga o custo acumulado. O algoritmo passa a expandir
    sempre o nó que PARECE mais perto do objetivo, sem nenhuma
    memória do que já gastou.

    É por isso que ele atravessa a água: a água é cara, mas está na
    direção certa, e preço não entra na conta dele.

    Na literatura: greedy best-first search. Doran e Michie, 1966.
    """
    raise NotImplementedError("TODO 2")


def a_estrela(mapa, ao_passo=None, h=None):
    """Ordena por g + h. Ótimo com heurística admissível, e rápido.

        return busca_por_prioridade(mapa, ao_passo,
                                    peso_g=1, peso_h=1, h=h)

    Os dois pesos em 1: a prioridade vira a soma. O algoritmo
    expande sempre o nó que promete o menor custo TOTAL.

    Repare que este é o único dos três que repassa o `h` recebido.
    É o único em que trocar a heurística muda o comportamento, e é
    sobre isso que gira o bloco 3.

    Hart, Nilsson e Raphael, 1968, "A Formal Basis for the Heuristic
    Determination of Minimum Cost Paths", IEEE TSSC 4(2).
    """
    raise NotImplementedError("TODO 2")


# ==================================================================
# TODO 3 — reconstruir o caminho               [Bloco 2.2, item 4]
# ==================================================================
def reconstruir(veio_de, fim):
    """Refaz o caminho de S até E a partir do dicionário de origens.

        caminho = []
        atual = fim
        while atual is not None:
            caminho.append(atual)
            atual = veio_de[atual]
        caminho.reverse()
        return caminho

    ------------------------------------------------------------
    POR QUE ISSO É NECESSÁRIO
    ------------------------------------------------------------
    Durante a busca ninguém guarda o caminho inteiro. Guardar uma
    lista de posições para cada casa da fronteira custaria memória
    demais. O que se guarda é UMA SETA por casa: de onde eu vim.

        veio_de = {E: X, X: W, W: S, S: None}

    Isso é uma árvore com as setas invertidas, todas apontando para
    a raiz.

    ------------------------------------------------------------
    O QUE CADA LINHA FAZ
    ------------------------------------------------------------
        atual = fim              começa no FIM, não no início

        while atual is not None  anda de trás para frente seguindo
                                 as setas. Só o início tem origem
                                 None, então esta condição para
                                 exatamente lá.

        caminho.append(atual)    vai empilhando E, X, W, S

        caminho.reverse()        inverte no lugar, porque a lista
                                 saiu do fim para o começo e a
                                 gente quer do começo para o fim

    `reverse()` mexe na própria lista e devolve None. Não escreva
    `return caminho.reverse()`, porque isso devolve None. Inverta
    numa linha e retorne na outra.
    """
    raise NotImplementedError("TODO 3")


# ==================================================================
# PRONTO — o BFS de referência
# ==================================================================
def bfs_que_voces_ja_conhecem(mapa, ao_passo=None):
    """BFS clássico: fila, visitados, vizinhos.

    Nada aqui é novo, é o percurso em largura de Estrutura de Dados,
    com a árvore trocada por uma grade. Está neste arquivo por um
    motivo só: rodar no mapa PANTANO e mostrar o resultado.

    Ele encontra um caminho de 39 passos, que é de fato o mais curto
    que existe, atravessando a água de ponta a ponta. Custo 182.

    O algoritmo não está com defeito. Ele responde corretamente à
    pergunta que sabe responder: qual o caminho com menos passos. Só
    que essa passou a ser a pergunta errada.

    Repare no que ele NÃO tem: nenhuma menção a custo, e nenhum uso
    de mapa.custo(). Custo é uma noção que não existe no vocabulário
    dele.
    """
    from collections import deque

    inicio, fim = mapa.inicio, mapa.fim

    # deque em vez de list: popleft() numa lista é O(n), porque todos
    # os elementos deslocam uma posição. No deque é O(1).
    fronteira = deque([inicio])
    veio_de = {inicio: None}
    visitados = []

    while fronteira:
        # popleft = o mais ANTIGO. Esta palavra é a diferença entre
        # BFS e DFS: pop() faria sair o mais recente, a fila viraria
        # pilha, e o percurso viraria profundidade.
        atual = fronteira.popleft()
        visitados.append(atual)

        if ao_passo:
            ao_passo(visitados, list(fronteira), atual)

        if atual == fim:
            return reconstruir(veio_de, fim), visitados

        for viz in mapa.vizinhos(atual):
            # veio_de faz dois trabalhos: registra a rota e serve de
            # conjunto de visitados. Marcar ao ENFILEIRAR, e não ao
            # retirar, impede que a mesma casa entre na fila uma vez
            # por vizinho que a descobre.
            if viz not in veio_de:
                veio_de[viz] = atual
                fronteira.append(viz)

    return None, visitados
