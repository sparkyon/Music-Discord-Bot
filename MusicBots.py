import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os

TOKEN = 'Your Token'
BOT_PREFIX = '/'

bot = commands.Bot(command_prefix=BOT_PREFIX)

@bot.event
async def on_ready():
    print("Eingeloggt als: " + bot.user.name + "\n")


@bot.command(pass_context=True, aliases=['j', 'joi'])
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"Der Bot ist in den Channel {channel} gejoint\n")

    await ctx.send(f"Joined {channel}")


@bot.command(pass_context=True, aliases=['l', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"Der Bot ist aus dem Channel {channel} geleaved")
        await ctx.send(f"Left {channel}")
    else:
        print("Error")
        await ctx.send("Error")


@bot.command(pass_context=True, aliases=['p', 'pla'])
async def play(ctx, url: str):

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print("Removed old song file")
    except PermissionError:
        print("Error")
        await ctx.send("ERROR: Music playing")
        return

    await ctx.send("Lädt")

    voice = get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloaded die Audio jetzt\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("Song fertig!"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit("-", 2)
    await ctx.send(f"Spielt: {nname[0]}")
    print("spielt\n")


@bot.command(pass_context=True, aliases=['pa', 'pau'])
async def pause(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Musik ist pausiert")
        voice.pause()
        await ctx.send("Musik ist pausiert")
    else:
        print("Error")
        await ctx.send("Error")


@bot.command(pass_context=True, aliases=['r', 'res'])
async def resume(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print("Musik wird gespielt")
        voice.resume()
        await ctx.send("Musik wird gespielt")
    else:
        print("Musik ist nicht pausiert")
        await ctx.send("Musik ist nicht pausiert")


@bot.command(pass_context=True, aliases=['s', 'sto'])
async def stop(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Musik gestoppt")
        voice.stop()
        await ctx.send("Musik gestoppt")
    else:
        print("Error")
        await ctx.send("Error")




bot.run(TOKEN)
