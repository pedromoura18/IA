"""
Menu da aula: escolhe o mapa, escolhe o algoritmo, roda.

    python main.py

Aula 04 · Busca heurística · IA 6P

------------------------------------------------------------------
O PAPEL DESTE ARQUIVO
------------------------------------------------------------------
Nenhum algoritmo é implementado aqui. Este arquivo só amarra as três
peças que já existem:

    mapa.py              o problema
    busca_informada.py   os algoritmos
    visualizador.py      o desenho

Ele tem dois modos de saída. O modo com janela mostra a busca casa por
casa, e serve para entender o COMPORTAMENTO. O modo tabela roda todos os
algoritmos sem desenhar nada, e serve para comparar NÚMEROS. Os dois são
necessários: a animação mostra o formato da exploração, a tabela mostra
o preço dela.
"""

import mapa as mp
from busca_informada import a_estrela, bfs_que_voces_ja_conhecem, dijkstra, guloso
from visualizador import animar

# ------------------------------------------------------------------
# OS MENUS
# ------------------------------------------------------------------
# Dicionário de tecla -> (rótulo, dado). Guardar as opções em estrutura
# de dados, em vez de espalhar em ifs, permite montar o menu na tela
# percorrendo o próprio dicionário: acrescentar um mapa aqui já o faz
# aparecer na listagem, sem tocar em mais nada.
#
# A partir do Python 3.7 o dicionário preserva a ordem de inserção, então
# a ordem escrita aqui é a ordem exibida.
MAPAS = {
    "1": ("Sala vazia   (o BFS de vocês custa 226)", mp.VAZIA),
    "2": ("Pântano      (o caminho curto não é o barato)", mp.PANTANO),
    "3": ("Seco         (a lição do desempate)", mp.SECO),
}

# Aqui cada valor é (rótulo, função, argumentos extras).
#
# As três últimas linhas são o ponto do menu: chamam a MESMA a_estrela
# das anteriores, trocando apenas a heurística passada em `h`. Nenhuma
# linha do A* muda entre (d), (e), (f) e (g) — muda só a informação que
# ele recebe, e o comportamento muda junto.
#
# O dicionário `{}` vazio significa "sem argumento extra": a função é
# chamada com o padrão, que para a_estrela é h = manhattan.
ALGORITMOS = {
    "a": ("BFS (Estrut. de Dados)", bfs_que_voces_ja_conhecem, {}),
    "b": ("Dijkstra  (só g)", dijkstra, {}),
    "c": ("Guloso    (só h)", guloso, {}),
    "d": ("A*        (g + h)", a_estrela, {}),
    "e": ("A* com heurística INFLADA x10", a_estrela, {"h": mp.manhattan_inflada}),
    "f": ("A* com DESEMPATE", a_estrela, {"h": mp.manhattan_desempate}),
    "g": ("A* com h = 0  (vira Dijkstra)", a_estrela, {"h": mp.zero}),
}


def tabela(m):
    """Roda todos os algoritmos no mesmo mapa e imprime a comparação.

    Sem janela: aqui interessa o número, não o desenho. Rodar os sete sem
    desenhar leva alguns milissegundos.
    """
    print()
    # Os `:<32` e `:>9` alinham as colunas: `<` à esquerda, `>` à
    # direita, e o número é a largura reservada. Alinhar números à
    # direita é o que deixa as ordens de grandeza comparáveis de relance.
    print(f"  {'algoritmo':<32}{'expandiu':>9}{'passos':>8}{'custo':>8}")
    print("  " + "-" * 57)

    # Primeira passada: roda tudo e guarda. É preciso ter todos os
    # resultados antes de imprimir qualquer linha, porque a marcação de
    # "ótimo" depende de saber qual foi o menor custo — e isso só se sabe
    # no fim.
    resultados = []
    for _, (nome, funcao, kw) in ALGORITMOS.items():
        # `**kw` desempacota o dicionário em argumentos nomeados:
        # {"h": manhattan_inflada} vira h=manhattan_inflada. Com o
        # dicionário vazio, nada é acrescentado.
        caminho, visitados = funcao(m, **kw)
        if caminho is None:
            # Sem caminho ainda há trabalho medido: guarda as expansões e
            # marca passos e custo como ausentes.
            resultados.append((nome, len(visitados), None, None))
        else:
            resultados.append(
                # len(caminho) - 1: o caminho é uma lista de CASAS, e o
                # número de passos é o número de casas menos um. Mesma
                # razão do [1:] em custo_do_caminho.
                (nome, len(visitados), len(caminho) - 1, m.custo_do_caminho(caminho))
            )

    # Menor custo entre os que acharam caminho: a régua da coluna final.
    melhor_custo = min(c for _, _, _, c in resultados if c is not None)

    # Segunda passada: imprime, agora sabendo quem é o ótimo.
    for nome, exp, passos, custo in resultados:
        if custo is None:
            print(f"  {nome:<32}{exp:>9}{'—':>8}{'sem caminho':>8}")
            continue
        # A marca é o que responde à pergunta do fechamento da aula:
        # examinar menos não é automaticamente melhor.
        marca = "  <- ótimo" if custo == melhor_custo else f"  <- {custo - melhor_custo} a mais"
        print(f"  {nome:<32}{exp:>9}{passos:>8}{custo:>8}{marca}")
    print()


def main():
    print()
    print("=" * 62)
    print("AULA 04 — BUSCA HEURÍSTICA")
    print("=" * 62)

    # Monta o menu percorrendo o dicionário. O `_` descarta o texto do
    # mapa, que não interessa na listagem.
    for k, (nome, _) in MAPAS.items():
        print(f"  {k}) {nome}")

    # `.strip()` remove espaços acidentais; o `or "1"` cobre o enter
    # vazio, porque string vazia é falsa em Python.
    escolha = input("\nmapa (1/2/3, enter = 1): ").strip() or "1"
    # `.get(chave, padrão)` em vez de MAPAS[escolha]: digitar "9" cai no
    # mapa 1 em vez de derrubar o programa com KeyError na frente da sala.
    nome_mapa, texto = MAPAS.get(escolha, MAPAS["1"])
    m = mp.Mapa.de_texto(texto)

    print()
    for k, (nome, _, _) in ALGORITMOS.items():
        print(f"  {k}) {nome}")
    print("  t) só a TABELA comparativa (sem janela)")
    modo = input("\nalgoritmo (enter = d): ").strip() or "d"

    if modo == "t":
        tabela(m)
        return

    nome_alg, funcao, kw = ALGORITMOS.get(modo, ALGORITMOS["d"])
    # `animar` cria a janela, passa o próprio método de desenho como
    # `ao_passo` e devolve o mesmo par (caminho, visitados) que o
    # algoritmo devolveria sem janela.
    #
    # O split("(") corta o parêntese do rótulo do mapa, que é explicação
    # de menu e não caberia bem na barra de título.
    caminho, visitados = animar(
        m, funcao, f"{nome_alg}  ·  {nome_mapa.split('(')[0].strip()}", fps=120, **kw
    )

    # Repete os números no terminal. A janela fecha, o terminal fica —
    # e é dele que os números vão para o quadro.
    print()
    print(f"  expandiu : {len(visitados)}")
    if caminho:
        print(f"  passos   : {len(caminho) - 1}")
        print(f"  custo    : {m.custo_do_caminho(caminho)}")
    else:
        print("  SEM CAMINHO")
    print()


# Só executa main() quando o arquivo é rodado direto, não quando é
# importado por outro. É o que permite `from main import tabela` sem
# disparar o menu.
if __name__ == "__main__":
    main()
