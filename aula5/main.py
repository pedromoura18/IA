import time

import csp

TETO = 2_000_000

LARGURA = 64


def num(n):
    return f"{n:,}".replace(",", ".")


def seg(x, casas=2):
    return f"{x:.{casas}f}".replace(".", ",")


PECAS = [
    ("sudoku_csp", "a traducao do Sudoku para variaveis/dominios/vizinhas"),
    ("formatar_sudoku", "imprimir o tabuleiro no terminal"),
    ("CSP", "a classe que resolve"),
]


def exigir(*nomes):
    faltam = [n for n in nomes if not hasattr(csp, n)]
    if not faltam:
        return False
    print()
    print("  AINDA NAO DA PARA RODAR ESTA OPCAO.")
    print()
    print("  Falta escrever no csp.py:")
    for n in faltam:
        texto = dict(PECAS).get(n, "")
        print("     " + n + ("   (" + texto + ")" if texto else ""))
    print()
    return True


def situacao():
    faltam = [(n, d) for n, d in PECAS if not hasattr(csp, n)]
    if not faltam:
        return
    print()
    print("  O csp.py ainda esta incompleto. Falta:")
    for n, d in faltam:
        print("     {:<18} {}".format(n, d))
    print()
    print("  E isso que a gente vai escrever hoje.")


def narrar(titulo, linhas):
    print()
    print("  " + "=" * (LARGURA - 2))
    print(f"  {titulo}")
    print("  " + "=" * (LARGURA - 2))
    print()
    for l in linhas:
        print(f"  {l}" if l else "")
    print()


def enter(texto="  [enter para continuar]"):
    try:
        input(texto)
    except (EOFError, KeyboardInterrupt):
        print()


def o_problema():
    if exigir("sudoku_csp", "formatar_sudoku", "CSP"):
        return
    grade = csp.FACIL
    vazias = sum(l.count(".") for l in grade)

    print()
    print("  O TABULEIRO, como ele chega:")
    print()
    print(csp.formatar_sudoku({
        (i, j): int(grade[i][j])
        for i in range(9) for j in range(9) if grade[i][j] not in ".0"
    }))
    print()
    print(f"  {vazias} casas vazias, {81 - vazias} pistas.")
    print()
    enter()

    problema = csp.sudoku_csp(grade)
    t0 = time.time()
    resultado = problema.resolver(limite_nos=TETO)
    dt = time.time() - t0

    if resultado is None:
        print()
        print(f"  NAO TERMINOU: bateu no teto de {num(TETO)} tentativas.")
        print("  Faltam as duas trocas marcadas com >>> no csp.py.")
        print()
        return

    print()
    print("  RESOLVIDO:")
    print()
    print(csp.formatar_sudoku(resultado))
    print()
    print(f"  {problema.nos} tentativas · {problema.retrocessos} retrocessos"
          f" · {seg(dt, 3)}s")

    narrar("O QUE VOCÊ ACABOU DE VER", [
        f"Este tabuleiro tem {vazias} casas vazias. Cada casa é uma",
        "VARIÁVEL: alguma coisa que precisa ser decidida.",
        "",
        "Cada uma aceita um número de 1 a 9. Esse conjunto de valores",
        "possíveis é o DOMÍNIO dela.",
        "",
        "E existe uma regra só: casas da mesma linha, da mesma coluna",
        "ou do mesmo bloco 3x3 não podem repetir valor. Essa é a",
        "RESTRIÇÃO.",
        "",
        "Variáveis, domínios, restrições. Um problema descrito com",
        "essas três coisas chama-se CSP — satisfação de restrições.",
        "",
        "CSP não é um algoritmo. É um FORMATO de descrever problema.",
        "",
        f"Repare no resultado: {problema.nos} tentativas e"
        f" {problema.retrocessos} retrocessos.",
        "São exatamente as 81 casas do tabuleiro, uma atribuição para",
        "cada uma, e NENHUMA delas foi desfeita. O solver não errou",
        "uma única vez.",
        "",
        "Guarde esse zero. Daqui a pouco ele vai ficar impressionante.",
    ])


def o_burro():
    if exigir("sudoku_csp", "CSP"):
        return
    print()
    print("  Vai abrir uma janela. Ela PARA SOZINHA em uns 15 segundos,")
    print("  ao bater no teto, e escreve NÃO TERMINOU no rodapé.")
    print("  Depois feche no X ou no ESC.")
    print()
    print("  Se parecer travada, NÃO travou: ela está pensando. O")
    print("  ingênuo faz milhares de tentativas entre um quadro e outro.")
    print()
    enter()

    try:
        import visual
    except ImportError:
        print()
        print("  Falta o pygame:  py -m pip install pygame-ce")
        print()
        return
    problema = csp.sudoku_csp(csp.FACIL)
    visual.animar(csp.FACIL, problema, "Sudoku — backtracking ingênuo",
                  usar_mrv=False, usar_fc=False,
                  passos_por_quadro=4000, limite_nos=TETO)

    narrar("O QUE VOCÊ ACABOU DE VER", [
        "Ele atacou as casas na ordem em que elas vieram: primeira",
        "linha, da esquerda para a direita. Como um robô burro.",
        "",
        "Cada número que APARECEU foi escrito. Ele tentou bem mais:",
        "a maioria briga com uma vizinha e nem chega a aparecer.",
        "Cada número que SUMIU é um retrocesso: ele descobriu que",
        "aquele caminho não levava a lugar nenhum e teve que apagar.",
        "",
        f"Ele parou em {num(problema.nos)} tentativas porque eu botei um",
        "teto, senão a aula travava. Ele NÃO terminou.",
        "",
        "Agora a pergunta que interessa:",
        "",
        "   Quando VOCÊ resolve Sudoku no papel, você começa pela",
        "   primeira casa vazia, de cima para baixo?",
        "",
        "Não começa. Você começa pela casa que tem menos opção.",
        "Você já usa uma estratégia que este programa não usa.",
    ])


def a_tabela(grade=None, nome="FACIL"):
    if exigir("sudoku_csp", "CSP"):
        return
    grade = grade or csp.FACIL
    print()
    print(f"  SUDOKU {nome}  (teto de {num(TETO)} tentativas)")
    print()
    print(f"  {'estratégia':<14}{'tentativas':>13}{'retrocessos':>14}"
          f"{'tempo':>9}   resultado")
    print("  " + "-" * 62)

    medidos = {}
    for rotulo, mrv, fc in [
        ("ingênuo", False, False),
        ("+ MRV", True, False),
        ("+ MRV + FC", True, True),
    ]:
        problema = csp.sudoku_csp(grade)
        t0 = time.time()
        resultado = problema.resolver(usar_mrv=mrv, usar_fc=fc, limite_nos=TETO)
        dt = time.time() - t0
        if problema.estourou:
            estado = "NÃO TERMINOU"
        elif resultado:
            estado = "resolvido"
        else:
            estado = "sem solução"
        medidos[rotulo] = (problema.nos, problema.retrocessos)
        print(f"  {rotulo:<14}{num(problema.nos):>13}{num(problema.retrocessos):>14}"
              f"{seg(dt):>7}s   {estado}")

    fc_nos, fc_retro = medidos["+ MRV + FC"]
    mrv_nos, _ = medidos["+ MRV"]

    if fc_nos == mrv_nos:
        narrar("AS TRES LINHAS DERAM IGUAL", [
            "As linhas marcadas com >>> no csp.py ainda estao na",
            "versao simples, entao as tres medicoes rodaram o MESMO",
            "algoritmo — e as tres bateram no teto.",
            "",
            "É o esperado neste ponto da aula. Faça as duas trocas e",
            "rode a opção 3 de novo.",
        ])
        return

    narrar("O QUE ESSA TABELA DIZ", [
        "Leia de baixo para cima.",
        "",
        f"ÚLTIMA LINHA: {fc_nos} tentativas e {fc_retro} retrocessos.",
        "Oitenta e uma atribuições, todas certas, direto. Uma para",
        "cada casa do tabuleiro. Ele não errou nenhuma vez.",
        "",
        f"LINHA DO MEIO: {num(mrv_nos)} tentativas. Já é enorme perto de"
        f" {fc_nos},",
        "e mesmo assim é cinquenta vezes menos que a linha de cima —",
        "que nem terminou. Contra o número real do ingênuo, os",
        "65.946.271, são mil e setecentas vezes menos.",
        "",
        "PRIMEIRA LINHA: ele nem terminou. Bateu no teto de 2 milhões",
        "que eu botei para a aula não travar. Sem o teto ele termina —",
        "em 65.946.271 tentativas e mais de cinco minutos. Eu medi.",
        "",
        "E agora a pergunta que fecha:",
        "",
        "   Eu troquei de algoritmo entre a primeira linha e a última?",
        "",
        "NÃO. É o mesmo backtracking, o mesmo arquivo, a mesma função",
        "recursiva. Eu mudei DUAS COISAS:",
        "",
        "   1. por onde começar      -> escolher a casa com menos",
        "                               opções restantes  (MRV)",
        "   2. o que checar antes    -> se alguma vizinha ficou sem",
        "      de descer                nenhuma opção  (forward checking)",
        "",
        "Duas heurísticas. Sessenta e cinco milhões viraram oitenta e um.",
        "",
        "Dar INFORMAÇÃO ao algoritmo sobre o problema rendeu mais do",
        "que qualquer troca de algoritmo renderia.",
    ])


def o_esperto():
    if exigir("sudoku_csp", "CSP"):
        return
    print()
    print("  Vai abrir a mesma janela, no mesmo tabuleiro — agora com")
    print("  MRV e forward checking ligados. Compare com a opção 2.")
    print()
    enter()

    try:
        import visual
    except ImportError:
        print()
        print("  Falta o pygame:  py -m pip install pygame-ce")
        print()
        return
    problema = csp.sudoku_csp(csp.FACIL)
    visual.animar(csp.FACIL, problema, "Sudoku — MRV + forward checking",
                  usar_mrv=True, usar_fc=True,
                  passos_por_quadro=1, limite_nos=TETO)

    narrar("O QUE VOCÊ ACABOU DE VER", [
        "Os números quase só APARECERAM. Quase nada sumiu.",
        "A tela ficou calma, e acabou em menos de um segundo.",
        "",
        "Na opção 2 a tela era uma cascata de números piscando. Aqui",
        "não. É o mesmo tabuleiro e o mesmo algoritmo — mudou só a",
        "ordem em que ele escolhe as casas, e o que ele confere antes",
        "de descer.",
        "",
        "O contraste entre as duas janelas é a aula inteira, sem",
        "nenhum número.",
    ])


def o_dificil():
    if exigir("sudoku_csp", "formatar_sudoku", "CSP"):
        return
    grade = csp.DIFICIL
    pistas = 81 - sum(l.count(".") for l in grade)
    problema = csp.sudoku_csp(grade)

    print()
    print("  ANTES:")
    print(csp.formatar_sudoku({
        (i, j): int(grade[i][j])
        for i in range(9) for j in range(9) if grade[i][j] not in ".0"
    }))

    t0 = time.time()
    resultado = problema.resolver(limite_nos=TETO)
    dt = time.time() - t0

    print()
    print("  DEPOIS:")
    print(csp.formatar_sudoku(resultado))
    print()
    print(f"  {num(problema.nos)} tentativas · {num(problema.retrocessos)}"
          f" retrocessos · {seg(dt)}s")

    narrar("O QUE VOCÊ ACABOU DE VER", [
        f"Este tabuleiro tem só {pistas} pistas e é um dos Sudokus mais",
        "difíceis que se conhece.",
        "",
        f"O fácil custou 81 tentativas e ZERO retrocessos.",
        f"Este custou {num(problema.nos)} tentativas e"
        f" {num(problema.retrocessos)} retrocessos.",
        "",
        "Ou seja: aqui ele erra o tempo todo. Chuta, desce, descobre",
        "que não dá, e volta. Mais de dez mil vezes.",
        "",
        "É a resposta para quem disse, lá no começo da aula, que",
        "'não chuta' ao resolver Sudoku. Em tabuleiro fácil dá para",
        "deduzir tudo. Aqui não dá — em algum momento é preciso",
        "arriscar e estar pronto para voltar atrás.",
        "",
        f"E mesmo assim ele resolveu em {seg(dt, 1)} segundo.",
    ])


def outros_problemas():
    if not hasattr(csp, "n_rainhas_csp"):
        print()
        print("  Esta opcao e da proxima aula.")
        print("  Ela usa o n_rainhas_csp() e o horarios_csp(), que ainda")
        print("  nao foram escritos no csp.py.")
        print()
        return
    print()
    print("  Duas coisas que não têm nada a ver com Sudoku, resolvidas")
    print("  pelo MESMO csp.py, sem trocar uma linha do solver.")
    print()
    enter()

    print()
    print("  PARTE A — N RAINHAS")
    print()
    print(f"  {'n':>4}{'tentativas':>13}{'retrocessos':>14}{'tempo':>9}")
    print("  " + "-" * 40)
    for n in (8, 12, 20, 30):
        problema = csp.n_rainhas_csp(n)
        t0 = time.time()
        problema.resolver()
        dt = time.time() - t0
        print(f"  {n:>4}{num(problema.nos):>13}{num(problema.retrocessos):>14}"
              f"{seg(dt):>7}s")
    print()
    print("  Tabuleiro 8x8 (o do xadrez):")
    problema = csp.n_rainhas_csp(8)
    print()
    print(csp.formatar_rainhas(problema.resolver(), 8))

    narrar("O QUE A TABELA DAS RAINHAS DIZ", [
        "O problema: pôr N rainhas num tabuleiro N por N sem que",
        "nenhuma ataque outra. A rainha ataca na horizontal, na",
        "vertical e nas duas diagonais.",
        "",
        "A modelagem é o que importa aqui: UMA VARIÁVEL POR COLUNA,",
        "e o valor dela é a linha onde aquela rainha fica.",
        "",
        "Repare no que isso faz: duas rainhas na mesma coluna não são",
        "só proibidas — elas são IMPOSSÍVEIS DE REPRESENTAR. Cada",
        "coluna só tem uma variável. Uma restrição inteira sumiu de",
        "graça, sem nenhuma linha de código.",
        "",
        "Agora olhe os números: 8 rainhas custou 75 tentativas e 30",
        "rainhas custou 147. O espaço de busca saltou de",
        "8^8 (17 milhões) para 30^30 (mais de 10^44) — trinta e sete",
        "ordens de grandeza — e o trabalho nem chegou a dobrar.",
        "",
        "Por quê? Porque N-rainhas tem MUITAS soluções espalhadas.",
        "É fácil cair em uma delas. Um Sudoku bem formulado tem UMA",
        "solução só — achar a única agulha é outro problema.",
        "",
        "O tamanho do espaço importa menos do que a densidade de",
        "respostas certas dentro dele.",
    ])
    enter()

    print()
    print("  PARTE B — A GRADE DE HORÁRIO DESTE CURSO")
    print()
    problema, info = csp.horarios_csp()
    t0 = time.time()
    resultado = problema.resolver()
    dt = time.time() - t0

    print(f"  {len(csp.DISCIPLINAS)} disciplinas · {len(csp.DIAS)} dias · "
          f"{len(csp.SALAS)} salas")
    print()
    if not resultado:
        print("  SEM SOLUÇÃO — as restrições são impossíveis de satisfazer.")
        print(f"  ({num(problema.nos)} tentativas até provar isso)")
        return

    for dia in csp.DIAS:
        do_dia = sorted(
            (nome, v[1]) for nome, v in resultado.items() if v[0] == dia
        )
        print(f"  {dia.upper()}")
        if not do_dia:
            print("     —")
        for nome, sala in do_dia:
            prof, per = info[nome]
            print(f"     {sala:<8} {nome:<26} {prof:<7} {per}º período")
        print()
    print(f"  resolvido em {problema.nos} tentativas ({seg(dt, 3)}s)")

    narrar("O QUE A GRADE DIZ", [
        "As restrições são três, e são as de qualquer instituição:",
        "",
        "   1. um professor não se divide em dois lugares no mesmo dia",
        "   2. uma sala não recebe duas turmas no mesmo dia",
        "   3. duas disciplinas do MESMO período não caem no mesmo dia",
        "      (o aluno também não se divide)",
        "",
        f"O solver resolveu em {problema.nos} tentativas.",
        "",
        "Este é o problema que o coordenador deste curso resolve todo",
        "semestre. Na mão. Levando dias, com planilha e telefonema.",
        "",
        "E não é brincadeira de sala: montar grade de horário é um CSP",
        "clássico, existe software comercial caro que faz isso, e o",
        "miolo é o que está no csp.py que vocês escreveram.",
        "",
        "Se você apertar as vagas — 4 dias e 2 salas, ou seja 8 vagas",
        "para 10 disciplinas — ele responde SEM SOLUÇÃO depois de",
        "38.840 tentativas. Repare: ele não travou nem chutou. Ele",
        "PROVOU que não existe resposta. Isso também é resultado útil:",
        "é o que o coordenador precisa para pedir mais uma sala.",
    ])


def main():
    print()
    print("=" * LARGURA)
    print("AULA 05 — SATISFAÇÃO DE RESTRIÇÕES")
    print("=" * LARGURA)
    print()
    print("  Rode 1, 2, 3, 4 nesta ordem. É a aula inteira.")
    print()
    print("   1) O PROBLEMA        o Sudoku e as três partes de um CSP")
    print("   2) O BURRO           backtracking ingênuo ao vivo  (janela)")
    print("   3) A TABELA          65 milhões contra 81   <- o número")
    print("   4) O ESPERTO         o mesmo, com heurísticas      (janela)")
    print()
    print("  Depois, se der tempo:")
    print()
    print("   5) O SUDOKU MAIS DIFÍCIL DO MUNDO")
    print("   6) O MESMO SOLVER, OUTROS DOIS PROBLEMAS")
    print("      rainhas e a grade de horário do curso")
    print()
    print("  Cada opção termina explicando o próprio resultado.")

    situacao()

    escolha = input("\nopção (enter = 1): ").strip() or "1"

    acoes = {
        "1": o_problema,
        "2": o_burro,
        "3": a_tabela,
        "4": o_esperto,
        "5": o_dificil,
        "6": outros_problemas,
    }
    acoes.get(escolha, o_problema)()


if __name__ == "__main__":
    main()
