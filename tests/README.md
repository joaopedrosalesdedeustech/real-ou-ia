# Testes

Esta pasta contém os testes automatizados do jogo **Real ou IA?**, escritos com `pytest`.
Nenhum teste abre janela: o Pygame roda com o driver de vídeo "dummy" e nenhum teste altera os arquivos reais de `data/`.

## Arquivos

| Arquivo | O que testa |
|---|---|
| `test_logica.py` | Regras do jogo em `src/funcoes.py`: interpretação dos comandos digitados, acerto e erro, pontos, vidas, vitória e derrota, recorde e quebra de texto em linhas. |
| `test_dados.py` | Leitura e gravação de arquivos em `src/dados.py`: recorde (arquivo ausente, vazio, inválido, maior e menor) e cartões (campos obrigatórios, tipos e erros). Também confere o arquivo real `data/cartoes.json`: 15 cartões, sem repetição, de tamanho adequado e com os dois tipos. |
| `test_jogo.py` | Interface em `src/jogo.py`: desenho das telas (cartão, pista, vidas, cursor, tela final) e **partidas completas simuladas** com eventos de teclado falsos (vitória, derrota, comando inválido, Backspace, ESC, jogar novamente e falhas ao carregar os cartões). |

## Como executar

```bash
python -m pytest            # roda todos os testes
python -m pytest -v         # mostra o nome de cada teste
python -m pytest tests/test_logica.py   # roda só um arquivo
```

Para ver a cobertura (opcional, precisa do pacote `pytest-cov`):

```bash
pip install pytest-cov
python -m pytest --cov=src --cov-report=term-missing
```

## Como os testes simulam uma partida

O teste `test_jogo.py` troca `pygame.event.get` por uma função que devolve, a cada quadro do jogo, uma lista de eventos pré-definidos (letras digitadas, Enter, Backspace, ESC). Assim o loop principal roda de verdade, do início ao fim, sem ninguém digitando. Os arquivos de recorde e de cartões são trocados por arquivos temporários (fixture `tmp_path` e `monkeypatch`), então o `data/recorde.txt` verdadeiro nunca é alterado.

## Boas práticas

- Crie testes para toda regra de pontuação, vidas e condições de fim de jogo.
- Prefira funções pequenas e testáveis em `src/funcoes.py`, que não dependem do Pygame.
- Ao mudar uma regra (por exemplo, os pontos por acerto), rode os testes: eles devem falhar até serem atualizados junto com a mudança.
- Ao adicionar cartões em `data/cartoes.json`, rode os testes para conferir se o arquivo continua válido.
