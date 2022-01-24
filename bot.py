from re import L
import discord
from discord.ext import commands, tasks
from itertools import cycle

import youtube_dl
import os

from fetchKanyeQuote import getKanye
import fetchTrends
import random
import content_db 
from secrets import secret_token
import time

client = commands.Bot(command_prefix="kye, ")
status = cycle(["your mum all night", "you", "your best friend", "your whole family"])

# ideas

# deez nutz
# ask dad joke, reply with dad joke
# expand off search term, using web scraper to get info?
# play youtube clip inside a call
# create a poll

@client.event
async def on_ready():
    change_status.start()
    print('Kye is awake')
    

@tasks.loop(seconds=60)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

@client.command(aliases=['status'])
async def ping(ctx):
    options = ["I am awake", "stfu", "i dont care", "status: absolute weapon", "ERROR ERROR, AAAAAAAAAAAAAGH!"]
    await ctx.send(random.choice(options))

@client.command(aliases=['confused'])
async def info(ctx):
    await ctx.send("*Available Commands:*\n \
        status/ping:  return kye's current status\n \
        greetings/hi/yo:  recieve kye's wisdom\n \
        whatGame?: let kye pick a game to play\n \
        search <WORD>: let kye search the internet for <WORD>\n \
        trending: kye will return the current top 20 trending google searchs\n \
        content/link?: kye will randomly send a URL from a database of hand-picked quality enterntainment \
        voiceHelp: kye will provide more details on available voice channel commands  \
    \nAll Commands must use the prefix <kye, > or kye won't care!")

@client.command(aliases=['yo', 'oi', 'hi', 'hello', 'good morning', 'good afternoon','good evening', 'hey'])
async def greetings(ctx):
    await ctx.send(getKanye())

@client.command()
async def pickTeam(ctx):
    options = ["60P", "muchWarf", "dame Tu Cosita", "garry", "LordBrandon", "realG"]
    random.shuffle(options)
    team1 = options[:3]
    team2 = options[3:]
    await ctx.send(f"{team1} and {team2}")

@client.command(aliases=['query', 'google'])
async def search(ctx, *args, **kwargs):
    local_values = locals().values()
    params = list(list(local_values)[1])
    text = " ".join(params)
    msg = ""
    for i, resp in enumerate(fetchTrends.textSuggestions(text)):
        msg+=f"{i+1}.  {resp['title']} (a {resp['type']})\n"
    if len(msg)<1:
        await ctx.send("no results found")
    else:
        await ctx.send(msg)

@client.command(aliases=['trends', 'hot'])
async def trending(ctx, *args, **kwargs):
    await ctx.send(fetchTrends.trendingSearchs().to_string(header=False))


@client.command(aliases=['pick?', 'game?', 'pick', 'game', 'decide?', "pickGame", "decideGame", "whatGame?"])
async def decide(ctx):
    options = ["apex", "valorant", "halo infinite", "minecraft", "super auto pets", "lol", "no", "i dont want to", "decide for yourself loser", "weak minded and pathetic, just pick one idiot", "oh yeah like you'd listen to what I'd say", "your mum", "deez nuts", "my balls", "its bedtime, go to bed", "i don't care", "stop bothering me"]
    await ctx.send(random.choice(options))

@client.command(aliases=['importantLink', 'link?', 'sendMeSomethingImportant', 'content', 'Content'])
async def importantContent(ctx):
    await ctx.send(random.choice(content_db.options))

@client.command(aliases=['veryGveryN'])
async def veryGoodveryNice(ctx):
    await ctx.send(random.choice(content_db.veryGoodveryNice_files))



# Voice Channel Commands
@client.command()
async def play(ctx, url : str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            # print('song detected')
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return
    
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"))

# Play a specific song
@client.command()
async def very(ctx):
    # # play song
    # song_there = os.path.isfile("vGvN.mp3")
    # try:
    #     if not song_there:
    #         ctx.send("nothing found matchs what you are looking for.")
    # except PermissionError:
    #     await ctx.send("Wait for the current playing music to end or use the 'stop' command")
    #     return

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    
    voice.play(discord.FFmpegPCMAudio("songs/vGvN.mp3"))
    print("voice called")
    time.sleep(10)
    await voice.disconnect()

# Play a specific song
@client.command()
async def peanut(ctx):

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    
    voice.play(discord.FFmpegPCMAudio("songs/nothnButaPeanut.mp3"))
    print("voice called")
    time.sleep(10)
    await voice.disconnect()

# Leave Voice Channel
@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

# Pause Command
@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing")

# Resume Command
@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")

#Stop Command
@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()



client.run(secret_token)