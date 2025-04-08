# ApostaAIvobot com Banco de Dados (PostgreSQL)

Este bot analisa jogos do Brasileirão com base na estratégia "Empate no 1º tempo + Ambas NÃO" e salva os jogos analisados em um banco de dados PostgreSQL.

## Variáveis de ambiente necessárias:
- `API_FOOTBALL_KEY`
- `TELEGRAM_TOKEN`
- `CHAT_ID`
- `DB_HOST`
- `DB_NAME`
- `DB_USER`
- `DB_PASS`

## Como usar:
1. Suba este repositório para o GitHub.
2. No Railway, conecte um banco de dados PostgreSQL e adicione as variáveis acima.
3. Configure um cron job diário para executar: `python main.py`