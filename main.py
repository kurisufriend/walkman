import discord
import yt_dlp as youtube_dl
import time
import asyncio
import requests
import json
import sys
import random

g_client = discord.Client(intents=discord.Intents.all())
queue = []
voice_client = None

async def q_vid(url):
    global voice_client
    global queue
    ydl = youtube_dl.YoutubeDL({"simulate": True})
    res = ydl.extract_info(url, force_generic_extractor=ydl.params.get('force_generic_extractor', False))

    link = None
    for format in res["requested_formats"]:
        print(format)
        if not (format.get("url") is None):
            link = format["url"]
    if not link: return

    queue.append({"link": link, "ctx": res})

@g_client.event
async def on_ready():
    print("ohai")
    while True:
        await asyncio.sleep(.1)
        if len(queue) > 0:
            if (voice_client is not None) and (not voice_client.is_playing()):
                voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(queue[0]["link"], before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"), volume=1.0))
                print("playan")
                sav = queue[0]["link"]
                hack = False
                for sec in range(queue[0]["ctx"]["duration"]):# FIX SH1T HACK
                    await asyncio.sleep(1)
                    try:# how do i computer i just press keys please help
                        if not(sav == queue[0]["link"]):
                            hack = True
                            break
                    except:
                        hack = True
                        break
                if hack:
                    continue
                queue.pop(0)
                print("popped")
@g_client.event
async def on_message(message):
    global voice_client
    global queue
    print(">>>", message.author.display_name, message.content)
    if message.author == g_client.user:
        return

#    if message.content.startswith("*") and message.author.id == 376713633641660426 and random.randint(0, 4) == 3:
#        await message.channel.send("nice try gayboy! roll again.")
#        return

    if message.content.startswith("*play"):
        print("1")
        try:
            print("2", message.author.voice.channel, discord.__version__)
            voice_client = await message.author.voice.channel.connect()
            print("shiggy", voice_client)
        except Exception as e: print("passed on the oppo of a lifetime xister", e)
        print("3")
        await q_vid(message.content.split(" ")[1])

        await message.channel.send("k")
    if message.content.startswith("*np"):
        embed = discord.Embed(title="now playan~", url=queue[0]["ctx"]["webpage_url"])
        embed.set_thumbnail(url=queue[0]["ctx"]["thumbnail"])
        embed.add_field(name="naem:", value=queue[0]["ctx"]["title"], inline=True)
        embed.add_field(name="uploadah:", value=queue[0]["ctx"]["uploader"], inline=True)
        embed.add_field(name="viewz:", value=queue[0]["ctx"]["view_count"], inline=True)
        embed.add_field(name="length:", value=str(queue[0]["ctx"]["duration"]/60)+" minutes", inline=True)
        await message.channel.send(embed=embed)

    if message.content.startswith("*q"):
        embed = discord.Embed(title="queue")
        for q in queue:
            embed.add_field(name="song:", value=q["ctx"]["title"], inline=False)
        await message.channel.send(embed=embed)

    if message.content.startswith("*s"):
        queue.pop(0)
        voice_client.stop()
    if message.content.startswith(f"*moans* i love sucking your little baby child penis unh i am a pedophile and my name is {message.author.display_name}"):
        await message.channel.send(f" wtf bro thats not cool wtf wtf wtf im leaving wtf i cant believe {message.author.display_name} is a monster i idolized oyu man wtf how could you do this im gone bro")
        print("lol")
        exit(0)

    if message.content.startswith("*b"):
        try: voice_client = await message.author.voice.channel.connect()
        except: pass
        res = json.loads(requests.get(f"https://watch.supernets.org/api/v1/search?q={'%20'.join(message.content.split(' ')[1:])}&pretty=1").text)
        res = [item for item in res if item["type"] == "video"]
        if message.content.split(' ')[0][-1] in list("012345"):
            v = res[int(message.content.split(' ')[0][-1])]
            await q_vid(f"https://www.youtube.com/watch?v={v['videoId']}")
            await message.channel.send(f"k, {v['title']}")
            return
        embed = discord.Embed(title="does this look right")
        for i, q in enumerate(res):
            if i > 5: break
            embed.add_field(name=str(i), value=q["title"], inline=False)
        await message.channel.send(embed=embed)

conf = open("token", "r")
g_client.run(conf.read())
conf.close()
