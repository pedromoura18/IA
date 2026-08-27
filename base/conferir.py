"""
Confere o seu codigo contra os numeros da aula.

    python conferir.py

Rode quantas vezes quiser, a qualquer altura. Ele descobre sozinho ate
onde voce chegou: o que ainda esta como TODO aparece em amarelo, o que
ja funciona aparece em verde ou vermelho.
"""

import traceback

VERDE = "\033[92m"
VERMELHO = "\033[91m"
AMARELO = "\033[93m"
CINZA = "\033[90m"
FIM = "\033[0m"

_placar = {"ok": 0, "falhou": 0, "todo": 0}


def titulo(txt):
    print()
    print(f"  {txt}")
    print("  " + "-" * 64)


def _todo(rotulo, detalhe=""):
    extra = f"  {CINZA}{detalhe}{FIM}" if detalhe else ""
    print(f"  {AMARELO}TODO  {FIM} {rotulo}{extra}")
    _placar["todo"] += 1


def checar(rotulo, funcao, esperado):
    """`funcao` e uma lambda: o calculo so acontece aqui dentro."""
    try:
        obtido = funcao()
    except NotImplementedError:
        _todo(rotulo, "ainda nao implementado")
        return
    except Exception as e:  # noqa: BLE001
        print(f"  {VERMELHO}ERRO  {FIM} {rotulo:<42} {type(e).__name__}: {e}")
        _placar["falhou"] += 1
        return

    if obtido == esperado:
        print(f"  {VERDE}OK    {FIM} {rotulo:<42} {obtido}")
        _placar["ok"] += 1
    else:
        print(f"  {VERMELHO}FALHOU{FIM} {rotulo:<42} "
              f"saiu {obtido}, esperado {esperado}")
        _placar["falhou"] += 1


# ==================================================================
titulo("BLOCO 1 — mapa.py")

try:
    import mapa as mp
except ModuleNotFoundError:
    print(f"  {AMARELO}mapa.py nao esta nesta pasta.{FIM}")
    raise SystemExit
except Exception:
    print(f"  {VERMELHO}mapa.py nao carrega:{FIM}\n")
    traceback.print_exc()
    raise SystemExit

for nome in ("PAREDE", "GRAMA", "LAMA", "AGUA", "CUSTOS", "Mapa",
             "VAZIA", "PANTANO", "SECO"):
    if not hasattr(mp, nome):
        print(f"  {VERMELHO}FALHOU{FIM} falta {nome} em mapa.py")
        _placar["falhou"] += 1

if not getattr(mp, "CUSTOS", None):
    # Dicionario vazio: ainda e o esqueleto, nao um erro.
    _todo("CUSTOS · grama, lama e agua", "TODO 1 ainda em branco")
    _placar["todo"] += 2
else:
    checar("CUSTOS · grama", lambda: mp.CUSTOS.get(mp.GRAMA), 1)
    checar("CUSTOS · lama", lambda: mp.CUSTOS.get(mp.LAMA), 5)
    checar("CUSTOS · agua", lambda: mp.CUSTOS.get(mp.AGUA), 10)

_cache = {}


def mapa_de(nome):
    """Constroi o mapa uma vez so. Propaga NotImplementedError para o
    checar(), que sabe traduzir em TODO."""
    if nome not in _cache:
        _cache[nome] = mp.Mapa.de_texto(getattr(mp, nome))
    return _cache[nome]


checar("Mapa.inicio no pantano", lambda: mapa_de("PANTANO").inicio, (7, 1))
checar("Mapa.fim no pantano", lambda: mapa_de("PANTANO").fim, (7, 40))
checar("custo((7,20)) — agua", lambda: mapa_de("PANTANO").custo((7, 20)), 10)
checar("custo((3,12)) — lama", lambda: mapa_de("PANTANO").custo((3, 12)), 5)
checar("vizinhos(S) — 3, sem diagonal",
       lambda: mapa_de("PANTANO").vizinhos((7, 1)), [(6, 1), (7, 2), (8, 1)])
# O erro classico: somar o S. Este caminho tem 2 casas alem do S.
checar("custo_do_caminho NAO soma o S",
       lambda: mapa_de("PANTANO").custo_do_caminho([(7, 1), (7, 2), (7, 3)]), 2)
checar("manhattan(S, E) no pantano",
       lambda: mp.manhattan((7, 1), (7, 40)), 39)

# ==================================================================
titulo("BLOCO 2 — busca_informada.py")

try:
    from busca_informada import (a_estrela, bfs_que_voces_ja_conhecem,
                                 dijkstra, guloso)
except ModuleNotFoundError:
    print(f"  {AMARELO}busca_informada.py nao esta nesta pasta.{FIM}")
    raise SystemExit
except Exception:
    print(f"  {VERMELHO}busca_informada.py nao carrega:{FIM}\n")
    traceback.print_exc()
    raise SystemExit


def medir(fn, nome_mapa, campo, **kw):
    """campo: 'exp', 'passos' ou 'custo'."""
    caminho, visitados = fn(mapa_de(nome_mapa), **kw)
    if campo == "exp":
        return len(visitados)
    if caminho is None:
        return None
    if campo == "passos":
        return len(caminho) - 1
    return mapa_de(nome_mapa).custo_do_caminho(caminho)


checar("SALA VAZIA · Dijkstra · expansoes",
       lambda: medir(dijkstra, "VAZIA", "exp"), 226)
checar("SALA VAZIA · Dijkstra · passos",
       lambda: medir(dijkstra, "VAZIA", "passos"), 27)
checar("SALA VAZIA · A* · expansoes   <- o numero do quadro",
       lambda: medir(a_estrela, "VAZIA", "exp"), 28)
checar("SALA VAZIA · A* · passos",
       lambda: medir(a_estrela, "VAZIA", "passos"), 27)

checar("PANTANO · BFS · expansoes",
       lambda: medir(bfs_que_voces_ja_conhecem, "PANTANO", "exp"), 472)
checar("PANTANO · BFS · passos",
       lambda: medir(bfs_que_voces_ja_conhecem, "PANTANO", "passos"), 39)
checar("PANTANO · BFS · custo",
       lambda: medir(bfs_que_voces_ja_conhecem, "PANTANO", "custo"), 182)

checar("PANTANO · Dijkstra · expansoes",
       lambda: medir(dijkstra, "PANTANO", "exp"), 470)
checar("PANTANO · Dijkstra · custo",
       lambda: medir(dijkstra, "PANTANO", "custo"), 49)
checar("PANTANO · Guloso · expansoes",
       lambda: medir(guloso, "PANTANO", "exp"), 40)
checar("PANTANO · Guloso · custo (errado de proposito)",
       lambda: medir(guloso, "PANTANO", "custo"), 182)
checar("PANTANO · A* · expansoes",
       lambda: medir(a_estrela, "PANTANO", "exp"), 294)
checar("PANTANO · A* · custo",
       lambda: medir(a_estrela, "PANTANO", "custo"), 49)

# ==================================================================
titulo("BLOCO 3 — as heuristicas")

checar("zero() · A* com h=0 e Dijkstra",
       lambda: medir(a_estrela, "VAZIA", "exp", h=mp.zero), 226)
checar("inflada · expansoes (fica rapido)",
       lambda: medir(a_estrela, "PANTANO", "exp", h=mp.manhattan_inflada), 40)
checar("inflada · custo (e responde errado)",
       lambda: medir(a_estrela, "PANTANO", "custo", h=mp.manhattan_inflada), 182)
checar("SECO · A* sem desempate · expansoes",
       lambda: medir(a_estrela, "SECO", "exp"), 558)
checar("SECO · com desempate · expansoes",
       lambda: medir(a_estrela, "SECO", "exp", h=mp.manhattan_desempate), 227)
checar("SECO · com desempate · custo (continua otimo)",
       lambda: medir(a_estrela, "SECO", "custo", h=mp.manhattan_desempate), 61)

# ==================================================================
titulo("PLACAR")
print(f"  {VERDE}{_placar['ok']} OK{FIM}   "
      f"{VERMELHO}{_placar['falhou']} falhou{FIM}   "
      f"{AMARELO}{_placar['todo']} ainda TODO{FIM}")
if _placar["falhou"] == 0 and _placar["todo"] == 0:
    print(f"  {VERDE}Tudo pronto. Seu codigo bate com o quadro.{FIM}")
print()
