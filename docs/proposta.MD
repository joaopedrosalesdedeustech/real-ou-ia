# Proposta Inicial do Jogo

## 1. Nome provisório do jogo

**Nome:**

> Real ou IA?

## 2. Integrantes do grupo

- Nome 1: João Pedro Sales de Deus
- Nome 2: Aiandra de Sousa Silva
- Nome 3: Victhor Gabriel Freire de Oliveira

## 3. Tema escolhido

**Tema:**

> Confiabilidade de sistemas inteligentes e análise crítica de informações: respostas imprecisas de IA, conteúdos duvidosos ou gerados artificialmente e a importância de conferir antes de confiar.

**Como esse tema se relaciona com o jogo?**

> O tema está na regra principal do jogo. O jogador precisa decidir se cada informação apresentada (resposta de um assistente de IA, publicação de rede social ou notícia) é confiável ou suspeita. Aceitar uma informação falsa faz o jogador perder uma vida, e pedir uma verificação revela uma pista, mas custa pontos. Assim, o jogo mostra que conferir informações tem um custo, mas ajuda a decidir melhor.

## 4. Tipo de jogo

**Tipo escolhido:**

> Perguntas e respostas (quiz de "confiável ou suspeito"), com resposta digitada pelo jogador.

## 5. Descrição geral do jogo

**Descrição:**

> A tela mostra um "cartão" por vez, com um texto curto, por exemplo: *"Assistente de IA: a Muralha da China é visível a olho nu do espaço."* Abaixo do cartão há uma caixa de texto, onde o jogador digita um comando e aperta Enter: `confiavel`, `suspeito` ou `verificar`. Se escolher `verificar`, o jogo mostra uma pista sobre o cartão (por exemplo, "não cita fonte" ou "promete cura milagrosa") e desconta 1 ponto. Depois o jogador ainda precisa responder `confiavel` ou `suspeito`. O jogo informa se a resposta estava certa e passa para o próximo cartão. A tela também mostra pontos, vidas e o número do cartão atual (por exemplo, 4 de 15).

## 6. Objetivo do jogador

**Objetivo:**

> Classificar corretamente os 15 cartões da partida, conservando pelo menos uma vida e fazendo a maior pontuação possível, decidindo quando vale a pena gastar pontos para verificar uma informação.

## 7. Regras principais

- Regra 1: O jogador começa com 3 vidas e 0 pontos.
- Regra 2: Cada resposta correta (`confiavel` ou `suspeito`) soma 10 pontos.
- Regra 3: Cada resposta errada retira 1 vida.
- Regra 4: O comando `verificar` mostra a pista do cartão e retira 1 ponto (uma vez por cartão).
- Regra 5: Comandos inválidos (ex.: `talvez`) exibem "comando inválido" e não alteram pontos nem vidas.

## 8. Condição de vitória

**Condição de vitória:**

> O jogador vence ao responder todos os 15 cartões ainda com pelo menos 1 vida. Ao final, a pontuação é comparada com o recorde salvo.

## 9. Condição de derrota ou encerramento

**Condição de derrota ou encerramento:**

> O jogador perde quando as 3 vidas acabam. A partida também pode ser encerrada a qualquer momento com a tecla ESC.

## 10. Elementos previstos no jogo

- **Personagem ou elemento principal:** a caixa de texto de comando do jogador (o que ele digita controla o jogo) e o cartão exibido.
- **Obstáculos ou desafios:** os cartões com informações falsas disfarçadas de confiáveis, e o custo de verificar.
- **Itens ou objetos de interação (se houver):** as pistas reveladas pelo comando `verificar`.
- **Pontuação, vidas, tempo ou progresso:** pontuação, 3 vidas, contador de cartões (ex.: 4/15) e recorde.

## 11. Controles previstos

**Controles:**

> Teclado. O jogador digita `confiavel`, `suspeito` ou `verificar`; `Enter` envia o comando; `Backspace` apaga a última letra; `ESC` encerra o jogo. O programa ignora maiúsculas, espaços extras e acentos (aceita `confiável` e `confiavel`).

## 12. Principais dificuldades esperadas

- Dificuldade 1: Capturar texto digitado no Pygame, que não tem `input()` (será preciso montar o texto letra por letra com eventos de teclado, incluindo acentos).
- Dificuldade 2: Escrever cartões e pistas claros e equilibrados, sem que a resposta seja óbvia demais ou ambígua.
- Dificuldade 3: Trabalhar em grupo no GitHub (conflitos e organização) e testar a lógica separada da interface.

## 13. Escopo mínimo para a entrega final

**Escopo mínimo:**

> Uma janela do Pygame com uma única tela de jogo, que carrega 15 cartões de um arquivo `.json`, lê os comandos digitados, aplica as regras de pontos e vidas, mostra as pistas, termina em vitória ou derrota, salva o recorde em arquivo e tem README, proposta e testes das funções de lógica.

## 14. Possíveis melhorias, caso haja tempo

- Melhoria 1: Menu inicial e tela de instruções.
- Melhoria 2: Cartões sorteados em ordem aleatória a cada partida e níveis de dificuldade (pistas mais sutis).
- Melhoria 3: Ranking com os melhores resultados (usando `data/ranking.txt`) e efeitos sonoros.

## 15. Estruturas de dados previstas

- **Lista de dicionários:** os cartões, cada um com `texto`, `confiavel` (booleano) e `pista`.
- **Dicionário de estado do jogo:** `pontos`, `vidas`, `indice_cartao`, `pista_visivel` e `texto_digitado`.
- **Conjunto (ou tupla) de comandos válidos:** `confiavel`, `suspeito` e `verificar`.
- **Strings:** tratamento do texto digitado (`strip`, `lower` e remoção de acentos).

## 16. Uso de arquivos

- `data/cartoes.json`: leitura dos cartões do jogo (texto, gabarito e pista).
- `data/recorde.txt`: leitura e gravação da maior pontuação (já previsto no template, em `src/dados.py`).

## 17. Testes planejados

Testes com `pytest` em `tests/test_logica.py`, sem abrir a janela do jogo:

- `interpretar_comando`: aceita `Confiável`, `  SUSPEITO ` e `verificar`; retorna `None` para `talvez` e texto vazio.
- `checar_resposta`: acerto e erro para cartões confiáveis e suspeitos.
- `calcular_pontos`: soma de +10 por acerto e desconto de 1 ponto por verificação.
- `tomar_dano` e `jogador_perdeu`: perda de vidas e derrota com 0 vidas.
- `carregar_recorde` e `salvar_recorde`: arquivo inexistente, vazio e com valor.
- `carregar_cartoes`: lista de cartões com os campos obrigatórios.

## 18. Organização inicial do código

O projeto parte do template da disciplina, mantendo sua estrutura de pastas:

| Arquivo | Responsabilidade |
|---|---|
| `main.py` | Ponto de entrada |
| `src/jogo.py` | Loop principal, eventos de teclado, atualização e desenho da tela |
| `src/funcoes.py` | Regras do jogo: `interpretar_comando`, `checar_resposta`, `calcular_pontos`, `tomar_dano`, `jogador_perdeu` |
| `src/dados.py` | Leitura dos cartões e leitura/gravação do recorde |
| `src/config.py` | Constantes: tela, cores, caminhos dos arquivos, número de vidas e de cartões |
| `data/` | `cartoes.json` e `recorde.txt` |
| `tests/test_logica.py` | Testes das funções de lógica |
| `docs/` | Esta proposta |

O jogo usará apenas texto e retângulos, então `src/sprites.py` e a spritesheet do template não serão utilizados.