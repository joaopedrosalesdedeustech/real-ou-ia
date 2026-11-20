"""Funções de regra e lógica do jogo "Real ou IA?".

Nada neste módulo depende do Pygame, então tudo aqui pode ser testado
sem abrir a janela do jogo.
"""
import unicodedata

from src.config import (
    COMANDOS_VALIDOS,
    ROTULOS,
    VIDAS_INICIAIS,
    PONTOS_ACERTO,
    CUSTO_VERIFICACAO,
)


# ---------------------------------------------------------------------------
# Funções básicas (vindas do template)
# ---------------------------------------------------------------------------

def calcular_pontos(pontos_atual, pontos_ganhos):
    """Soma os pontos ganhos à pontuação atual (use valor negativo para descontar)."""
    return pontos_atual + pontos_ganhos


def tomar_dano(vida_atual, dano):
    """Reduz a vida atual com base no dano recebido."""
    return vida_atual - dano


def jogador_perdeu(vidas):
    """Indica se o jogador ficou sem vidas."""
    return vidas <= 0


def limitar_valor(valor, minimo, maximo):
    """Mantém um valor dentro do intervalo [minimo, maximo]."""
    if valor < minimo:
        return minimo
    if valor > maximo:
        return maximo
    return valor


def verificar_colisao(retangulo_1, retangulo_2):
    """Verifica sobreposição entre dois retângulos do Pygame."""
    return retangulo_1.colliderect(retangulo_2)


# ---------------------------------------------------------------------------
# Comandos digitados e resposta do jogador
# ---------------------------------------------------------------------------

def remover_acentos(texto):
    """Remove acentos de um texto (ex.: 'confiável' vira 'confiavel')."""
    decomposto = unicodedata.normalize("NFD", texto)
    return "".join(c for c in decomposto if unicodedata.category(c) != "Mn")


def interpretar_comando(texto):
    """Converte o texto digitado em um comando válido.

    Ignora maiúsculas, espaços extras e acentos.
    Retorna 'confiavel', 'suspeito' ou 'verificar'; ou None se o texto for inválido.
    """
    limpo = remover_acentos(texto.strip().lower())
    if limpo in COMANDOS_VALIDOS:
        return limpo
    return None


def obter_resposta_correta(cartao):
    """Retorna a resposta correta de um cartão: 'confiavel' ou 'suspeito'."""
    if cartao["confiavel"]:
        return "confiavel"
    return "suspeito"


def checar_resposta(cartao, resposta):
    """Verifica se a resposta do jogador ('confiavel' ou 'suspeito') está correta.

    Qualquer outro valor (como 'verificar' ou None) não é uma resposta e retorna False.
    """
    if resposta not in ("confiavel", "suspeito"):
        return False
    return resposta == obter_resposta_correta(cartao)


# ---------------------------------------------------------------------------
# Estado da partida
# ---------------------------------------------------------------------------

def criar_estado():
    """Cria o estado inicial de uma partida.

    Campos:
      pontos, vidas, indice (cartão atual, começando em 0);
      pista_visivel (se o jogador já verificou o cartão atual);
      mensagem / tipo_mensagem (feedback mostrado na tela);
      resultado (None enquanto espera resposta; 'acerto' ou 'erro' depois de responder);
      fim (None durante a partida; 'vitoria' ou 'derrota' quando a partida acaba).
    """
    return {
        "pontos": 0,
        "vidas": VIDAS_INICIAIS,
        "indice": 0,
        "pista_visivel": False,
        "mensagem": "",
        "tipo_mensagem": None,
        "resultado": None,
        "fim": None,
    }


def processar_comando(estado, cartao, comando, total_cartoes):
    """Aplica um comando do jogador ao estado da partida.

    - Comando inválido (None): só mostra aviso, sem perder nada.
    - 'verificar': revela a pista e desconta pontos (apenas uma vez por cartão).
    - 'confiavel' / 'suspeito': acerto soma pontos; erro tira uma vida.
    Ao responder, também define se a partida acabou (vitória ou derrota).

    Modifica o dicionário 'estado' e também o retorna.
    """
    # Depois de responder, o jogador precisa avançar para o próximo cartão.
    if estado["resultado"] is not None:
        return estado

    if comando is None:
        estado["mensagem"] = "Comando inválido. Digite confiavel, suspeito ou verificar."
        estado["tipo_mensagem"] = "invalido"
        return estado

    if comando == "verificar":
        if estado["pista_visivel"]:
            estado["mensagem"] = "Você já pediu a pista deste cartão."
            estado["tipo_mensagem"] = "info"
        else:
            estado["pista_visivel"] = True
            novos_pontos = calcular_pontos(estado["pontos"], -CUSTO_VERIFICACAO)
            estado["pontos"] = max(0, novos_pontos)
            estado["mensagem"] = "Pista revelada (-%d ponto)." % CUSTO_VERIFICACAO
            estado["tipo_mensagem"] = "info"
        return estado

    # Daqui em diante o comando é 'confiavel' ou 'suspeito'.
    if checar_resposta(cartao, comando):
        estado["pontos"] = calcular_pontos(estado["pontos"], PONTOS_ACERTO)
        estado["resultado"] = "acerto"
        estado["mensagem"] = "Correto! +%d pontos." % PONTOS_ACERTO
        estado["tipo_mensagem"] = "acerto"
    else:
        estado["vidas"] = tomar_dano(estado["vidas"], 1)
        estado["resultado"] = "erro"
        correta = obter_resposta_correta(cartao)
        estado["mensagem"] = "Errado! Este cartão era %s. -1 vida." % ROTULOS[correta]
        estado["tipo_mensagem"] = "erro"

    if jogador_perdeu(estado["vidas"]):
        estado["fim"] = "derrota"
    elif estado["indice"] + 1 >= total_cartoes:
        estado["fim"] = "vitoria"

    return estado


def avancar_cartao(estado):
    """Passa para o próximo cartão, limpando pista, mensagem e resultado."""
    estado["indice"] += 1
    estado["pista_visivel"] = False
    estado["mensagem"] = ""
    estado["tipo_mensagem"] = None
    estado["resultado"] = None
    return estado


def e_novo_recorde(pontos, recorde):
    """Indica se a pontuação da partida superou o recorde salvo."""
    return pontos > recorde


# ---------------------------------------------------------------------------
# Texto na tela
# ---------------------------------------------------------------------------

def quebrar_texto(texto, largura_max, medir_largura):
    """Divide um texto em linhas que cabem em 'largura_max' pixels.

    'medir_largura' é uma função que recebe um texto e devolve sua largura em pixels
    (no jogo, usamos fonte.size; nos testes, uma função simples).
    """
    linhas = []
    linha_atual = ""
    for palavra in texto.split():
        tentativa = palavra if linha_atual == "" else linha_atual + " " + palavra
        if medir_largura(tentativa) <= largura_max or linha_atual == "":
            linha_atual = tentativa
        else:
            linhas.append(linha_atual)
            linha_atual = palavra
    if linha_atual != "":
        linhas.append(linha_atual)
    return linhas
