"""Verifica se o endpoint e a chave da oficina funcionam.

    python testar_conexao.py
"""
import sys
import time

import guardrail as g


def main():
    if not g.API_KEY:
        print("ERRO: a variável GUARD_API_KEY não está definida.\n"
              "Defina a chave que o professor passou (veja o README) e rode de novo.")
        return 1
    print(f"Testando {g.URL} ...")
    inicio = time.perf_counter()
    try:
        probs = g.chamar_modelo("Olá! Qual a capital da França?")
    except g.ErroModelo as e:
        print(f"ERRO: {e}")
        return 1
    ms = (time.perf_counter() - inicio) * 1000
    print(f"OK: o modelo respondeu em {ms:.0f} ms.")
    print("Probabilidade de 'sim' em cada pergunta: " + ", ".join(f"{q}={p:.2f}" for q, p in probs.items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
