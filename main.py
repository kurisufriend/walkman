import discord
import yt_dlp as youtube_dl
import time
import asyncio

g_client = discord.Client()
queue = []
voice_client = None
@g_client.event
async def on_ready():
    print("ohai")
    while True:
        await asyncio.sleep(.1)
        if len(queue) > 0:
            if not voice_client.is_playing() and voice_client is not None:
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
    print(">>>", message.content)
    if message.author == g_client.user:
        return

    if message.content.startswith("*play"):
        try: voice_client = await message.author.voice.channel.connect()
        except: pass
        ydl = youtube_dl.YoutubeDL({"simulate": True})
        res = ydl.extract_info(message.content.split(" ")[1], force_generic_extractor=ydl.params.get('force_generic_extractor', False))

        link = None
        for format in res["requested_formats"]:
            if not (format["asr"] is None):
                link = format["url"]
        if not link: return

        queue.append({"link": link, "ctx": res})
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
conf = open("token", "r")
g_client.run(conf.read(), bot=True)
conf.close()