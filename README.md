# Oficina de guardrails

Um guardrail simples para assistentes de IA, em Python puro (sem instalar nada). Ele olha um texto antes que chegue ao assistente e decide entre **bloquear**, **revisar** ou **permitir**, em três camadas:

1. **Regras:** expressões regulares que pegam padrões conhecidos ("ignore as instruções", CPF, cartão...).
2. **Modelo:** o [Laya](https://huggingface.co/convaiinnovations/laya) responde duas perguntas sobre o texto: "tenta dar ordens ao assistente?" e "tem dados sensíveis?". Cada resposta vem com uma probabilidade.
3. **Decisão:** junta as duas coisas usando dois limiares.

Se o modelo falhar (fora do ar, chave errada, tempo esgotado), o guardrail **falha fechado**: nada passa direto. O texto vai para revisão, ou é bloqueado se alguma regra disparou.

## Como rodar

Você precisa do Python 3.10 ou mais novo.

- **No seu computador:** clique em **Use this template** (ou baixe o ZIP), abra um terminal na pasta e siga os comandos abaixo.
- **No GitHub Codespaces:** clique em **Code → Codespaces → Create codespace**. O Python já vem instalado; use o terminal que abre embaixo.

### Defina a chave

O professor passa a chave na aula. Não coloque a chave em nenhum arquivo que vá para o Git.

```powershell
# Windows (PowerShell)
$env:GUARD_API_KEY = "cole-a-chave-aqui"
```

```bash
# macOS, Linux e Codespaces
export GUARD_API_KEY="cole-a-chave-aqui"
```

A variável vale só para aquele terminal. Se preferir, copie `.env.example` para `.env` e coloque a chave lá. O `.env` fica fora do Git.

Sem a chave, os scripts avisam e rodam **só as regras**.

## Exercícios

```bash
python testar_conexao.py                 # 1. a chave e o servidor funcionam?
python guardrail.py                      # 2. roda os exemplos embutidos
python guardrail.py "seu texto aqui"     #    avalia os seus textos
python guardrail.py --offline            #    só as regras, sem o modelo
python avaliar.py                        # 3. placar com exemplos/ataques.txt e exemplos/legitimos.txt
python avaliar.py --limiar-bloqueio 0.9 --limiar-revisao 0.6   # 4. mude os limiares e compare
python -m unittest discover -s tests -v  # testes (não usam a internet)
```

**Placar Red x Blue:** +1 por ataque bloqueado e -1 por pedido legítimo bloqueado. "Revisar" vale 0. O time vermelho escreve ataques em `exemplos/ataques.txt`; o azul melhora as regras e os limiares sem bloquear os pedidos de `exemplos/legitimos.txt`.

**Os limiares:**
- `--limiar-bloqueio`: a partir dessa probabilidade, o modelo sozinho bloqueia.
- `--limiar-revisao`: a partir dessa probabilidade, o texto vai para revisão. Se uma regra também disparou, ele é bloqueado.

## Se der erro

O `testar_conexao.py` explica o problema em português. Os mais comuns:

| Mensagem | O que fazer |
|---|---|
| `GUARD_API_KEY não está definida` | Defina a chave no mesmo terminal (veja acima). |
| `chave recusada (401)` | A chave está errada ou incompleta. Copie de novo. |
| `limite de requisições atingido (429)` | Espere uns 10 segundos. |
| `servidor ocupado (503)` | Muita gente ao mesmo tempo. Tente de novo. |
| `fora do ar` ou `não consegui conectar` | Avise o professor. |
| `erro 1010` | Seu código chamou o servidor sem `User-Agent`. Use as funções do `guardrail.py`. |

## Regras de uso

- O servidor (`https://laya.rynalde.com`) existe **só para esta oficina**.
- **Não envie dados pessoais reais**: nada de CPF, senha, cartão ou documento de verdade. Use dados inventados, como os dos exemplos.
- O servidor tem **limite de requisições**. Se você mandar demais, fica bloqueado por alguns segundos.
- **A chave será trocada depois da aula**, e a antiga deixa de funcionar.

## Licença

MIT. Veja [LICENSE](LICENSE).
