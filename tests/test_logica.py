"""Testes das regras do jogo (src/funcoes.py), sem abrir janela."""
import pygame

from src.funcoes import (
    calcular_pontos,
    jogador_perdeu,
    limitar_valor,
    tomar_dano,
    verificar_colisao,
    remover_acentos,
    interpretar_comando,
    obter_resposta_correta,
    checar_resposta,
    criar_estado,
    processar_comando,
    avancar_cartao,
    e_novo_recorde,
    quebrar_texto,
)

CARTAO_CONFIAVEL = {"texto": "A água ferve a 100 °C.", "confiavel": True, "pista": "Fato básico."}
CARTAO_SUSPEITO = {"texto": "Compartilhe e ganhe!", "confiavel": False, "pista": "Corrente."}


# --- Funções do template ---------------------------------------------------

def test_calcular_pontos():
    """Deve somar corretamente os pontos atuais com os pontos ganhos."""
    assert calcular_pontos(10, 5) == 15


def test_calcular_pontos_com_desconto():
    """Deve descontar pontos quando o valor ganho for negativo."""
    assert calcular_pontos(10, -1) == 9


def test_tomar_dano():
    """Deve reduzir a vida de acordo com o dano recebido."""
    assert tomar_dano(3, 1) == 2


def test_jogador_perdeu_com_zero_vidas():
    """Deve indicar derrota quando o total de vidas chega a zero."""
    assert jogador_perdeu(0) is True


def test_jogador_nao_perdeu_com_vidas():
    """Nao deve indicar derrota quando o jogador ainda tem vidas."""
    assert jogador_perdeu(3) is False


def test_verificar_colisao_retangulos_sobrepostos():
    """Retângulos que se sobrepõem colidem."""
    assert verificar_colisao(pygame.Rect(0, 0, 10, 10), pygame.Rect(5, 5, 10, 10)) is True


def test_verificar_colisao_retangulos_separados():
    """Retângulos afastados não colidem."""
    assert verificar_colisao(pygame.Rect(0, 0, 10, 10), pygame.Rect(50, 50, 10, 10)) is False


def test_limitar_valor_abaixo_do_minimo():
    """Deve retornar o limite minimo quando o valor informado for menor."""
    assert limitar_valor(-5, 0, 100) == 0


def test_limitar_valor_acima_do_maximo():
    """Deve retornar o limite maximo quando o valor informado for maior."""
    assert limitar_valor(150, 0, 100) == 100


def test_limitar_valor_dentro_do_intervalo():
    """Deve manter o valor original quando ele ja estiver no intervalo."""
    assert limitar_valor(50, 0, 100) == 50


# --- Interpretação dos comandos digitados ----------------------------------

def test_remover_acentos():
    """Deve remover os acentos do texto."""
    assert remover_acentos("confiável") == "confiavel"


def test_interpretar_comando_aceita_acento_e_maiusculas():
    """Deve aceitar 'Confiável' e converter para 'confiavel'."""
    assert interpretar_comando("Confiável") == "confiavel"


def test_interpretar_comando_ignora_espacos():
    """Deve ignorar espaços extras e maiúsculas."""
    assert interpretar_comando("  SUSPEITO ") == "suspeito"


def test_interpretar_comando_verificar():
    """Deve reconhecer o comando verificar."""
    assert interpretar_comando("verificar") == "verificar"


def test_interpretar_comando_invalido():
    """Deve retornar None para textos que não são comandos."""
    assert interpretar_comando("talvez") is None


def test_interpretar_comando_vazio():
    """Deve retornar None para texto vazio."""
    assert interpretar_comando("") is None


# --- Resposta do jogador ---------------------------------------------------

def test_obter_resposta_correta():
    """Deve devolver o gabarito do cartão em formato de comando."""
    assert obter_resposta_correta(CARTAO_CONFIAVEL) == "confiavel"
    assert obter_resposta_correta(CARTAO_SUSPEITO) == "suspeito"


def test_checar_resposta_acerto_em_cartao_confiavel():
    """Deve acertar ao marcar confiável um cartão confiável."""
    assert checar_resposta(CARTAO_CONFIAVEL, "confiavel") is True


def test_checar_resposta_acerto_em_cartao_suspeito():
    """Deve acertar ao marcar suspeito um cartão suspeito."""
    assert checar_resposta(CARTAO_SUSPEITO, "suspeito") is True


def test_checar_resposta_erro():
    """Deve errar ao marcar confiável um cartão suspeito."""
    assert checar_resposta(CARTAO_SUSPEITO, "confiavel") is False
    assert checar_resposta(CARTAO_CONFIAVEL, "suspeito") is False


def test_checar_resposta_ignora_comandos_que_nao_sao_resposta():
    """Verificar ou None não contam como resposta."""
    assert checar_resposta(CARTAO_CONFIAVEL, "verificar") is False
    assert checar_resposta(CARTAO_CONFIAVEL, None) is False


# --- Estado da partida ------------------------------------------------------

def test_criar_estado_inicial():
    """A partida começa com 0 pontos, 3 vidas e no primeiro cartão."""
    estado = criar_estado()
    assert estado["pontos"] == 0
    assert estado["vidas"] == 3
    assert estado["indice"] == 0
    assert estado["resultado"] is None
    assert estado["fim"] is None


def test_acerto_soma_10_pontos():
    """Acertar deve somar 10 pontos e não tirar vida."""
    estado = criar_estado()
    processar_comando(estado, CARTAO_SUSPEITO, "suspeito", 15)
    assert estado["pontos"] == 10
    assert estado["vidas"] == 3
    assert estado["resultado"] == "acerto"


def test_erro_tira_uma_vida():
    """Errar deve tirar 1 vida e não mexer nos pontos."""
    estado = criar_estado()
    processar_comando(estado, CARTAO_SUSPEITO, "confiavel", 15)
    assert estado["pontos"] == 0
    assert estado["vidas"] == 2
    assert estado["resultado"] == "erro"


def test_mensagem_de_erro_mostra_a_resposta_correta_com_acento():
    """A mensagem de erro diz qual era a resposta certa, escrita com acento."""
    estado = criar_estado()
    processar_comando(estado, CARTAO_CONFIAVEL, "suspeito", 15)
    assert "confiável" in estado["mensagem"]

    estado = criar_estado()
    processar_comando(estado, CARTAO_SUSPEITO, "confiavel", 15)
    assert "suspeito" in estado["mensagem"]


def test_verificar_mostra_pista_e_desconta_um_ponto():
    """Verificar deve revelar a pista e descontar 1 ponto."""
    estado = criar_estado()
    estado["pontos"] = 10
    processar_comando(estado, CARTAO_SUSPEITO, "verificar", 15)
    assert estado["pista_visivel"] is True
    assert estado["pontos"] == 9
    assert estado["resultado"] is None


def test_verificar_duas_vezes_cobra_so_uma_vez():
    """Pedir a pista de novo no mesmo cartão não deve descontar outro ponto."""
    estado = criar_estado()
    estado["pontos"] = 10
    processar_comando(estado, CARTAO_SUSPEITO, "verificar", 15)
    processar_comando(estado, CARTAO_SUSPEITO, "verificar", 15)
    assert estado["pontos"] == 9


def test_verificar_nao_deixa_pontos_negativos():
    """Os pontos nunca ficam abaixo de zero."""
    estado = criar_estado()
    processar_comando(estado, CARTAO_SUSPEITO, "verificar", 15)
    assert estado["pontos"] == 0


def test_comando_invalido_nao_altera_nada():
    """Comando inválido mostra aviso, sem alterar pontos nem vidas."""
    estado = criar_estado()
    processar_comando(estado, CARTAO_SUSPEITO, None, 15)
    assert estado["pontos"] == 0
    assert estado["vidas"] == 3
    assert estado["resultado"] is None
    assert estado["tipo_mensagem"] == "invalido"


def test_nao_responde_duas_vezes_o_mesmo_cartao():
    """Depois de responder, novos comandos são ignorados até avançar de cartão."""
    estado = criar_estado()
    processar_comando(estado, CARTAO_SUSPEITO, "suspeito", 15)
    processar_comando(estado, CARTAO_SUSPEITO, "suspeito", 15)
    assert estado["pontos"] == 10


def test_avancar_cartao_limpa_o_estado_do_cartao():
    """Avançar deve ir ao próximo cartão e limpar pista, mensagem e resultado."""
    estado = criar_estado()
    processar_comando(estado, CARTAO_SUSPEITO, "verificar", 15)
    processar_comando(estado, CARTAO_SUSPEITO, "suspeito", 15)
    avancar_cartao(estado)
    assert estado["indice"] == 1
    assert estado["pista_visivel"] is False
    assert estado["mensagem"] == ""
    assert estado["resultado"] is None


def test_derrota_quando_vidas_acabam():
    """A partida termina em derrota quando as 3 vidas acabam."""
    estado = criar_estado()
    for _ in range(3):
        processar_comando(estado, CARTAO_SUSPEITO, "confiavel", 15)
        if estado["fim"] is None:
            avancar_cartao(estado)
    assert estado["vidas"] == 0
    assert estado["fim"] == "derrota"


def test_vitoria_ao_responder_ultimo_cartao_com_vidas():
    """Responder o último cartão ainda com vidas termina em vitória."""
    estado = criar_estado()
    total = 3
    for _ in range(total):
        processar_comando(estado, CARTAO_SUSPEITO, "suspeito", total)
        if estado["fim"] is None:
            avancar_cartao(estado)
    assert estado["fim"] == "vitoria"
    assert estado["pontos"] == 30


def test_derrota_no_ultimo_cartao_vale_derrota():
    """Se as vidas acabam justamente no último cartão, o resultado é derrota."""
    estado = criar_estado()
    estado["vidas"] = 1
    estado["indice"] = 2
    processar_comando(estado, CARTAO_SUSPEITO, "confiavel", 3)
    assert estado["fim"] == "derrota"


def test_sem_fim_no_meio_da_partida():
    """Durante a partida normal, o campo fim continua vazio."""
    estado = criar_estado()
    processar_comando(estado, CARTAO_SUSPEITO, "suspeito", 15)
    assert estado["fim"] is None


# --- Recorde ---------------------------------------------------------------

def test_novo_recorde():
    """Pontuação maior que o recorde é novo recorde."""
    assert e_novo_recorde(50, 40) is True


def test_nao_e_novo_recorde_se_igual_ou_menor():
    """Pontuação igual ou menor que o recorde não é novo recorde."""
    assert e_novo_recorde(40, 40) is False
    assert e_novo_recorde(10, 40) is False


# --- Quebra de texto -------------------------------------------------------

def medir(texto):
    """Mede a largura de um texto como 10 pixels por caractere (apenas para os testes)."""
    return len(texto) * 10


def test_quebrar_texto_cabe_em_uma_linha():
    """Texto curto deve ficar em uma única linha."""
    assert quebrar_texto("uma frase curta", 400, medir) == ["uma frase curta"]


def test_quebrar_texto_em_varias_linhas():
    """Texto longo deve ser dividido em linhas que cabem na largura."""
    linhas = quebrar_texto("aaa bbb ccc ddd", 70, medir)
    assert linhas == ["aaa bbb", "ccc ddd"]
    assert all(medir(linha) <= 70 for linha in linhas)


def test_quebrar_texto_palavra_maior_que_a_linha():
    """Uma palavra gigante fica sozinha na linha, sem travar."""
    assert quebrar_texto("supercalifragilistico oi", 50, medir) == ["supercalifragilistico", "oi"]


def test_quebrar_texto_vazio():
    """Texto vazio não gera linhas."""
    assert quebrar_texto("", 100, medir) == []
