import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_TOKEN")

bot = commands.Bot(command_prefix = "!", intents = discord.Intents.all())

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    for file in message.attachments:
        print(file.filename)
        if file.filename.endswith((".png", ".jpg", ".jpeg", ".gif")):
            await message.channel.send(f"The filename is {file.filename}")

bot.run(token)