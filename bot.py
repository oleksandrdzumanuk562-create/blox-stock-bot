import discord
from discord.ext import commands, tasks
import os
from flask import Flask
from threading import Thread
import requests
from bs4 import BeautifulSoup

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = 1528326358709833858

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


normal_stock = [
    ("🚀 Rocket", "5,000$"),
    ("🌀 Spin", "7,500$"),
    ("🌫️ Smoke", "100,000$"),
    ("🏜️ Sand", "420,000$")
]


mirage_stock = [
    ("🚀 Rocket", "5,000$"),
    ("🌀 Spin", "7,500$"),
    ("💥 Bomb", "80,000$"),
    ("🌫️ Smoke", "100,000$"),
    ("🧘 Buddha", "1,200,000$")
]


def create_normal_stock():
    text = ""

    for fruit, price in normal_stock:
        text += f"{fruit}        -        {price}\n"

    return text


def create_mirage_stock():
    text = ""

    for fruit, price in mirage_stock:
        text += f"{fruit}        -        {price}\n"

    return text


@tasks.loop(hours=4)
async def normal_update():
    channel = bot.get_channel(CHANNEL_ID)

    if channel:
        embed = discord.Embed(
            title="🍎 Current Normal Stock",
            description=create_normal_stock(),
            color=0x00ff00
        )

        embed.set_footer(text="Normal Stock обновляется каждые 4 часа")

        await channel.send(embed=embed)


@tasks.loop(hours=2)
async def mirage_update():
    channel = bot.get_channel(CHANNEL_ID)

    if channel:
        embed = discord.Embed(
            title="🌌 Current Mirage Stock",
            description=create_mirage_stock(),
            color=0x9900ff
        )

        embed.set_footer(text="Mirage Stock обновляется каждые 2 часа")

        await channel.send(embed=embed)


@bot.event
async def on_ready():
    print(f"Бот {bot.user} запущен!")

    if not normal_update.is_running():
        normal_update.start()

    if not mirage_update.is_running():
        mirage_update.start()

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run():
    app.run(host="0.0.0.0", port=10000)

Thread(target=run).start()

bot.run(TOKEN)
