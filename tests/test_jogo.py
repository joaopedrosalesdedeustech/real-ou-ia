"""Testes da interface (src/jogo.py) e de partidas completas, sem abrir janela.

O Pygame roda com o driver de vídeo "dummy" (sem tela). As partidas são simuladas
enviando eventos de teclado falsos, quadro a quadro, para o loop principal.
"""
# flake8: noqa: E402  (os imports vêm depois de configurar o Pygame sem janela, de propósito)
import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import json
from types import SimpleNamespace

import pygame
import pytest

from src import dados, jogo
from src.config import (
    CARTOES_POR_PARTIDA,
    LARGURA_TELA,
    ALTURA_TELA,
    FUNDO,
    BRANCO,
    CINZA_ESCURO,
    VERMELHO,
    AMARELO_FUNDO,
    TEXTO_ESCURO,
)
from src.funcoes import criar_estado

# Três cartões de teste: o gabarito é conhecido e não depende do arquivo real.
CARTOES_TESTE = [
    {"texto": "Cartão um", "confiavel": True, "pista": "Pista um"},
    {"texto": "Cartão dois", "confiavel": False, "pista": "Pista dois"},
    {"texto": "Cartão três", "confiavel": True, "pista": "Pista três"},
]


# ---------------------------------------------------------------------------
# Eventos de teclado falsos
# ---------------------------------------------------------------------------

def digitar(texto):
    """Eventos de texto digitado, uma letra por evento."""
    return [pygame.event.Event(pygame.TEXTINPUT, text=letra) for letra in texto]


def enter():
    """Evento da tecla Enter."""
    return [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode="\r")]


def backspace():
    """Evento da tecla Backspace."""
    return [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_BACKSPACE, mod=0, unicode="")]


def esc():
    """Evento da tecla ESC."""
    return [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode="")]


def resposta_certa(cartao):
    """Comando que acerta o cartão."""
    return "confiavel" if cartao["confiavel"] else "suspeito"


def resposta_errada(cartao):
    """Comando que erra o cartão."""
    return "suspeito" if cartao["confiavel"] else "confiavel"


def quadros_respondendo(cartoes, escolher_resposta):
    """Monta os quadros de uma partida: responde cada cartão e aperta Enter para avançar.

    O último Enter leva à tela de resultado final (e grava o recorde, se for o caso).
    """
    quadros = []
    for cartao in cartoes:
        quadros.append(digitar(escolher_resposta(cartao)) + enter())
        quadros.append(enter())
    return quadros


# ---------------------------------------------------------------------------
# Fixture que roda o loop principal com os eventos falsos
# ---------------------------------------------------------------------------

@pytest.fixture
def jogar(tmp_path, monkeypatch):
    """Retorna uma função que executa o jogo com eventos falsos e arquivos temporários.

    Uso: resultado = jogar(quadros, cartoes=CARTOES_TESTE, recorde=0)
    O resultado tem: recorde_final (int) e saiu_cedo (True se o jogo fechou
    antes de acabarem os quadros, por exemplo com ESC).
    """
    def executar(quadros, cartoes=CARTOES_TESTE, recorde=0, sorteio=None):
        """Roda o jogo com os quadros de eventos informados e devolve o resultado.

        Por padrão o sorteio de cartões é trocado por um que mantém a ordem do arquivo,
        para que os testes saibam qual cartão aparece em cada rodada.
        """
        if sorteio is None:
            def sorteio(lista, quantidade):
                """Pega os primeiros cartões, sem embaralhar."""
                return lista[:quantidade]
        monkeypatch.setattr(jogo, "sortear_cartoes", sorteio)

        arquivo_recorde = tmp_path / "recorde.txt"
        arquivo_recorde.write_text(str(recorde), encoding="utf-8")
        monkeypatch.setattr(dados, "ARQUIVO_RECORDE", arquivo_recorde)

        if cartoes is not None:
            arquivo_cartoes = tmp_path / "cartoes.json"
            arquivo_cartoes.write_text(json.dumps(cartoes), encoding="utf-8")
            monkeypatch.setattr(dados, "ARQUIVO_CARTOES", arquivo_cartoes)

        monkeypatch.setattr(jogo, "FPS", 0)  # sem esperar entre os quadros

        controle = {"proximo": 0}

        def eventos_falsos():
            """Devolve os eventos do próximo quadro; depois do último, fecha a janela."""
            if controle["proximo"] >= len(quadros):
                return [pygame.event.Event(pygame.QUIT)]
            quadro = quadros[controle["proximo"]]
            controle["proximo"] += 1
            return quadro

        monkeypatch.setattr(pygame.event, "get", eventos_falsos)
        jogo.executar_jogo()

        return SimpleNamespace(
            recorde_final=int(arquivo_recorde.read_text(encoding="utf-8").strip()),
            saiu_cedo=controle["proximo"] < len(quadros),
        )

    return executar


# ---------------------------------------------------------------------------
# Partidas completas
# ---------------------------------------------------------------------------

def test_partida_perfeita_grava_novo_recorde(jogar):
    """Acertar todos os cartões (3 x 10 pontos) deve gravar 30 como recorde."""
    quadros = quadros_respondendo(CARTOES_TESTE, resposta_certa)
    assert jogar(quadros, recorde=0).recorde_final == 30


def test_recorde_maior_nao_e_substituido(jogar):
    """Uma pontuação menor que o recorde não altera o recorde salvo."""
    quadros = quadros_respondendo(CARTOES_TESTE, resposta_certa)
    assert jogar(quadros, recorde=100).recorde_final == 100


def test_derrota_nao_grava_recorde_menor(jogar):
    """Perder as 3 vidas (0 pontos) não altera um recorde já existente."""
    quadros = quadros_respondendo(CARTOES_TESTE, resposta_errada)
    assert jogar(quadros, recorde=40).recorde_final == 40


def test_partida_com_apenas_um_erro_ainda_vence(jogar):
    """Errar um cartão tira uma vida, mas a partida continua; 2 acertos = 20 pontos."""
    respostas = {"Cartão um": resposta_errada}
    quadros = quadros_respondendo(
        CARTOES_TESTE,
        lambda c: respostas.get(c["texto"], resposta_certa)(c),
    )
    assert jogar(quadros, recorde=0).recorde_final == 20


def test_comando_invalido_nao_atrapalha_a_partida(jogar):
    """Digitar um comando inválido no meio da partida não tira pontos nem vidas."""
    quadros = [digitar("talvez") + enter()] + quadros_respondendo(CARTOES_TESTE, resposta_certa)
    assert jogar(quadros, recorde=0).recorde_final == 30


def test_comando_vazio_nao_atrapalha_a_partida(jogar):
    """Apertar Enter sem digitar nada é um comando inválido e não tem efeito."""
    quadros = [enter()] + quadros_respondendo(CARTOES_TESTE, resposta_certa)
    assert jogar(quadros, recorde=0).recorde_final == 30


def test_verificar_desconta_um_ponto(jogar):
    """Pedir a pista no segundo cartão desconta 1 ponto: 30 - 1 = 29."""
    quadros = [
        digitar("confiavel") + enter(), enter(),                        # cartão 1: +10
        digitar("verificar") + enter(),                                 # cartão 2: -1
        digitar("suspeito") + enter(), enter(),                         # cartão 2: +10
        digitar("confiavel") + enter(), enter(),                        # cartão 3: +10
    ]
    assert jogar(quadros, recorde=0).recorde_final == 29


def test_comando_aceita_acento_e_maiusculas(jogar):
    """O jogador pode digitar 'Confiável' ou 'SUSPEITO'."""
    quadros = [
        digitar("Confiável") + enter(), enter(),
        digitar("SUSPEITO") + enter(), enter(),
        digitar("  confiavel ") + enter(), enter(),
    ]
    assert jogar(quadros, recorde=0).recorde_final == 30


def test_backspace_corrige_o_texto_digitado(jogar):
    """Apagar uma letra com Backspace deve permitir corrigir o comando."""
    quadros = [
        digitar("confiavell") + backspace() + enter(), enter(),
        digitar("suspeito") + enter(), enter(),
        digitar("confiavel") + enter(), enter(),
    ]
    assert jogar(quadros, recorde=0).recorde_final == 30


def test_nao_digita_enquanto_mostra_o_resultado(jogar):
    """Texto digitado depois de responder (antes do Enter) é ignorado."""
    quadros = [
        digitar("confiavel") + enter(),
        digitar("lixo"),                      # ignorado: o cartão já foi respondido
        enter(),                              # avança para o cartão 2
        digitar("suspeito") + enter(), enter(),
        digitar("confiavel") + enter(), enter(),
    ]
    assert jogar(quadros, recorde=0).recorde_final == 30


def test_texto_muito_longo_e_limitado(jogar):
    """Digitar muitos caracteres não quebra o jogo (o texto tem limite de tamanho)."""
    quadros = [digitar("a" * 100) + enter()] + quadros_respondendo(CARTOES_TESTE, resposta_certa)
    assert jogar(quadros, recorde=0).recorde_final == 30


def test_esc_encerra_o_jogo(jogar):
    """A tecla ESC fecha o jogo imediatamente."""
    resultado = jogar([[], esc(), [], []], recorde=5)
    assert resultado.saiu_cedo is True
    assert resultado.recorde_final == 5


def test_jogar_novamente_apos_o_fim(jogar):
    """Depois da tela final, Enter começa uma nova partida (que pode ser jogada de novo)."""
    quadros = quadros_respondendo(CARTOES_TESTE, resposta_certa)
    quadros.append(enter())                              # tela final -> nova partida
    quadros += quadros_respondendo(CARTOES_TESTE, resposta_errada)
    assert jogar(quadros, recorde=0).recorde_final == 30


def test_nova_partida_pode_superar_o_recorde_da_anterior(jogar):
    """Uma segunda partida melhor que a primeira atualiza o recorde."""
    erros = {"Cartão um": resposta_errada}
    quadros = quadros_respondendo(
        CARTOES_TESTE, lambda c: erros.get(c["texto"], resposta_certa)(c)
    )                                                    # 20 pontos
    quadros.append(enter())
    quadros += quadros_respondendo(CARTOES_TESTE, resposta_certa)   # 30 pontos
    assert jogar(quadros, recorde=0).recorde_final == 30


def test_partida_completa_com_os_cartoes_reais(jogar):
    """Acertar os 15 cartões de uma partida com o arquivo real deve render 150 pontos."""
    cartoes = dados.carregar_cartoes()[:CARTOES_POR_PARTIDA]
    quadros = quadros_respondendo(cartoes, resposta_certa)
    resultado = jogar(quadros, cartoes=None, recorde=0)
    assert resultado.recorde_final == 10 * CARTOES_POR_PARTIDA


def test_cada_partida_sorteia_novos_cartoes(jogar):
    """O jogo usa a lista sorteada e sorteia de novo ao começar outra partida."""
    chamadas = []

    def sorteio_girado(lista, quantidade):
        """Registra o pedido e devolve os cartões em outra ordem (o primeiro vai para o fim)."""
        chamadas.append(quantidade)
        return lista[1:] + lista[:1]

    ordem_sorteada = CARTOES_TESTE[1:] + CARTOES_TESTE[:1]
    quadros = quadros_respondendo(ordem_sorteada, resposta_certa)
    quadros.append(enter())                                   # tela final -> nova partida
    quadros += quadros_respondendo(ordem_sorteada, resposta_certa)
    resultado = jogar(quadros, recorde=0, sorteio=sorteio_girado)
    assert resultado.recorde_final == 30                      # só acerta se usar a ordem sorteada
    assert chamadas == [CARTOES_POR_PARTIDA, CARTOES_POR_PARTIDA]


# ---------------------------------------------------------------------------
# Falhas nos arquivos de recorde
# ---------------------------------------------------------------------------

def test_erro_ao_salvar_recorde_nao_derruba_o_jogo(jogar, monkeypatch, capsys):
    """Se não for possível gravar o recorde, o jogo avisa e continua até o fim."""
    def salvar_com_erro(pontuacao):
        """Simula um arquivo sem permissão de escrita."""
        raise PermissionError("sem permissão")

    monkeypatch.setattr(jogo, "salvar_recorde", salvar_com_erro)
    quadros = quadros_respondendo(CARTOES_TESTE, resposta_certa) + [esc()]
    resultado = jogar(quadros, recorde=0)  # um erro não tratado derrubaria o teste aqui
    assert "Não foi possível salvar o recorde" in capsys.readouterr().out
    assert resultado.recorde_final == 0  # o arquivo ficou como estava


def test_erro_ao_ler_recorde_nao_derruba_o_jogo(jogar, monkeypatch, capsys):
    """Se não for possível ler o recorde, o jogo avisa e começa com recorde 0."""
    def carregar_com_erro():
        """Simula um arquivo sem permissão de leitura."""
        raise PermissionError("sem permissão")

    monkeypatch.setattr(jogo, "carregar_recorde", carregar_com_erro)
    quadros = quadros_respondendo(CARTOES_TESTE, resposta_certa)
    assert jogar(quadros, recorde=0).recorde_final == 30
    assert "Não foi possível ler o recorde" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# Falhas ao carregar os cartões
# ---------------------------------------------------------------------------

def test_arquivo_de_cartoes_inexistente_mostra_aviso(tmp_path, monkeypatch, capsys):
    """Sem o arquivo de cartões, o jogo avisa e termina sem erro."""
    monkeypatch.setattr(dados, "ARQUIVO_CARTOES", tmp_path / "nao_existe.json")
    jogo.executar_jogo()
    assert "Não foi possível carregar os cartões" in capsys.readouterr().out


def test_arquivo_de_cartoes_invalido_mostra_aviso(tmp_path, monkeypatch, capsys):
    """Com um cartão mal formado, o jogo avisa e termina sem erro."""
    arquivo = tmp_path / "cartoes.json"
    arquivo.write_text(json.dumps([{"texto": "sem os outros campos"}]), encoding="utf-8")
    monkeypatch.setattr(dados, "ARQUIVO_CARTOES", arquivo)
    jogo.executar_jogo()
    assert "Não foi possível carregar os cartões" in capsys.readouterr().out


def test_arquivo_de_cartoes_vazio_mostra_aviso(tmp_path, monkeypatch, capsys):
    """Com a lista de cartões vazia, o jogo avisa e termina sem erro."""
    arquivo = tmp_path / "cartoes.json"
    arquivo.write_text("[]", encoding="utf-8")
    monkeypatch.setattr(dados, "ARQUIVO_CARTOES", arquivo)
    jogo.executar_jogo()
    assert "nenhum cartão" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# Desenho das telas
# ---------------------------------------------------------------------------

@pytest.fixture
def ambiente():
    """Prepara o Pygame, uma superfície do tamanho da tela e as fontes do jogo."""
    pygame.init()
    tela = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
    yield tela, jogo.criar_fontes()
    pygame.quit()


def cor(tela, posicao):
    """Cor (R, G, B) de um pixel da tela."""
    return tuple(tela.get_at(posicao))[:3]


def test_criar_fontes_tem_todas_as_fontes(ambiente):
    """O dicionário de fontes deve ter todas as chaves usadas no desenho."""
    _, fontes = ambiente
    for nome in ("titulo", "grande", "media", "media_negrito", "pequena", "minima"):
        assert nome in fontes
    assert len(fontes["cartao"]) == 3


def test_fonte_do_cartao_texto_curto_usa_a_maior(ambiente):
    """Texto curto cabe na fonte maior."""
    _, fontes = ambiente
    escolhida = jogo.escolher_fonte_do_cartao("Texto curto", fontes, 640, 140)
    assert escolhida is fontes["cartao"][0]


def test_fonte_do_cartao_texto_enorme_usa_a_menor(ambiente):
    """Texto enorme não cabe em nenhuma fonte e usa a menor delas."""
    _, fontes = ambiente
    texto_enorme = "palavra " * 300
    escolhida = jogo.escolher_fonte_do_cartao(texto_enorme, fontes, 640, 140)
    assert escolhida is fontes["cartao"][-1]


def test_desenhar_texto_quebrado_devolve_altura(ambiente):
    """A altura devolvida cresce com o número de linhas do texto."""
    tela, fontes = ambiente
    curto = jogo.desenhar_texto_quebrado(tela, "oi", fontes["pequena"], BRANCO, 10, 10, 600)
    longo = jogo.desenhar_texto_quebrado(
        tela, "palavra " * 60, fontes["pequena"], BRANCO, 10, 10, 200
    )
    assert curto > 0
    assert longo > curto


def test_tela_do_jogo_desenha_fundo_e_cartao(ambiente):
    """A tela do jogo deve ter fundo escuro e o cartão branco."""
    tela, fontes = ambiente
    jogo.desenhar_tela_jogo(tela, fontes, criar_estado(), CARTOES_TESTE, "", 0, 0)
    assert cor(tela, (5, 300)) == FUNDO
    assert cor(tela, (700, 120)) == BRANCO


def test_pista_so_aparece_depois_de_verificar(ambiente):
    """A caixa amarela da pista só é desenhada depois do comando verificar."""
    tela, fontes = ambiente
    estado = criar_estado()
    jogo.desenhar_tela_jogo(tela, fontes, estado, CARTOES_TESTE, "", 0, 0)
    assert cor(tela, (700, 405)) == FUNDO

    estado["pista_visivel"] = True
    jogo.desenhar_tela_jogo(tela, fontes, estado, CARTOES_TESTE, "", 0, 0)
    assert cor(tela, (700, 405)) == AMARELO_FUNDO


def test_explicacao_aparece_depois_de_responder(ambiente):
    """Depois de responder, a caixa da explicação aparece mesmo sem verificar."""
    tela, fontes = ambiente
    estado = criar_estado()
    estado["resultado"] = "acerto"
    estado["mensagem"] = "Correto! +10 pontos."
    estado["tipo_mensagem"] = "acerto"
    jogo.desenhar_tela_jogo(tela, fontes, estado, CARTOES_TESTE, "", 0, 0)
    assert cor(tela, (700, 405)) == AMARELO_FUNDO


def test_cabecalho_mostra_as_vidas_restantes(ambiente):
    """Vidas restantes aparecem como círculos vermelhos; as perdidas, vazias."""
    tela, fontes = ambiente
    estado = criar_estado()
    jogo.desenhar_cabecalho(tela, fontes, estado, 15, 0)
    assert cor(tela, (434, 56)) == VERMELHO  # terceira vida ainda existe

    tela.fill(FUNDO)
    estado["vidas"] = 1
    jogo.desenhar_cabecalho(tela, fontes, estado, 15, 0)
    assert cor(tela, (366, 56)) == VERMELHO       # primeira vida continua
    assert cor(tela, (400, 56)) == CINZA_ESCURO   # segunda vida perdida (círculo vazio)
    assert cor(tela, (434, 56)) == CINZA_ESCURO   # terceira vida perdida (círculo vazio)


def test_cursor_da_caixa_de_texto_pisca(ambiente):
    """O cursor aparece em um instante e some 500 ms depois."""
    tela, fontes = ambiente
    jogo.desenhar_caixa_digitacao(tela, fontes, criar_estado(), "", 0)
    assert cor(tela, (68, 531)) == TEXTO_ESCURO

    jogo.desenhar_caixa_digitacao(tela, fontes, criar_estado(), "", 500)
    assert cor(tela, (68, 531)) == BRANCO


def test_aviso_para_continuar_depois_de_responder(ambiente):
    """Depois de responder, a caixa de digitação é trocada pelo aviso de Enter."""
    tela, fontes = ambiente
    estado = criar_estado()
    estado["resultado"] = "acerto"
    jogo.desenhar_caixa_digitacao(tela, fontes, estado, "", 0)
    assert cor(tela, (60, 510)) == CINZA_ESCURO


def test_tela_de_fim_desenha_vitoria_e_derrota(ambiente):
    """As telas finais de vitória e derrota (com ou sem novo recorde) são desenhadas."""
    tela, fontes = ambiente
    for fim in ("vitoria", "derrota"):
        for novo_recorde in (True, False):
            estado = criar_estado()
            estado["fim"] = fim
            estado["indice"] = 14
            estado["pontos"] = 120
            tela.fill((0, 0, 0))
            jogo.desenhar_tela_fim(tela, fontes, estado, 15, 120, novo_recorde)
            assert cor(tela, (5, 5)) == FUNDO
