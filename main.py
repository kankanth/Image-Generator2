import os
import discord
import requests

from myserver import server_on

TOKEN =  os.getenv("DISCORD_BOT_TOKEN")
HF_TOKEN = os.getenv("HF_API_TOKEN")


API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    if message.content.startswith("!img "):
        prompt = message.content[5:]
        await message.channel.send("กำลังสร้างภาพ...")

        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})

        if response.status_code == 200:
            with open("output.png", "wb") as f:
                f.write(response.content)
            await message.channel.send(file=discord.File("output.png"))
        else:
            await message.channel.send(response.text)

server_on()

client.run(TOKEN)