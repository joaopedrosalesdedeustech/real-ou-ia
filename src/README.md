# Código-fonte (`src`)

Esta pasta contém os módulos principais do jogo **Real ou IA?**.

## Arquivos

- `jogo.py`: interface em Pygame e loop principal (eventos de teclado, desenho da tela do jogo e da tela de resultado final).
- `funcoes.py`: regras do jogo, sem depender do Pygame (interpretar comandos, checar respostas, pontos, vidas, vitória e derrota, sorteio de cartões e quebra de texto).
- `dados.py`: leitura e validação dos cartões (`data/cartoes.json`) e leitura/gravação do recorde (`data/recorde.txt`).
- `config.py`: constantes globais (tela, cores e regras do jogo).
- `sprites.py`: arquivo do template para recorte de spritesheet. **Não é usado neste jogo.**

## Como as partes se conectam

`main.py` chama `executar_jogo()` (em `jogo.py`). O loop lê o teclado, entrega o comando digitado a `processar_comando()` (em `funcoes.py`), que atualiza o estado da partida, e então desenha a tela. Os cartões e o recorde vêm de `dados.py`.

## Dica de evolução

Mantenha módulos pequenos e separados por responsabilidade: regras em `funcoes.py`, arquivos em `dados.py` e tudo que depende do Pygame em `jogo.py`.
