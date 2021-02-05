import discord
import d20

from config import token


DISCORD_CHARACTER_LIMIT = 2000


app = discord.Client()


def dice_roll_string(author, roll) -> str:
    string = f"{author.mention}: {roll}"

    if len(string) > 2000:
        return f"{author.mention}: result too long. {roll}"
    else:
        return string


@app.event
async def on_ready():
    print(f"Bot is up as {app.user}!")
    await app.change_presence(status=discord.Status.online, activity=discord.Game("Dungeons and Dragons"), afk=False)


@app.event 
async def on_message(msg: discord.message.Message):
    text:str = msg.content.strip()

    roll = None

    try:
        roll = d20.roll(text)
    except:
        pass

    if roll: 
        await msg.channel.send(dice_roll_string(msg.author, roll))


app.run(token)