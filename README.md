# Real ou IA?

Jogo educativo em Python e Pygame sobre **confiabilidade de informações** e **uso responsável da Inteligência Artificial no cotidiano**.

> Projeto final da disciplina **Jogos para o Futuro** (Introdução a Algoritmos), desenvolvido a partir do template oficial da disciplina.

**Status:** em desenvolvimento

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
- **Há sinais para reconhecer informações duvidosas:** ausência de fonte, promessas milagrosas, linguagem exagerada ou genérica. As pistas ensinam a identificá-los.

Nenhuma IA real é usada. As classificações são simuladas com listas, dicionários e condicionais.

---

## Como jogar

1. Um cartão aparece na tela, por exemplo: *"Beber água gelada cura gripe, dizem 'especialistas'."*
2. Na caixa de texto, o jogador **digita** um dos comandos e aperta **Enter**:

| Comando | O que faz |
|---|---|
| `confiavel` (ou `confiável`) | Marca a informação como confiável |
| `suspeito` | Marca a informação como suspeita |
| `verificar` | Mostra uma pista sobre o cartão (custa 1 ponto) |

3. Depois de verificar, o jogador ainda precisa responder `confiavel` ou `suspeito`.
4. O jogo informa se acertou ou errou e passa para o próximo cartão.
5. Comandos inválidos (ex.: `talvez`) mostram a mensagem "comando inválido" e **não** fazem o jogador perder nada.

**Teclas auxiliares:** `Backspace` apaga a última letra digitada e `Enter` envia o comando.

---

## Regras

- O jogador começa com **3 vidas** e **0 pontos**.
- **Resposta certa:** +10 pontos.
- **Resposta errada:** perde 1 vida.
- **Verificar um cartão:** −1 ponto.
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
├── assets/              # Recursos visuais (o jogo usa só texto e retângulos)
├── data/
│   ├── cartoes.json     # Cartões do jogo (texto, gabarito e pista)
│   └── recorde.txt      # Maior pontuação registrada
├── docs/
│   └── proposta.MD      # Proposta inicial do grupo
├── src/
│   ├── config.py        # Constantes: tela, cores, caminhos, vidas
│   ├── funcoes.py       # Regras: interpretar comando, checar resposta, pontos, vidas
│   ├── dados.py         # Leitura dos cartões e leitura/gravação do recorde
│   └── jogo.py          # Loop principal, teclado e desenho da tela
└── tests/
    └── test_logica.py   # Testes das funções de lógica
```

### Formato de um cartão

Cada cartão é um dicionário guardado em `data/cartoes.json`:

```json
{
  "texto": "Beber água gelada cura gripe, dizem 'especialistas'.",
  "confiavel": false,
  "pista": "Não cita nenhuma fonte e promete cura milagrosa."
}
```

### Principais funções

| Função | Arquivo | O que faz |
|---|---|---|
| `carregar_cartoes(caminho)` | `src/dados.py` | Lê os cartões do arquivo `.json` |
| `interpretar_comando(texto)` | `src/funcoes.py` | Converte o texto digitado em `confiavel`, `suspeito`, `verificar` ou `None` |
| `checar_resposta(cartao, resposta)` | `src/funcoes.py` | Verifica se o jogador acertou |
| `calcular_pontos(pontos_atual, pontos_ganhos)` | `src/funcoes.py` | Atualiza a pontuação (+10 por acerto, −1 por verificação) |
| `tomar_dano(vida_atual, dano)` | `src/funcoes.py` | Retira vida em caso de erro |
| `jogador_perdeu(vidas)` | `src/funcoes.py` | Indica derrota quando as vidas acabam |
| `carregar_recorde(caminho)` / `salvar_recorde(caminho, pontuacao)` | `src/dados.py` | Lê e grava o recorde em arquivo |
| `desenhar_tela(...)` | `src/jogo.py` | Mostra cartão, pontos, vidas e caixa de texto |

---

## Como executar

**Requisitos:** Python 3.10 ou superior.

```bash
# 1. Clonar o repositório
git clone LINK_DO_REPOSITORIO
cd NOME_DA_PASTA

# 2. Instalar as dependências
pip install -r requirements.txt

# 3. Iniciar o jogo
python main.py
```

## Como rodar os testes

```bash
python -m pytest
```

---

## Recursos externos

- [Pygame](https://www.pygame.org/): biblioteca de jogos em Python.
- [Pytest](https://docs.pytest.org/): biblioteca de testes.
- [Template da disciplina](https://github.com/ICEI-PUC-Minas-PPL-CDIA/IntroAlgs_pygame_template): estrutura inicial do projeto.

---

## Declaração de originalidade

Este projeto foi desenvolvido pelos integrantes do grupo para a disciplina, a partir do template oficial. Os recursos externos utilizados estão referenciados acima.