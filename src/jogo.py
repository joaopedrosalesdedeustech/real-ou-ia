"""Interface em Pygame e loop principal do jogo "Real ou IA?".

As regras ficam em src/funcoes.py e a leitura de arquivos em src/dados.py.
Aqui ficam apenas o que aparece na tela e a leitura do teclado.
"""
import pygame

from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    TITULO_JOGO,
    FUNDO,
    BRANCO,
    CINZA,
    CINZA_ESCURO,
    AZUL_CLARO,
    TEXTO_ESCURO,
    VERDE,
    VERMELHO,
    AMARELO,
    AMARELO_FUNDO,
    LARANJA,
    VIDAS_INICIAIS,
    CUSTO_VERIFICACAO,
    MAX_CARACTERES_COMANDO,
    CARTOES_POR_PARTIDA,
)
from src.funcoes import (
    criar_estado,
    interpretar_comando,
    processar_comando,
    avancar_cartao,
    quebrar_texto,
    e_novo_recorde,
    sortear_cartoes,
)
from src.dados import carregar_cartoes, carregar_recorde, salvar_recorde

# Cores das mensagens de feedback, de acordo com o tipo da mensagem.
COR_MENSAGEM = {
    "acerto": VERDE,
    "erro": VERMELHO,
    "invalido": LARANJA,
    "info": AZUL_CLARO,
}

# Área do cartão na tela: (x, y, largura, altura).
AREA_CARTAO = pygame.Rect(50, 100, 700, 200)
AREA_PISTA = pygame.Rect(50, 318, 700, 100)
AREA_DIGITACAO = pygame.Rect(50, 505, 700, 52)


# ---------------------------------------------------------------------------
# Funções de desenho
# ---------------------------------------------------------------------------

def criar_fontes():
    """Cria as fontes usadas no jogo e retorna um dicionário com elas."""
    def fonte(tamanho, negrito=False):
        """Cria uma fonte Arial do sistema (ou a fonte padrão, se a Arial não existir)."""
        return pygame.font.SysFont("arial", tamanho, bold=negrito)

    return {
        "titulo": fonte(58, True),
        "grande": fonte(32, True),
        "media": fonte(26),
        "media_negrito": fonte(26, True),
        "pequena": fonte(20),
        "minima": fonte(16),
        # Tamanhos do texto do cartão, do maior para o menor (cabe mais texto nos menores).
        "cartao": [fonte(30), fonte(26), fonte(22)],
    }


def desenhar_texto(tela, texto, fonte, cor, x, y, alinhamento="esquerda"):
    """Desenha um texto na posição (x, y). O alinhamento pode ser esquerda, centro ou direita."""
    imagem = fonte.render(texto, True, cor)
    retangulo = imagem.get_rect()
    if alinhamento == "centro":
        retangulo.midtop = (x, y)
    elif alinhamento == "direita":
        retangulo.topright = (x, y)
    else:
        retangulo.topleft = (x, y)
    tela.blit(imagem, retangulo)


def desenhar_texto_quebrado(tela, texto, fonte, cor, x, y, largura_max, alinhamento="esquerda"):
    """Desenha um texto em várias linhas e retorna a altura total ocupada."""
    linhas = quebrar_texto(texto, largura_max, lambda t: fonte.size(t)[0])
    altura_linha = fonte.get_linesize()
    for i, linha in enumerate(linhas):
        desenhar_texto(tela, linha, fonte, cor, x, y + i * altura_linha, alinhamento)
    return len(linhas) * altura_linha


def escolher_fonte_do_cartao(texto, fontes, largura_max, altura_max):
    """Escolhe a maior fonte em que o texto do cartão cabe na área disponível."""
    for fonte in fontes["cartao"]:
        linhas = quebrar_texto(texto, largura_max, lambda t, f=fonte: f.size(t)[0])
        if len(linhas) * fonte.get_linesize() <= altura_max:
            return fonte
    return fontes["cartao"][-1]


def desenhar_cabecalho(tela, fontes, estado, total_cartoes, recorde):
    """Desenha a barra do topo: pontos, recorde, vidas e número do cartão."""
    pygame.draw.rect(tela, CINZA_ESCURO, (0, 0, LARGURA_TELA, 80))

    desenhar_texto(tela, "Pontos: %d" % estado["pontos"], fontes["grande"], BRANCO, 24, 10)
    desenhar_texto(tela, "Recorde: %d" % recorde, fontes["pequena"], CINZA, 24, 50)

    # Vidas: círculos cheios (vidas restantes) e vazios (vidas perdidas).
    desenhar_texto(tela, "Vidas", fontes["pequena"], CINZA, LARGURA_TELA // 2, 10, "centro")
    for i in range(VIDAS_INICIAIS):
        x = LARGURA_TELA // 2 + (i - (VIDAS_INICIAIS - 1) / 2) * 34
        if i < estado["vidas"]:
            pygame.draw.circle(tela, VERMELHO, (int(x), 56), 12)
        else:
            pygame.draw.circle(tela, CINZA, (int(x), 56), 12, 2)

    numero = min(estado["indice"] + 1, total_cartoes)
    desenhar_texto(tela, "Cartão", fontes["pequena"], CINZA, LARGURA_TELA - 24, 10, "direita")
    desenhar_texto(tela, "%d / %d" % (numero, total_cartoes), fontes["grande"], BRANCO,
                   LARGURA_TELA - 24, 32, "direita")


def desenhar_cartao(tela, fontes, cartao):
    """Desenha o cartão com o texto que o jogador precisa analisar."""
    pygame.draw.rect(tela, BRANCO, AREA_CARTAO, border_radius=16)
    desenhar_texto(tela, "MENSAGEM PARA ANALISAR", fontes["minima"], CINZA_ESCURO,
                   AREA_CARTAO.x + 24, AREA_CARTAO.y + 16)

    largura_texto = AREA_CARTAO.width - 60
    altura_texto = AREA_CARTAO.height - 60
    fonte = escolher_fonte_do_cartao(cartao["texto"], fontes, largura_texto, altura_texto)
    linhas = quebrar_texto(cartao["texto"], largura_texto, lambda t: fonte.size(t)[0])
    altura_total = len(linhas) * fonte.get_linesize()
    y_inicial = AREA_CARTAO.y + 44 + (altura_texto - altura_total) // 2
    for i, linha in enumerate(linhas):
        desenhar_texto(tela, linha, fonte, TEXTO_ESCURO, AREA_CARTAO.centerx,
                       y_inicial + i * fonte.get_linesize(), "centro")


def desenhar_pista(tela, fontes, estado, cartao):
    """Desenha a pista (se foi pedida) ou a explicação (depois de responder)."""
    respondeu = estado["resultado"] is not None
    if estado["pista_visivel"] or respondeu:
        pygame.draw.rect(tela, AMARELO_FUNDO, AREA_PISTA, border_radius=12)
        pygame.draw.rect(tela, AMARELO, AREA_PISTA, 3, border_radius=12)
        titulo = "Explicação:" if respondeu else "Pista:"
        desenhar_texto(tela, titulo, fontes["media_negrito"], TEXTO_ESCURO,
                       AREA_PISTA.x + 18, AREA_PISTA.y + 8)
        desenhar_texto_quebrado(tela, cartao["pista"], fontes["pequena"], TEXTO_ESCURO,
                                AREA_PISTA.x + 18, AREA_PISTA.y + 40, AREA_PISTA.width - 36)
    else:
        dica = "Em dúvida? Digite verificar para ver uma pista (custa %d ponto)." % (
            CUSTO_VERIFICACAO
        )
        desenhar_texto(tela, dica, fontes["pequena"], CINZA, AREA_PISTA.centerx,
                       AREA_PISTA.y + 36, "centro")


def desenhar_mensagem(tela, fontes, estado):
    """Desenha a mensagem de feedback (acerto, erro, aviso ou informação)."""
    if estado["mensagem"] == "":
        return
    cor = COR_MENSAGEM.get(estado["tipo_mensagem"], BRANCO)
    desenhar_texto(tela, estado["mensagem"], fontes["media_negrito"], cor,
                   LARGURA_TELA // 2, 440, "centro")


def desenhar_caixa_digitacao(tela, fontes, estado, texto_digitado, tempo_ms):
    """Desenha a caixa onde o jogador digita o comando (ou o aviso para continuar)."""
    if estado["resultado"] is not None:
        pygame.draw.rect(tela, CINZA_ESCURO, AREA_DIGITACAO, border_radius=10)
        if estado["fim"] is not None:
            aviso = "Pressione ENTER para ver o resultado final"
        else:
            aviso = "Pressione ENTER para o próximo cartão"
        desenhar_texto(tela, aviso, fontes["media"], BRANCO, AREA_DIGITACAO.centerx,
                       AREA_DIGITACAO.y + 12, "centro")
        return

    desenhar_texto(tela, "Digite: confiavel, suspeito ou verificar  (e aperte ENTER)",
                   fontes["pequena"], AZUL_CLARO, AREA_DIGITACAO.x, AREA_DIGITACAO.y - 28)
    pygame.draw.rect(tela, BRANCO, AREA_DIGITACAO, border_radius=10)
    pygame.draw.rect(tela, AZUL_CLARO, AREA_DIGITACAO, 3, border_radius=10)
    desenhar_texto(tela, texto_digitado, fontes["grande"], TEXTO_ESCURO,
                   AREA_DIGITACAO.x + 16, AREA_DIGITACAO.y + 8)

    # Cursor piscando ao lado do texto digitado.
    if (tempo_ms // 500) % 2 == 0:
        largura = fontes["grande"].size(texto_digitado)[0]
        x_cursor = AREA_DIGITACAO.x + 18 + largura
        pygame.draw.line(tela, TEXTO_ESCURO, (x_cursor, AREA_DIGITACAO.y + 10),
                         (x_cursor, AREA_DIGITACAO.bottom - 10), 2)


def desenhar_tela_jogo(tela, fontes, estado, cartoes, texto_digitado, recorde, tempo_ms):
    """Desenha a tela principal do jogo."""
    tela.fill(FUNDO)
    cartao = cartoes[estado["indice"]]
    desenhar_cabecalho(tela, fontes, estado, len(cartoes), recorde)
    desenhar_cartao(tela, fontes, cartao)
    desenhar_pista(tela, fontes, estado, cartao)
    desenhar_mensagem(tela, fontes, estado)
    desenhar_caixa_digitacao(tela, fontes, estado, texto_digitado, tempo_ms)
    desenhar_texto(tela, "ESC: sair", fontes["minima"], CINZA, LARGURA_TELA - 16, ALTURA_TELA - 28,
                   "direita")


def desenhar_tela_fim(tela, fontes, estado, total_cartoes, recorde, novo_recorde):
    """Desenha a tela de resultado final (vitória ou derrota)."""
    tela.fill(FUNDO)
    venceu = estado["fim"] == "vitoria"
    titulo = "VITÓRIA!" if venceu else "FIM DE JOGO"
    cor = VERDE if venceu else VERMELHO
    if venceu:
        subtitulo = "Você analisou todos os cartões com cuidado."
    else:
        subtitulo = "Suas vidas acabaram. Conferir antes de confiar faz diferença!"

    desenhar_texto(tela, titulo, fontes["titulo"], cor, LARGURA_TELA // 2, 110, "centro")
    desenhar_texto(tela, subtitulo, fontes["media"], BRANCO, LARGURA_TELA // 2, 190, "centro")

    respondidos = estado["indice"] + 1
    desenhar_texto(tela, "Pontuação: %d" % estado["pontos"], fontes["grande"], BRANCO,
                   LARGURA_TELA // 2, 270, "centro")
    desenhar_texto(tela, "Cartões respondidos: %d de %d" % (respondidos, total_cartoes),
                   fontes["media"], CINZA, LARGURA_TELA // 2, 320, "centro")
    desenhar_texto(tela, "Recorde: %d" % recorde, fontes["media"], CINZA,
                   LARGURA_TELA // 2, 360, "centro")
    if novo_recorde:
        desenhar_texto(tela, "Novo recorde!", fontes["grande"], AMARELO,
                       LARGURA_TELA // 2, 410, "centro")

    desenhar_texto(tela, "ENTER: jogar novamente     ESC: sair", fontes["media"], AZUL_CLARO,
                   LARGURA_TELA // 2, 510, "centro")


# ---------------------------------------------------------------------------
# Loop principal
# ---------------------------------------------------------------------------

def executar_jogo():
    """Executa o loop principal do jogo: teclado, regras e desenho da tela."""
    try:
        todos_os_cartoes = carregar_cartoes()
    except (OSError, ValueError) as erro:
        print("Não foi possível carregar os cartões (data/cartoes.json): %s" % erro)
        return

    if len(todos_os_cartoes) == 0:
        print("O arquivo data/cartoes.json não tem nenhum cartão.")
        return

    # Cada partida usa cartões sorteados, em ordem aleatória (e muda a cada nova partida).
    cartoes = sortear_cartoes(todos_os_cartoes, CARTOES_POR_PARTIDA)

    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)
    if hasattr(pygame.key, "start_text_input"):
        pygame.key.start_text_input()

    fontes = criar_fontes()
    relogio = pygame.time.Clock()

    try:
        recorde = carregar_recorde()
    except OSError as erro:
        # Sem acesso ao arquivo: o jogo funciona normalmente, começando com recorde 0.
        print("Não foi possível ler o recorde: %s" % erro)
        recorde = 0
    novo_recorde = False
    estado = criar_estado()
    texto_digitado = ""
    tela_atual = "jogo"  # "jogo" ou "fim"
    rodando = True

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            elif evento.type == pygame.TEXTINPUT:
                # Letras digitadas (inclui acentos). Só aceita enquanto espera um comando.
                pode_digitar = tela_atual == "jogo" and estado["resultado"] is None
                if pode_digitar and len(texto_digitado) < MAX_CARACTERES_COMANDO:
                    texto_digitado += evento.text

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False

                elif evento.key == pygame.K_BACKSPACE:
                    texto_digitado = texto_digitado[:-1]

                elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    if tela_atual == "fim":
                        # Começa uma nova partida, com novos cartões sorteados.
                        cartoes = sortear_cartoes(todos_os_cartoes, CARTOES_POR_PARTIDA)
                        estado = criar_estado()
                        texto_digitado = ""
                        novo_recorde = False
                        tela_atual = "jogo"

                    elif estado["resultado"] is not None:
                        # O jogador já respondeu: avança ou mostra o resultado final.
                        if estado["fim"] is not None:
                            novo_recorde = e_novo_recorde(estado["pontos"], recorde)
                            # salvar_recorde só grava se a pontuação for maior
                            # e devolve o maior valor registrado.
                            try:
                                recorde = salvar_recorde(estado["pontos"])
                            except OSError as erro:
                                # Sem permissão para gravar: o jogo continua sem guardar o recorde.
                                print("Não foi possível salvar o recorde: %s" % erro)
                                recorde = max(recorde, estado["pontos"])
                            tela_atual = "fim"
                        else:
                            avancar_cartao(estado)

                    else:
                        comando = interpretar_comando(texto_digitado)
                        cartao = cartoes[estado["indice"]]
                        processar_comando(estado, cartao, comando, len(cartoes))
                        texto_digitado = ""

        if tela_atual == "jogo":
            desenhar_tela_jogo(tela, fontes, estado, cartoes, texto_digitado, recorde,
                               pygame.time.get_ticks())
        else:
            desenhar_tela_fim(tela, fontes, estado, len(cartoes), recorde, novo_recorde)

        pygame.display.flip()
        relogio.tick(FPS)

    pygame.quit()
