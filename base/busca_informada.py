
# g(n) -> Quanto já custou para chegar em n (fato)
# h(n) -> Quanto se ESTIMA que ainda falta (chute)
# f(n) -> é a soma do custo g com a estimativa h

# Dijkstra ordena por g -> so olha o passado
# Dijsktra Tira da fronteira sempre a mais barata
# Greedy ordena por h -> só olha o futuro
# Greedy tira a que PARECE estar mais perto do fim
# A* ordena por g + h
# A* Tira a que promete o menor total

import heapq

# Acha um caminho do inicio ao fim do mapa,
# É uma função só que se torna os TRES ALGORITMOS DE BUSCA
# é quem esclhe qual é o par de pesos peso_g e peso_h que vem por 
# parametro.
# Tem que devolver duas coisas: O caminho e a lista de passos
# que ele olhou
def busca_por_prioridade(mapa, ao_passo=None, peso_g=1, peso_h=1, h=None):
    # Primeiro que preciso é: uma função que chute quanto falta daqui
    # até o final. 
    # Se o metodo que chamou, nao passou uma, assumo o manhattan
    if h is None:
        from mapa import manhattan
        h = manhattan

    
    inicio, fim = mapa.inicio, mapa.fim

    # Aqui iniciamos a construcao da fronteira. é a lista de casas
    # que eu ja descobri e ainda nao visitei/olhei. Cada casa entra
    # na fronteira como (prioridade, contador, casa). Porque no heapq 
    # vai olhar a prioridade primeiro, e se houver empate, ele usa
    # o contador pra ver quem chegou antes
    contador = 0

    fronteira = [(0, contador, inicio)]

    # Para cada casa, registro o menor custo que eu ja consegui para 
    # chegar nela. Porque pode ter um caminho mais barato para a 
    # mesma casa
    g = {inicio: 0}

    # Preciso anotar de onde eu vim para chegar em cada casa.
    # Para poder no final reconstruir o caminho.
    veio_de = {inicio: None}

    # As casas visitadas na ordem
    visitados = []

    ja_expandido = set()

    while fronteira:
        # De toda a lista, eu tiro a casa de MENOR prioridade.
        # Aqui só a casa interessa porque prioridade e contador
        # já ordenaram a lista
        _, _, atual = heapq.heappop(fronteira)

        # Se já processei esta casa antes, é apenas uma cópia
        # que devo ignorar e sigo para a proxima.
        if atual in ja_expandido:
            continue

        ja_expandido.add(atual)
        visitados.append(atual)

        # Se a janela de animacao estiver ativa e funcionando
        # entao eu desenho este passo na tela
        if ao_passo:
            ao_passo(visitados, [p for _,_,p in fronteira], atual)

        if atual == fim:
            return reconstruir(veio_de, fim), visitados

        # Não cheguei ao final, olho para onde?
        # Olho para os vizinhos 
        for viz in mapa.vizinhos(atual):
            # Para cada vizinho da casa atual eu calculo quanto
            # me custaria para chegar nela por aqui: que é o quanto
            # eu gastei para chegar ate 'atual', mais o custo do
            # chão da casa vizinha
            novo_g = g[atual] + mapa.custo(viz)

            # Só mexo no vizinho em dois casos:
            # - ou eu nunca tinha chegado nesta casa, 
            # - ou achei uma forma mais barata do que a que ja estava anotado
            if viz not in g or novo_g < g[viz]:
                g[viz] = novo_g
                veio_de[viz] = atual

                # Preciso dar uma nota de prioridade para este vizinho
                # Para isso somo duas coisas:
                # novo_g -> É o que eu JA gastei para chegar ate aqui
                # h(viz, fim) -> O chute de quanto ainda falta
                # Se zero o peso_h, sobra só o gasto que é Dijsktra.
                # Se zero o peso_g, sobra só o chute, que é greedy.
                prioridade = ((peso_g * novo_g) + (peso_h * h(viz, fim)))
                contador += 1

                # Jogando a vizinha na lista. Ele jja vai para o lugar certo
                # porque o heapq assim a coloca, pela ordem de prioridade que 
                # eu estou setando
                heapq.heappush(fronteira, (prioridade, contador, viz))

    return None, visitados



def dijkstra(mapa, ao_passo=None):
    return busca_por_prioridade(mapa, ao_passo,
                                peso_g=1, peso_h=0);


def guloso(mapa, ao_passo=None):
    return busca_por_prioridade(mapa, ao_passo,
                                peso_g=0, peso_h=1);


def a_estrela(mapa, ao_passo=None, h=None):
    return busca_por_prioridade(mapa, ao_passo,
                                peso_g=1, peso_h=1, h=h);


# Recebe o ponto de onde eu vim ate agora de cada casa, e o destino
# Devemos devolver a LISTA de casas do inicio ate o fim na ordem certa,
# Pinta na tela o trajeto final
# 
def reconstruir(veio_de, fim):
    caminho = []
    # Começando pelo fim
    atual = fim

    while atual is not None:
        caminho.append(atual)
        atual = veio_de[atual]
    
    caminho.reverse()
    return caminho



# ==================================================================
# Daqui para baixo já está pronto. Não precisa digitar.
# ==================================================================
def bfs_que_voces_ja_conhecem(mapa, ao_passo=None):
    """O BFS de referência, usado na abertura da aula."""
    from collections import deque

    inicio, fim = mapa.inicio, mapa.fim

    fronteira = deque([inicio])
    veio_de = {inicio: None}
    visitados = []

    while fronteira:
        atual = fronteira.popleft()
        visitados.append(atual)

        if ao_passo:
            ao_passo(visitados, list(fronteira), atual)

        if atual == fim:
            return reconstruir(veio_de, fim), visitados

        for viz in mapa.vizinhos(atual):
            if viz not in veio_de:
                veio_de[viz] = atual
                fronteira.append(viz)

    return None, visitados
