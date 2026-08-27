"""Confere o seu codigo.     python conferir.py

O que e COBRADO: passos e custo. Sao iguais para todo mundo.
O que e so INFORMADO: quantas casas o algoritmo examinou. Esse
numero muda conforme a ordem em que voce escreveu os vizinhos,
entao ele nao conta como erro.
"""
import traceback

V, R, A, C, F = "\033[92m", "\033[91m", "\033[93m", "\033[90m", "\033[0m"
p = {"ok": 0, "falhou": 0, "todo": 0}


def checar(rotulo, fn, esperado):
    try:
        obtido = fn()
    except NotImplementedError:
        print(f"  {A}TODO  {F} {rotulo}")
        p["todo"] += 1
        return
    except Exception as e:
        print(f"  {R}ERRO  {F} {rotulo:<44} {type(e).__name__}: {e}")
        p["falhou"] += 1
        return
    if obtido == esperado:
        print(f"  {V}OK    {F} {rotulo:<44} {obtido}")
        p["ok"] += 1
    else:
        print(f"  {R}FALHOU{F} {rotulo:<44} saiu {obtido}, esperado {esperado}")
        p["falhou"] += 1


def info(rotulo, fn):
    try:
        print(f"  {C}. . . .  {rotulo:<42} {fn()}{F}")
    except NotImplementedError:
        pass
    except Exception:
        pass


def titulo(t):
    print()
    print(f"  {t}")
    print("  " + "-" * 62)


titulo("PARTE 1 — mapa.py")
try:
    import mapa as mp
except Exception:
    print(f"  {R}mapa.py nao carrega:{F}\n")
    traceback.print_exc()
    raise SystemExit

if not getattr(mp, "CUSTOS", None):
    print(f"  {A}TODO  {F} CUSTOS ainda vazio")
    p["todo"] += 3
else:
    checar("custo da grama", lambda: mp.CUSTOS.get(mp.GRAMA), 1)
    checar("custo da lama", lambda: mp.CUSTOS.get(mp.LAMA), 5)
    checar("custo da agua", lambda: mp.CUSTOS.get(mp.AGUA), 10)

_c = {}


def mapa_de(nome):
    if nome not in _c:
        _c[nome] = mp.Mapa.de_texto(getattr(mp, nome))
    return _c[nome]


checar("Mapa.inicio", lambda: mapa_de("PANTANO").inicio, (7, 1))
checar("Mapa.fim", lambda: mapa_de("PANTANO").fim, (7, 40))
checar("custo de uma casa de agua", lambda: mapa_de("PANTANO").custo((7, 20)), 10)
checar("custo de uma casa de lama", lambda: mapa_de("PANTANO").custo((3, 12)), 5)
checar("vizinhos do S (3, sem diagonal)",
       lambda: sorted(mapa_de("PANTANO").vizinhos((7, 1))),
       [(6, 1), (7, 2), (8, 1)])
checar("custo_do_caminho NAO soma o S",
       lambda: mapa_de("PANTANO").custo_do_caminho([(7, 1), (7, 2), (7, 3)]), 2)
checar("manhattan(S, E)", lambda: mp.manhattan((7, 1), (7, 40)), 39)

titulo("PARTE 2 — busca_informada.py")
try:
    from busca_informada import (a_estrela, bfs_que_voces_ja_conhecem,
                                 dijkstra, guloso)
except Exception:
    print(f"  {R}busca_informada.py nao carrega:{F}\n")
    traceback.print_exc()
    raise SystemExit


def passos(fn, nome):
    return len(fn(mapa_de(nome))[0]) - 1


def custo(fn, nome):
    return mapa_de(nome).custo_do_caminho(fn(mapa_de(nome))[0])


def exp(fn, nome):
    return len(fn(mapa_de(nome))[1])


checar("PANTANO · BFS · passos", lambda: passos(bfs_que_voces_ja_conhecem, "PANTANO"), 39)
checar("PANTANO · BFS · CUSTO (o errado)", lambda: custo(bfs_que_voces_ja_conhecem, "PANTANO"), 182)
checar("PANTANO · Dijkstra · passos", lambda: passos(dijkstra, "PANTANO"), 49)
checar("PANTANO · Dijkstra · CUSTO (o certo)", lambda: custo(dijkstra, "PANTANO"), 49)
checar("PANTANO · Guloso · passos", lambda: passos(guloso, "PANTANO"), 39)
checar("PANTANO · Guloso · CUSTO (o errado)", lambda: custo(guloso, "PANTANO"), 182)
checar("PANTANO · A* · passos", lambda: passos(a_estrela, "PANTANO"), 49)
checar("PANTANO · A* · CUSTO (o certo)", lambda: custo(a_estrela, "PANTANO"), 49)
checar("SALA VAZIA · Dijkstra · passos", lambda: passos(dijkstra, "VAZIA"), 27)
checar("SALA VAZIA · A* · passos", lambda: passos(a_estrela, "VAZIA"), 27)

titulo("QUANTAS CASAS CADA UM EXAMINOU  (nao e nota, e o assunto da aula)")
info("PANTANO · Dijkstra", lambda: exp(dijkstra, "PANTANO"))
info("PANTANO · Guloso", lambda: exp(guloso, "PANTANO"))
info("PANTANO · A*", lambda: exp(a_estrela, "PANTANO"))
info("SALA VAZIA · Dijkstra", lambda: exp(dijkstra, "VAZIA"))
info("SALA VAZIA · A*", lambda: exp(a_estrela, "VAZIA"))

titulo("PLACAR")
print(f"  {V}{p['ok']} OK{F}   {R}{p['falhou']} falhou{F}   {A}{p['todo']} ainda TODO{F}")
if p["falhou"] == 0 and p["todo"] == 0:
    print(f"  {V}Acabou. Os tres algoritmos funcionam.{F}")
print()
