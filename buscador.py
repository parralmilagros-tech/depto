import os
import requests
from bs4 import BeautifulSoup
import time
from telegram import Bot

# Variables de entorno
TELEGRAM_TOKEN = os.getenv("8371356146:AAGv3E4HUdyYnuEko3J4j2aZqwYqqyZCh34")
CHAT_ID = os.getenv("1700481674")
bot = Bot(token=TELEGRAM_TOKEN)

def buscar_departamentos():
    url = "https://www.zonaprop.com.ar/departamentos-venta-capital-federal-3-ambientes-hasta-110000-dolares.html"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")

    propiedades = soup.find_all("div", class_="posting-card")

    resultados = []
    for prop in propiedades:
        titulo = prop.find("h2").get_text(strip=True) if prop.find("h2") else "Sin título"
        link = "https://www.zonaprop.com.ar" + prop.find("a")["href"]
        precio = prop.find("span", class_="first-price").get_text(strip=True) if prop.find("span", class_="first-price") else "N/D"
        resultados.append((titulo, precio, link))
    return resultados

def notificar_nuevos(resultados, vistos):
    nuevos = [r for r in resultados if r[2] not in vistos]
    for titulo, precio, link in nuevos:
        mensaje = f"🏠 {titulo}\n💲 {precio}\n🔗 {link}"
        bot.send_message(chat_id=CHAT_ID, text=mensaje)
    return vistos.union({r[2] for r in nuevos})

if __name__ == "__main__":
    vistos = set()
    while True:
        resultados = buscar_departamentos()
        vistos = notificar_nuevos(resultados, vistos)
        time.sleep(3600)  # espera 1 hora entre consultas
