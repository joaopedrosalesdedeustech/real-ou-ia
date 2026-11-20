# Proposta Inicial do Jogo

> Documento atualizado para a versão final (Entrega 3). As partes que mudaram em relação ao planejamento inicial estão nas seções 5, 7, 15, 17, 18 e 21 e também registradas em `docs/README.md`.

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

> O tema está na regra principal do jogo. O jogador precisa decidir se cada afirmação apresentada (sobre respostas de IA, notícias, imagens e publicações online) é confiável ou suspeita. Aceitar uma informação falsa faz o jogador perder uma vida, e pedir uma verificação revela uma pista, mas custa pontos. Assim, o jogo mostra que conferir informações tem um custo, mas ajuda a decidir melhor.

## 4. Tipo de jogo

**Tipo escolhido:**

> Perguntas e respostas (quiz de "confiável ou suspeito"), com resposta digitada pelo jogador.

## 5. Descrição geral do jogo

**Descrição:**

> A tela mostra um "cartão" por vez, com uma afirmação sobre informação e IA, por exemplo: *"Uma publicação muito compartilhada nas redes sociais já foi confirmada por muitas pessoas."* Abaixo do cartão há uma caixa de texto, onde o jogador digita um comando e aperta Enter: `confiavel`, `suspeito` ou `verificar`. Se escolher `verificar`, o jogo mostra uma pista sobre o cartão e desconta 1 ponto. Depois o jogador ainda precisa responder `confiavel` ou `suspeito`. O jogo informa se a resposta estava certa, mostra uma explicação do cartão e, quando o jogador aperta Enter, passa para o próximo cartão. A tela também mostra pontos, recorde, vidas e o número do cartão atual (por exemplo, 4 de 15). Ao final, uma tela de resultado mostra a pontuação, o recorde e se a partida foi vitória ou derrota.

## 6. Objetivo do jogador

**Objetivo:**

> Classificar corretamente os 15 cartões da partida, conservando pelo menos uma vida e fazendo a maior pontuação possível, decidindo quando vale a pena gastar pontos para verificar uma informação.

## 7. Regras principais

- Regra 1: O jogador começa com 3 vidas e 0 pontos.
- Regra 2: Cada resposta correta (`confiavel` ou `suspeito`) soma 10 pontos.
- Regra 3: Cada resposta errada retira 1 vida.
- Regra 4: O comando `verificar` mostra a pista do cartão e retira 1 ponto (uma vez por cartão; os pontos nunca ficam abaixo de zero).
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

> Uma janela do Pygame com uma única tela de jogo, que carrega os cartões de um arquivo `.json` (e sorteia 15 por partida), lê os comandos digitados, aplica as regras de pontos e vidas, mostra as pistas, termina em vitória ou derrota, salva o recorde em arquivo e tem README, proposta e testes das funções de lógica.

## 14. Possíveis melhorias, caso haja tempo

- Melhoria 1: Menu inicial e tela de instruções.
- Melhoria 2: Cartões sorteados em ordem aleatória a cada partida e níveis de dificuldade (pistas mais sutis).
- Melhoria 3: Ranking com os melhores resultados (usando `data/ranking.txt`) e efeitos sonoros.

*Status na versão final: a ordem aleatória dos cartões (Melhoria 2) foi implementada; os cartões são sorteados a cada partida. Menu inicial, níveis de dificuldade, ranking e sons ficam como evolução futura.*

## 15. Estruturas de dados previstas

- **Lista de dicionários:** os cartões, cada um com `texto`, `confiavel` (booleano) e `pista`.
- **Dicionário de estado da partida** (`criar_estado`): `pontos`, `vidas`, `indice`, `pista_visivel`, `mensagem`, `tipo_mensagem`, `resultado` e `fim`.
- **Tupla de comandos válidos** (`COMANDOS_VALIDOS`): `confiavel`, `suspeito` e `verificar`.
- **Conjunto de campos obrigatórios** de cada cartão, usado na validação do arquivo.
- **Strings:** tratamento do texto digitado (`strip`, `lower` e remoção de acentos).
- **Lista de linhas:** o texto de cada cartão é dividido em linhas para caber na tela.

## 16. Uso de arquivos

- `data/cartoes.json`: leitura dos cartões do jogo (texto, gabarito e pista), com validação dos campos. O arquivo tem 20 cartões e cada partida sorteia 15.
- `data/recorde.txt`: leitura e gravação da maior pontuação (em `src/dados.py`). O recorde só é gravado quando a pontuação da partida o supera.

## 17. Testes implementados

Testes automatizados com `pytest` (mais de 100 testes), sem abrir janela:

- `tests/test_logica.py`: `interpretar_comando` (maiúsculas, acentos, espaços, comando inválido), `checar_resposta`, `calcular_pontos`, `tomar_dano`, `jogador_perdeu`, `processar_comando` (acerto, erro, verificação, vitória e derrota), `avancar_cartao`, `sortear_cartoes`, `e_novo_recorde` e `quebrar_texto`.
- `tests/test_dados.py`: `carregar_recorde` e `salvar_recorde` (arquivo ausente, vazio, inválido, recorde maior e menor) e `carregar_cartoes` (campos obrigatórios, tipos e erros), além de conferir o arquivo real de cartões.
- `tests/test_jogo.py`: desenho das telas e partidas completas simuladas com eventos de teclado falsos (vitória, derrota, comando inválido, Backspace, ESC, jogar novamente e falhas ao carregar os cartões).

Veja `tests/README.md` para mais detalhes.

## 18. Organização do código

O projeto parte do template da disciplina, mantendo sua estrutura de pastas:

| Arquivo | Responsabilidade |
|---|---|
| `main.py` | Ponto de entrada |
| `src/jogo.py` | Loop principal, eventos de teclado e desenho das telas (jogo e resultado final) |
| `src/funcoes.py` | Regras do jogo, sem depender do Pygame: `interpretar_comando`, `checar_resposta`, `processar_comando`, `avancar_cartao`, `sortear_cartoes`, `calcular_pontos`, `tomar_dano`, `jogador_perdeu`, `quebrar_texto` |
| `src/dados.py` | Leitura e validação dos cartões e leitura/gravação do recorde |
| `src/config.py` | Constantes: tela, cores e regras (vidas, pontos, custo da verificação, comandos válidos) |
| `data/` | `cartoes.json` e `recorde.txt` |
| `tests/` | `test_logica.py`, `test_dados.py` e `test_jogo.py` |
| `docs/` | Esta proposta e o registro de decisões |

O jogo usa apenas texto e retângulos, então `src/sprites.py` e a spritesheet do template não são utilizados.

## 19. Recursos externos

- Python, Pygame (janela, desenho e teclado) e Pytest (testes).
- Template oficial da disciplina: https://github.com/ICEI-PUC-Minas-PPL-CDIA/IntroAlgs_pygame_template
- Fonte Arial do sistema (ou a fonte padrão do Pygame). Nenhuma imagem, som ou fonte externa foi incluída.
- Os 15 primeiros cartões foram escritos pela Aiandra; os 5 últimos foram redigidos com apoio de IA.
- Ferramentas de IA generativa (Claude, da Anthropic) foram usadas como apoio na elaboração do código, dos testes e da documentação.

## 20. Declaração de originalidade

Declaramos que a proposta e o jogo foram desenvolvidos pelo grupo a partir do template oficial da disciplina. Os recursos externos utilizados, incluindo o apoio de ferramentas de IA, estão referenciados na seção 19 e no `README.md`.

## 21. Desafios encontrados no desenvolvimento

- **Digitação no Pygame:** como não existe `input()`, o texto é montado letra por letra com o evento `TEXTINPUT`, o que também permite digitar acentos.
- **Integração das partes:** a lógica, a interface, os cartões e o recorde foram feitos por pessoas diferentes, e as funções precisaram ser ajustadas entre si (por exemplo, a interface passou a usar as funções de `src/dados.py` sem receber caminhos).
- **Testar uma interface:** para testar partidas completas sem abrir janela, os testes enviam eventos de teclado falsos ao loop principal e usam arquivos temporários.
- **Cartões bons:** foi preciso escrever afirmações e pistas claras, sem que a resposta fosse óbvia demais.