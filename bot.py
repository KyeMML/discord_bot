from dis import dis
import discord
from discord.ext import commands, tasks
from itertools import cycle



client = commands.Bot(command_prefix=".")
status = cycle(["status1", "status2"])


@client.event
async def on_ready():
    change_status.start()
    print('bot is awake')

@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


@client.command(aliases=['yo'])
async def ping(ctx):
    await ctx.send("im awake")


client.run(TOKEN_ID)