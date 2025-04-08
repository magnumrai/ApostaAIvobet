import requests
import datetime
import telebot
import time
import psycopg2
import os

API_KEY = os.getenv('API_FOOTBALL_KEY')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def conectar_db():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

def criar_tabela():
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS analises (
            id SERIAL PRIMARY KEY,
            data DATE,
            jogo TEXT,
            enviado BOOLEAN DEFAULT FALSE
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def salvar_analise(data, jogo):
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM analises WHERE data = %s AND jogo = %s", (data, jogo))
    if not cur.fetchone():
        cur.execute("INSERT INTO analises (data, jogo, enviado) VALUES (%s, %s, %s)", (data, jogo, True))
        conn.commit()
    cur.close()
    conn.close()

def buscar_jogos():
    hoje = datetime.datetime.now().strftime('%Y-%m-%d')
    url = f"https://v3.football.api-sports.io/fixtures?date={hoje}&league=71&season=2024"
    headers = {
        "x-apisports-key": API_KEY
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    jogos = []
    for item in data['response']:
        casa = item['teams']['home']['name']
        fora = item['teams']['away']['name']
        jogos.append(f"{casa} x {fora}")
    return jogos

def enviar_mensagem(msg):
    bot.send_message(CHAT_ID, msg)

def analise_diaria():
    hoje = datetime.datetime.now().strftime('%Y-%m-%d')
    jogos = buscar_jogos()
    if not jogos:
        enviar_mensagem("Nenhum jogo encontrado para hoje.")
    else:
        enviar_mensagem("Análise de hoje (Empate 1T + Ambas NÃO):")
        for jogo in jogos:
            enviar_mensagem(f"Possível jogo: {jogo}")
            salvar_analise(hoje, jogo)
            time.sleep(1)

if __name__ == "__main__":
    criar_tabela()
    analise_diaria()