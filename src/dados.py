"""Leitura dos cartões e gerenciamento do recorde do jogo.

Este módulo cuida apenas de arquivos: não usa Pygame e não conhece as regras
do jogo (elas ficam em src/funcoes.py). Autoria original: Aiandra de Sousa
Silva. Reescrito na Entrega 3 para separar a validação em funções pequenas,
dar mensagens de erro mais claras e gravar o recorde com mais segurança. As
funções públicas continuam as mesmas: carregar_cartoes, carregar_recorde e
salvar_recorde.
"""

import json
from pathlib import Path


PASTA_PROJETO = Path(__file__).resolve().parent.parent
PASTA_DADOS = PASTA_PROJETO / "data"
ARQUIVO_CARTOES = PASTA_DADOS / "cartoes.json"
ARQUIVO_RECORDE = PASTA_DADOS / "recorde.txt"

# "utf-8-sig" também aceita arquivos salvos com BOM (comum em editores do Windows).
CODIFICACAO_LEITURA = "utf-8-sig"

# Conjunto de campos que todo cartão precisa ter.
CAMPOS_OBRIGATORIOS = {"texto", "confiavel", "pista"}


def _texto_valido(valor):
    """Indica se o valor é uma string com algo além de espaços."""
    return isinstance(valor, str) and bool(valor.strip())


def validar_cartao(cartao, numero):
    """Confere um cartão; levanta ValueError dizendo qual cartão e qual campo falhou.

    O número é a posição do cartão no arquivo, começando em 1.
    """
    if not isinstance(cartao, dict):
        raise ValueError(f"O cartão {numero} não é um dicionário.")

    faltando = sorted(CAMPOS_OBRIGATORIOS - cartao.keys())
    if faltando:
        raise ValueError(
            f"O cartão {numero} não possui todos os campos obrigatórios "
            f"(faltando: {', '.join(faltando)})."
        )

    if not _texto_valido(cartao["texto"]):
        raise ValueError(f"O texto do cartão {numero} está vazio ou inválido.")

    if not isinstance(cartao["confiavel"], bool):
        raise ValueError(f"O campo 'confiavel' do cartão {numero} deve ser booleano.")

    if not _texto_valido(cartao["pista"]):
        raise ValueError(f"A pista do cartão {numero} está vazia ou inválida.")


def carregar_cartoes():
    """Carrega e valida os cartões de data/cartoes.json.

    Retorna uma lista de dicionários com "texto", "confiavel" e "pista".
    Levanta FileNotFoundError se o arquivo não existir e ValueError se o
    JSON for inválido ou algum cartão estiver incorreto.
    """
    texto = ARQUIVO_CARTOES.read_text(encoding=CODIFICACAO_LEITURA)
    cartoes = json.loads(texto)

    if not isinstance(cartoes, list):
        raise ValueError("O arquivo cartoes.json deve conter uma lista.")

    for numero, cartao in enumerate(cartoes, start=1):
        validar_cartao(cartao, numero)

    return cartoes


def carregar_recorde():
    """Lê o recorde salvo.

    Retorna 0 se o arquivo não existir, estiver vazio ou tiver conteúdo que
    não seja um número inteiro; valores negativos também viram 0.
    """
    try:
        conteudo = ARQUIVO_RECORDE.read_text(encoding=CODIFICACAO_LEITURA).strip()
        return max(0, int(conteudo))
    except (FileNotFoundError, ValueError):
        return 0


def salvar_recorde(pontuacao):
    """Grava a pontuação como recorde apenas se ela superar o recorde atual.

    Retorna o maior valor que ficou registrado. A gravação é feita em um
    arquivo temporário que depois substitui o original, para que uma falha no
    meio não deixe o recorde corrompido.
    """
    if not isinstance(pontuacao, int) or isinstance(pontuacao, bool):
        raise TypeError("A pontuação deve ser um número inteiro.")

    if pontuacao < 0:
        raise ValueError("A pontuação não pode ser negativa.")

    recorde_atual = carregar_recorde()
    if pontuacao <= recorde_atual:
        return recorde_atual

    ARQUIVO_RECORDE.parent.mkdir(parents=True, exist_ok=True)
    temporario = ARQUIVO_RECORDE.with_name(ARQUIVO_RECORDE.name + ".tmp")
    temporario.write_text(f"{pontuacao}\n", encoding="utf-8")
    temporario.replace(ARQUIVO_RECORDE)
    return pontuacao
