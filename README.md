# Real ou IA?

Jogo educativo em Python e Pygame sobre **confiabilidade de informações** e **uso responsável da Inteligência Artificial no cotidiano**.

> Projeto final da disciplina **Jogos para o Futuro** (Introdução a Algoritmos), desenvolvido a partir do template oficial da disciplina.

**Status:** em desenvolvimento. A versão atual (Entrega 2) já é jogável do início ao fim: 15 cartões, pontos, vidas, pistas, vitória/derrota e recorde salvo em arquivo.

---

## Integrantes

| Nome | Responsabilidade principal |
|---|---|
| João Pedro Sales de Deus | Lógica do jogo |
| João Pedro Sales de Deus | Interface em Pygame |
| Aiandra de Sousa Silva | Cartões e arquivo de recorde |
| Victhor Gabriel Freire de Oliveira | Testes e documentação |

---

## Sobre o jogo

Vivemos cercados de textos, notícias, imagens e respostas geradas por pessoas e por sistemas de IA. Nem tudo o que lemos é confiável, e conferir uma informação dá trabalho. **Real ou IA?** coloca o jogador diante dessa decisão.

A cada rodada aparece um **cartão** (uma frase, notícia ou mensagem curta). O jogador precisa decidir se a informação é **confiável** ou **suspeita**. Se estiver em dúvida, pode **verificar** o cartão e receber uma pista, mas isso tem um custo em pontos.

### Tema e uso responsável

O recorte escolhido dentro do tema *IA no Cotidiano: Aplicações e Uso Responsável* é a **confiabilidade e a análise crítica de resultados**. O tema está dentro da regra principal do jogo:

- **Confiar sem checar é arriscado:** aceitar uma informação falsa faz o jogador perder uma vida.
- **Verificar tem custo:** pedir uma pista desconta pontos, o que mostra que conferir informações dá trabalho, mas ajuda a decidir melhor.
- **Há hábitos que ajudam a reconhecer informações duvidosas:** procurar a fonte original, conferir data e contexto, comparar com outras fontes, desconfiar de imagens, áudios e respostas de IA que parecem convincentes e não tratar compartilhamentos ou boa aparência como prova. As pistas e as explicações de cada cartão ensinam esses hábitos.

Nenhuma IA real é usada. As classificações são simuladas com listas, dicionários e condicionais.

---

## Como jogar

1. Um cartão aparece na tela, por exemplo: *"Se um texto está bem escrito e não apresenta erros de português, suas informações são verdadeiras."*
2. Na caixa de texto, o jogador **digita** um dos comandos e aperta **Enter**:

| Comando | O que faz |
|---|---|
| `confiavel` (ou `confiável`) | Marca a informação como confiável |
| `suspeito` | Marca a informação como suspeita |
| `verificar` | Mostra uma pista sobre o cartão (custa 1 ponto) |

3. Depois de verificar, o jogador ainda precisa responder `confiavel` ou `suspeito`.
4. O jogo informa se acertou ou errou e mostra uma explicação do cartão. O jogador aperta **Enter** para passar para o próximo cartão.
5. Comandos inválidos (ex.: `talvez`) mostram a mensagem "comando inválido" e **não** fazem o jogador perder nada.

**Teclas auxiliares:** `Backspace` apaga a última letra digitada, `Enter` envia o comando (e avança para o próximo cartão depois de uma resposta) e `ESC` fecha o jogo a qualquer momento.

Ao final da partida aparece a tela de resultado (vitória ou derrota, pontuação e recorde). Nela, `Enter` começa uma nova partida.

---

## Regras

- O jogador começa com **3 vidas** e **0 pontos**.
- **Resposta certa:** +10 pontos.
- **Resposta errada:** perde 1 vida.
- **Verificar um cartão:** −1 ponto (só cobra uma vez por cartão, e os pontos nunca ficam abaixo de zero).
- Cada partida tem **15 cartões**.

### Fim de jogo

- **Derrota:** as 3 vidas acabaram.
- **Vitória:** o jogador respondeu os 15 cartões ainda com vidas.
- Ao final, a pontuação é exibida e comparada com o **recorde**, que fica salvo em arquivo.

---

## Estrutura do projeto

O projeto segue a estrutura do template da disciplina:

```
.
├── main.py              # Ponto de entrada do jogo
├── requirements.txt     # Dependências (pygame, pytest)
├── README.md            # Este arquivo
├── assets/              # Recursos visuais do template (o jogo usa só texto e retângulos)
├── data/
│   ├── cartoes.json     # Cartões do jogo (texto, gabarito e pista)
│   ├── recorde.txt      # Maior pontuação registrada
│   └── ranking.txt      # Arquivo do template (não usado pelo jogo)
├── docs/
│   ├── README.md        # Decisões e mudanças de escopo do projeto
│   └── proposta.MD      # Proposta do grupo
├── src/
│   ├── config.py        # Constantes: tela, cores e regras (vidas, pontos)
│   ├── funcoes.py       # Regras: interpretar comando, checar resposta, pontos, vidas
│   ├── dados.py         # Leitura dos cartões e leitura/gravação do recorde
│   ├── jogo.py          # Loop principal, teclado e desenho da tela
│   └── sprites.py       # Arquivo do template (não usado pelo jogo)
└── tests/
    ├── test_logica.py   # Testes das funções de lógica
    ├── test_dados.py    # Testes de leitura de cartões e do recorde
    └── test_jogo.py     # Testes da interface e partidas completas simuladas
```

### Formato de um cartão

Cada cartão é um dicionário guardado em `data/cartoes.json`:

```json
{
  "texto": "Se um texto está bem escrito e não apresenta erros de português, suas informações são verdadeiras.",
  "confiavel": false,
  "pista": "A qualidade da escrita não demonstra a qualidade das evidências."
}
```

### Principais funções

| Função | Arquivo | O que faz |
|---|---|---|
| `carregar_cartoes()` | `src/dados.py` | Lê e valida os cartões de `data/cartoes.json` |
| `interpretar_comando(texto)` | `src/funcoes.py` | Converte o texto digitado em `confiavel`, `suspeito`, `verificar` ou `None` |
| `checar_resposta(cartao, resposta)` | `src/funcoes.py` | Verifica se o jogador acertou |
| `calcular_pontos(pontos_atual, pontos_ganhos)` | `src/funcoes.py` | Atualiza a pontuação (+10 por acerto, −1 por verificação) |
| `tomar_dano(vida_atual, dano)` | `src/funcoes.py` | Retira vida em caso de erro |
| `jogador_perdeu(vidas)` | `src/funcoes.py` | Indica derrota quando as vidas acabam |
| `carregar_recorde()` | `src/dados.py` | Lê o recorde de `data/recorde.txt` (0 se não existir) |
| `salvar_recorde(pontuacao)` | `src/dados.py` | Grava a pontuação só se superar o recorde e devolve o maior valor |
| `criar_estado()` | `src/funcoes.py` | Cria o estado inicial da partida (pontos, vidas, cartão atual) |
| `processar_comando(estado, cartao, comando, total)` | `src/funcoes.py` | Aplica um comando do jogador: acerto, erro, verificação ou comando inválido; define vitória ou derrota |
| `avancar_cartao(estado)` | `src/funcoes.py` | Passa para o próximo cartão |
| `e_novo_recorde(pontos, recorde)` | `src/funcoes.py` | Indica se a pontuação superou o recorde |
| `quebrar_texto(texto, largura_max, medir_largura)` | `src/funcoes.py` | Divide um texto em linhas para caber no cartão |
| `desenhar_tela_jogo(...)` / `desenhar_tela_fim(...)` | `src/jogo.py` | Desenham a tela do jogo e a tela de resultado final |
| `executar_jogo()` | `src/jogo.py` | Loop principal: teclado, regras e desenho |

---

## Como executar

**Requisitos:** Python 3.10 ou superior.

```bash
# 1. Clonar o repositório
git clone https://github.com/joaopedrosalesdedeustech/real-ou-ia
cd real-ou-ia

# 2. Instalar as dependências
pip install -r requirements.txt

# 3. Iniciar o jogo
python main.py
```

## Como rodar os testes

```bash
python -m pytest
```

Os testes cobrem a lógica do jogo, a leitura dos arquivos e a interface (incluindo partidas completas simuladas, sem abrir janela). Veja `tests/README.md` para mais detalhes.

---

## Conceitos da disciplina utilizados

| Conceito | Onde aparece |
|---|---|
| **Variáveis e tipos de dados** | Pontos, vidas, índice do cartão e texto digitado (`src/funcoes.py`, `src/jogo.py`) |
| **Entrada e saída de dados** | Texto digitado pelo jogador na janela; informações, mensagens e pistas exibidas na tela |
| **Condicionais** | Decisão entre acerto, erro, verificação e comando inválido (`processar_comando`) |
| **Laços** | Loop principal do jogo (`executar_jogo`), validação dos cartões e quebra do texto em linhas |
| **Listas** | Lista de cartões carregada do arquivo; lista de linhas de texto de cada cartão |
| **Dicionários** | Cada cartão (`texto`, `confiavel`, `pista`) e o estado da partida (`criar_estado`) |
| **Tuplas e conjuntos** | Tupla de comandos válidos (`COMANDOS_VALIDOS`), cores em RGB e conjunto de campos obrigatórios do cartão (`src/dados.py`) |
| **Funções e modularização** | Código separado em `config.py`, `funcoes.py`, `dados.py` e `jogo.py`, com funções pequenas e documentadas |
| **Arquivos** | Leitura dos cartões (`.json`) e leitura/gravação do recorde (`.txt`) |
| **Tratamento de erros** | Recorde e cartões inválidos ou ausentes não travam o jogo |
| **Documentação** | Docstrings nas funções, README, proposta e READMEs das pastas |
| **Testes** | Testes automatizados com `pytest` para a lógica, os arquivos e a interface |

---

## Decisões técnicas

- **Lógica separada da interface:** `src/funcoes.py` não depende do Pygame. Isso permite testar todas as regras sem abrir a janela.
- **Estado da partida em um dicionário:** `criar_estado()` guarda pontos, vidas, cartão atual e resultado. As funções recebem e devolvem esse estado, sem variáveis globais.
- **Digitação com eventos de texto:** o Pygame não tem `input()`, então o texto é montado letra por letra com o evento `TEXTINPUT`, o que também permite digitar acentos.
- **Comandos tolerantes:** o texto digitado ignora maiúsculas, espaços extras e acentos (`Confiável`, `confiavel` e `  CONFIAVEL ` valem o mesmo). Comando inválido não tira pontos nem vidas.
- **Explicação depois de cada resposta:** o jogador vê por que o cartão era confiável ou suspeito. O objetivo é que o jogo ensine a checar informações, e não só pontue.
- **Pontos nunca negativos:** pedir pistas com 0 pontos não deixa a pontuação abaixo de zero, e a pista só é cobrada uma vez por cartão.
- **Cartões em arquivo `.json`:** é possível trocar ou acrescentar cartões sem mexer no código. O arquivo é validado ao carregar.
- **Caminhos independentes da pasta de execução:** `src/dados.py` calcula os caminhos a partir do local do próprio arquivo, então o jogo abre mesmo se for executado de outra pasta.
- **Testes sem janela:** as partidas completas são simuladas com eventos de teclado falsos e arquivos temporários, e o `recorde.txt` real nunca é alterado pelos testes.

---

## Recursos externos

- [Python](https://www.python.org/): linguagem do projeto.
- [Pygame](https://www.pygame.org/): biblioteca usada para a janela, o desenho e o teclado.
- [Pytest](https://docs.pytest.org/): biblioteca usada nos testes automatizados. O pacote opcional `pytest-cov` pode ser usado para medir a cobertura.
- [Template da disciplina](https://github.com/ICEI-PUC-Minas-PPL-CDIA/IntroAlgs_pygame_template): estrutura inicial de pastas e arquivos. Os arquivos `src/sprites.py`, `assets/imagens/spritesheet.bmp` e `data/ranking.txt` vieram do template e não são usados no jogo.
- **Fonte:** o jogo usa a fonte Arial instalada no sistema (ou a fonte padrão do Pygame, se a Arial não existir). Nenhum arquivo de fonte, imagem ou som externo foi incluído.
- **Textos dos cartões:** escritos pelo grupo.
- **Ferramentas de IA:** ferramentas de inteligência artificial generativa (Claude, da Anthropic) foram usadas como apoio na elaboração do código, dos testes e da documentação.

---

## Melhorias futuras

- Menu inicial e tela de instruções.
- Cartões em ordem aleatória a cada partida e níveis de dificuldade (pistas mais sutis).
- Ranking com os melhores resultados, usando o `data/ranking.txt` do template.
- Efeitos sonoros.

---

## Declaração de originalidade

Este projeto foi desenvolvido pelos integrantes do grupo para a disciplina, a partir do template oficial. Os recursos externos utilizados, incluindo o apoio de ferramentas de IA, estão referenciados na seção **Recursos externos**.
