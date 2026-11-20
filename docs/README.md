# Documentação

Esta pasta concentra os documentos de planejamento e apoio ao projeto **Real ou IA?**.

## Arquivos

- `proposta.MD`: proposta do jogo, com tema, regras, controles, estruturas de dados, arquivos, testes, organização do código, recursos externos e declaração de originalidade. Foi preenchida na Entrega 1 e atualizada para a versão final.

## Decisões do projeto

- O jogo é de perguntas e respostas: o jogador digita `confiavel`, `suspeito` ou `verificar` em uma caixa de texto.
- O tema (confiabilidade e análise crítica de informações) está na regra principal: verificar um cartão custa pontos, e aceitar uma informação falsa custa uma vida.
- O jogo usa só texto e retângulos, então `src/sprites.py` e a spritesheet do template não são utilizados.
- A lógica do jogo (`src/funcoes.py`) não depende do Pygame, o que permite testá-la sem abrir a janela.

## Mudanças de escopo

Mudanças em relação à proposta inicial (Entrega 1):

| Data | Mudança | Motivo |
|---|---|---|
| Entrega 2 | Depois de responder, o jogo mostra uma **explicação** do cartão e espera o jogador apertar Enter para continuar. | O jogador aprende por que a informação era confiável ou suspeita, e não só se acertou. |
| Entrega 2 | Os pontos **nunca ficam negativos**, e a verificação só é cobrada **uma vez por cartão**. | Evitar pontuação negativa e punir pedidos repetidos da mesma pista. |
| Entrega 2 | Os cartões da versão final foram escritos pela Aiandra: afirmações sobre informação e IA, em vez de mensagens de exemplo. | Cartões mais alinhados ao tema de uso responsável. |
| Entrega 2 | O recorde é gravado por `salvar_recorde(pontuacao)`, que só atualiza o arquivo quando a pontuação o supera. | Simplifica o uso no jogo e evita perder um recorde maior. |
| Entrega 3 | Testes ampliados: lógica, arquivos e interface (partidas completas simuladas). | Mais segurança ao alterar o código. |
| Entrega 3 | Cada partida **sorteia 15 cartões** em ordem aleatória (antes, todos os cartões do arquivo apareciam sempre na mesma ordem). | Os cartões originais alternavam confiável e suspeito, o que permitia acertar pelo padrão. Sortear evita isso e torna cada partida diferente. |
| Entrega 3 | Foram acrescentados 5 cartões ao arquivo (20 no total), sem alterar os 15 da Aiandra. Incluem afirmações confiáveis com palavras absolutas e suspeitas com palavras cautelosas, além de privacidade e busca reversa de imagens. | Nos 15 originais, os cartões suspeitos usavam palavras como "sempre" e "prova" e os confiáveis usavam "pode" e "ajuda", o que dava para acertar sem analisar o conteúdo. |
| Entrega 3 | Leitura de `cartoes.json` e `recorde.txt` passou a aceitar arquivos salvos com BOM; erros ao ler ou gravar o recorde não fecham mais o jogo. | Evitar falhas por detalhes de formato de arquivo no Windows e por falta de permissão. |

## Melhorias não implementadas

Ficam como evolução futura: menu inicial e tela de instruções, níveis de dificuldade, ranking com os melhores resultados e efeitos sonoros.
