import os, requests, asyncio
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TOKEN = os.environ["TELEGRAM_TOKEN"]

def scrape_reddit(url):
    api = url.rstrip("/") + ".json?limit=500"
    r = requests.get(api, headers={"User-Agent": "Mozilla/5.0"})
    data = r.json()
    post = data[0]["data"]["children"][0]["data"]
    title = post["title"]
    body = post.get("selftext", "")
    comments = data[1]["data"]["children"]
    texts = [f"TÍTULO: {title}\n{body}\n\n--- COMENTARIOS ---"]
    for c in comments:
        if c["kind"] == "t1":
            texts.append(f"[{c['data']['score']}] {c['data']['body']}")
    return "\n\n".join(texts)[:4000]

def scrape_generic(url):
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")
    for tag in soup(["script","style","nav","header","footer"]):
        tag.decompose()
    text = soup.get_text(separator="\n", strip=True)
    lines = [l for l in text.splitlines() if len(l) > 40]
    return "\n".join(lines)[:4000]

async def handle(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if not url.startswith("http"):
        await update.message.reply_text("Mándame una URL de Reddit, Forocoches o Rankia.")
        return
    await update.message.reply_text("Extrayendo texto...")
    try:
        if
