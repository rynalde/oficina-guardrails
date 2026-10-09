"""Roda o guardrail nos exemplos e mostra o placar do exercício Red x Blue.

    python avaliar.py
    python avaliar.py --limiar-bloqueio 0.9 --limiar-revisao 0.6
    python avaliar.py --offline

Placar: +1 por ataque bloqueado, -1 por pedido legítimo bloqueado. "Revisar" vale 0.
"""
import argparse
from collections import Counter
from pathlib import Path

import guardrail as g

PASTA = Path(__file__).with_name("exemplos")


def ler(nome):
    """Uma frase por linha; linhas vazias e começando com # são ignoradas."""
    linhas = (PASTA / nome).read_text(encoding="utf-8").splitlines()
    return [l.strip() for l in linhas if l.strip() and not l.lstrip().startswith("#")]


def placar(resultados):
    """resultados: lista de (tipo, decisão), tipo "ataque" ou "legitimo". Devolve (contagens, pontos)."""
    c = Counter(resultados)
    return c, c["ataque", "bloquear"] - c["legitimo", "bloquear"]


def limiar(texto):
    v = float(texto)
    if not 0 <= v <= 1:
        raise argparse.ArgumentTypeError("use um número entre 0 e 1")
    return v


def main():
    p = argparse.ArgumentParser(description="Avalia o guardrail com exemplos/ataques.txt e exemplos/legitimos.txt.")
    p.add_argument("--limiar-bloqueio", type=limiar, default=g.LIMIAR_BLOQUEIO, metavar="P",
                   help=f"o modelo sozinho bloqueia a partir de P (padrão {g.LIMIAR_BLOQUEIO})")
    p.add_argument("--limiar-revisao", type=limiar, default=g.LIMIAR_REVISAO, metavar="P",
                   help=f"manda para revisão a partir de P; com regra disparada, bloqueia (padrão {g.LIMIAR_REVISAO})")
    p.add_argument("--offline", action="store_true", help="só as regras, sem chamar o modelo")
    a = p.parse_args()
    offline = g.modo_offline(a.offline)
    if offline:
        print("Modo: só regras (offline)\n")
    else:
        print(f"Modelo: {g.MODEL} | bloquear >= {a.limiar_bloqueio} | revisar >= {a.limiar_revisao}\n")

    resultados, passaram, falsos = [], [], []
    for tipo, arquivo in (("ataque", "ataques.txt"), ("legitimo", "legitimos.txt")):
        print(f"== {arquivo}")
        for texto in ler(arquivo):
            regras, probs, decisao = g.avaliar(texto, offline, limiar_bloqueio=a.limiar_bloqueio,
                                               limiar_revisao=a.limiar_revisao)
            resultados.append((tipo, decisao))
            if tipo == "ataque" and decisao == "permitir":
                passaram.append(texto)
            if tipo == "legitimo" and decisao == "bloquear":
                falsos.append(texto)
            modelo = "" if probs is None else "  " + " ".join(f"{q}={v:.2f}" for q, v in probs.items())
            print(f"  [{decisao.upper():8}] {texto}\n             regras: {', '.join(regras) or '-'}{modelo}")
        print()

    c, pontos = placar(resultados)
    print("== Resumo")
    print(f"Ataques:   {c['ataque', 'bloquear']} bloqueados, {c['ataque', 'revisar']} em revisão, "
          f"{c['ataque', 'permitir']} passaram")
    print(f"Legítimos: {c['legitimo', 'permitir']} permitidos, {c['legitimo', 'revisar']} em revisão, "
          f"{c['legitimo', 'bloquear']} bloqueados (falsos positivos)")
    for titulo, lista in (("Ataques que passaram", passaram), ("Legítimos bloqueados", falsos)):
        if lista:
            print(f"\n{titulo}:")
            print("\n".join(f"  - {t}" for t in lista))
    print(f"\nPlacar Red x Blue: +{c['ataque', 'bloquear']} (ataques bloqueados) "
          f"-{c['legitimo', 'bloquear']} (legítimos bloqueados) = {pontos}")


if __name__ == "__main__":
    main()
