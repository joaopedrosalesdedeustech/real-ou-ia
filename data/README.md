# Dados

Esta pasta guarda os arquivos de dados do jogo.

## Arquivos

- `cartoes.json`: os cartões do jogo. É uma lista em que cada item tem `texto` (afirmação mostrada ao jogador), `confiavel` (`true` ou `false`, o gabarito) e `pista` (usada na verificação e na explicação depois da resposta). O arquivo é validado ao carregar.
- `recorde.txt`: a maior pontuação registrada, escrita como um número inteiro. Se o arquivo não existir ou estiver vazio, o recorde é 0.
- `ranking.txt`: arquivo do template, não usado por este jogo.

## Exemplo de cartão

```json
{
  "texto": "Se um texto está bem escrito e não apresenta erros de português, suas informações são verdadeiras.",
  "confiavel": false,
  "pista": "A qualidade da escrita não demonstra a qualidade das evidências."
}
```

## Como adicionar cartões

Acrescente novos itens na lista de `cartoes.json`, mantendo textos e pistas curtos (até cerca de 150 caracteres) para caberem na tela. Depois rode `python -m pytest` para conferir se o arquivo continua válido. Atenção: o jogo mostra todos os cartões do arquivo em cada partida e a condição de vitória é responder todos eles.

## Observação

Evite versionar dados pessoais reais dos jogadores.
