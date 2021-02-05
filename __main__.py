import discord

from config import token


app = discord.Client()


@app.event
async def on_ready():
    print(f"Bot is up as {app.user}!")
    await app.change_presence(status=discord.Status.online, activity=discord.Game("Dungeons and Dragons"), afk=False)


app.run(token)