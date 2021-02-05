import discord
import d20
from typing import Optional, Callable
from functools import wraps

from config import token


DISCORD_FORMAL_REQUEST_CONTENT_LIMIT = 2000
PREFIX = '!'
DISPATCHED = dict()


app = discord.Client()

def dispatched(cmd:str, f: Callable) -> Callable:
    
    @wraps(f)
    def wrapper(*args, **kwargs) -> Optional[str]:
        return f(args, **kwargs)

    DISPATCHED.update({cmd : wrapper})
    return wrapper


# Return Pong if pinged, simple example for dispatching
dispatched("ping", lambda *_: "Pong!")


def dice_roll_string(author, roll) -> str:
    string = f"{author.mention}: {roll}"

    if len(string) > DISCORD_FORMAL_REQUEST_CONTENT_LIMIT:
        return f"{author.mention}: **way result too long.** {roll.total}"
    else:
        return string


def dispatch_command(cmd, *args, msg) -> Optional[str]:
    return DISPATCHED.get(cmd)(*args, msg)


@app.event
async def on_ready():
    print(f"Bot is up as {app.user}!")
    await app.change_presence(status=discord.Status.online, activity=discord.Game("Dungeons and Dragons"), afk=False)


@app.event 
async def on_message(msg: discord.message.Message):
    text:str = msg.content.strip()

    roll = None
    command_args = []

    if text.startswith(PREFIX):
        command_args = text[len(PREFIX):].split(' ')
        # Slice first, everything else is args, if no args then None
        cmd, args = command_args[0] if command_args[0:1] else None, command_args[1:] or None
        response: str = dispatch_command(cmd, args, msg=msg)
        if response is None:
            return
        else:
            await msg.channel.send(response)

    try:
        roll = d20.roll(text)
    except:
        pass

    if roll: 
        await msg.channel.send(dice_roll_string(msg.author, roll))

if __name__ == '__main__':
    app.run(token)