"""Carregamento dos cartões e gerenciamento do recorde do jogo."""

import json
from pathlib import Path


PASTA_PROJETO = Path(__file__).resolve().parent.parent
PASTA_DADOS = PASTA_PROJETO / "data"
ARQUIVO_CARTOES = PASTA_DADOS / "cartoes.json"
ARQUIVO_RECORDE = PASTA_DADOS / "recorde.txt"


def carregar_cartoes():
    """Carrega e valida os cartões armazenados em data/cartoes.json.

    Retorna uma lista de dicionários com texto, confiavel e pista.
    """
    # "utf-8-sig" também aceita arquivos salvos com BOM (comum em editores do Windows).
    with ARQUIVO_CARTOES.open("r", encoding="utf-8-sig") as arquivo:
        cartoes = json.load(arquivo)

    if not isinstance(cartoes, list):
        raise ValueError("O arquivo cartoes.json deve conter uma lista.")

    campos_obrigatorios = {"texto", "confiavel", "pista"}

    for numero, cartao in enumerate(cartoes, start=1):
        if not isinstance(cartao, dict):
            raise ValueError(f"O cartão {numero} não é um dicionário.")

        if not campos_obrigatorios.issubset(cartao):
            raise ValueError(f"O cartão {numero} não possui todos os campos obrigatórios.")

        if not isinstance(cartao["texto"], str) or not cartao["texto"].strip():
            raise ValueError(f"O texto do cartão {numero} está vazio ou inválido.")

        if not isinstance(cartao["confiavel"], bool):
            raise ValueError(f"O campo 'confiavel' do cartão {numero} deve ser booleano.")

        if not isinstance(cartao["pista"], str) or not cartao["pista"].strip():
            raise ValueError(f"A pista do cartão {numero} está vazia ou inválida.")

    return cartoes


def carregar_recorde():
    """Lê o recorde salvo; retorna zero se o arquivo não existir ou estiver vazio."""
    try:
        conteudo = ARQUIVO_RECORDE.read_text(encoding="utf-8-sig").strip()

        if not conteudo:
            return 0

        recorde = int(conteudo)
        return max(0, recorde)

    except FileNotFoundError:
        return 0
    except ValueError:
        return 0


def salvar_recorde(pontuacao):
    """Atualiza o arquivo apenas se a pontuação superar o recorde atual.

    Retorna o maior valor que ficou registrado.
    """
    if not isinstance(pontuacao, int) or isinstance(pontuacao, bool):
        raise TypeError("A pontuação deve ser um número inteiro.")

    if pontuacao < 0:
        raise ValueError("A pontuação não pode ser negativa.")

    recorde_atual = carregar_recorde()

    if pontuacao > recorde_atual:
        PASTA_DADOS.mkdir(parents=True, exist_ok=True)
        ARQUIVO_RECORDE.write_text(str(pontuacao) + "\n", encoding="utf-8")
        return pontuacao

    return recorde_atual
