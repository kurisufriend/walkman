import discord
import yt_dlp as youtube_dl
import time
import asyncio

g_client = discord.Client()
queue = []
last_playing = {}
voice_client = None
last_start = 0
@g_client.event
async def on_ready():
    print("ohai")
    while True:
        await asyncio.sleep(.1)
        if len(queue) > 0:
            if not voice_client.is_playing() and voice_client is not None:
                ydl = youtube_dl.YoutubeDL({"simulate": True})
                res = ydl.extract_info(queue[0],
                                       force_generic_extractor=ydl.params.get('force_generic_extractor', False))#lifted the second bit from the ytdl innards
                link = None
                for format in res["requested_formats"]:
                    if not (format["asr"] is None):
                        link = format["url"]
                last_playing = res
                voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(link, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"), volume=1.0))
                print("playan")
                sav = queue[0]
                hack = False
                for sec in range(res["duration"]):# FIX SH1T HACK
                    await asyncio.sleep(1)
                    try:# how do i computer i just press keys please help
                        if not(sav == queue[0]):
                            hack = True
                            break
                    except:
                        hack = True
                        break
                if hack:
                    continue
                #await asyncio.sleep(res["duration"])
                queue.pop(0)
                print("popped")
@g_client.event
async def on_message(message):
    global last_playing
    global voice_client
    global queue
    print(">>>", message.content)
    if message.author == g_client.user:
        return

    if message.content.startswith("*play"):
        try:
             voice_client = await message.author.voice.channel.connect()
        except: #already conn'd/user not in chan/probably something else (?). fails are not /broadly/ (really) destructive neway so who cares#nevermind
            print("AAHHHHHHHHHHHHHHHHHHHH OH GOD")
            pass #it's ok if we do it ON PURPOSE ;^)
        queue.append(message.content.split(" ")[1])
        await message.channel.send("k")

    if message.content.startswith("*lp"):
        embed = discord.Embed(title="now playing...")
        embed.add_field(name="song:", value=last_playing["title"], inline=False)
        embed.set_image(url = last_playing["thumbnail"])
        embed.add_field(name="duration (in seconds):", value=last_playing["duration"], inline=False)
        await message.channel.send(embed=embed)

    if message.content.startswith("*q"):
        embed = discord.Embed(title="queue")
        for q in queue:
            embed.add_field(name="", value=q, inline=False)
        await message.channel.send(embed=embed)

    if message.content.startswith("*s"):
        queue.pop(0)
        voice_client.stop()
conf = open("token", "r")
g_client.run(conf.read(), bot=True)
conf.close()
