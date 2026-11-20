"""Configurações centrais do jogo (tela, cores e regras).

Os caminhos de cartoes.json e recorde.txt ficam em src/dados.py.
"""

# --- Tela ---
LARGURA_TELA = 800
ALTURA_TELA = 600
FPS = 60

TITULO_JOGO = "Real ou IA?"

# --- Cores ---
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (212, 212, 212)
FUNDO = (28, 33, 48)
AZUL_CLARO = (120, 170, 255)
CINZA_ESCURO = (60, 66, 84)
TEXTO_ESCURO = (30, 34, 45)
VERDE = (60, 190, 110)
VERMELHO = (225, 80, 80)
AMARELO = (250, 220, 120)
AMARELO_FUNDO = (255, 246, 214)
LARANJA = (240, 160, 60)

# --- Regras do jogo ---
VIDAS_INICIAIS = 3
PONTOS_ACERTO = 10
CUSTO_VERIFICACAO = 1
COMANDOS_VALIDOS = ("confiavel", "suspeito", "verificar")
# Como cada resposta aparece escrita na tela (com acento).
ROTULOS = {"confiavel": "confiável", "suspeito": "suspeito"}
MAX_CARACTERES_COMANDO = 20

# --- Caminhos de arquivos ---
CAMINHO_SPRITES = "assets/imagens/spritesheet.bmp"
