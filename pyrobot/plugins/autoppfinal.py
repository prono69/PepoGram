# -- Auto PP plugin Ported by @W4RR10R -- #
# .autopp - starts auto pp
# .stoppp - stops auto pp

from pyrogram import Client, Filters
import os,asyncio
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from pyrobot import COMMAND_HAND_LER, TMP_DOWNLOAD_DIRECTORY


 
IS_RUNNING = True

@Client.on_message(Filters.command("stoppp",COMMAND_HAND_LER)  & Filters.me)
async def stoppp(client, message):
    await message.edit("`Stopping...`")
    global IS_RUNNING
    IS_RUNNING = False


@Client.on_message(Filters.command("autopp", COMMAND_HAND_LER)  & Filters.me)
async def getpp(client, message):
    await message.edit("`Processing..`")
    setdpp = await client.get_profile_photos("me", limit=1)
    bkpic = "ppmani.png"
    if not os.path.isdir(TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TMP_DOWNLOAD_DIRECTORY)
    currentpp = await client.download_media(
            message=setdpp[0],
            file_name=TMP_DOWNLOAD_DIRECTORY
        )
    await message.edit("`Auto pp is running..`")
    FONT = os.path.join(
        TMP_DOWNLOAD_DIRECTORY,
        "font.ttf"
    )
    if not os.path.isfile(FONT):
        FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    while True:
        if not IS_RUNNING:
            await message.reply_text("`Auto PP have been aborted successfully`")
            break
        c_time = datetime.now().strftime("\n %H:%M:%S \n %d.%m.%y \n")
        img = Image.open(currentpp)
        w, h = img.size
        drawn_text = ImageDraw.Draw(img)
        font = ImageFont.truetype(FONT, 35)
        width,height  = drawn_text.textsize(c_time, font)
        (x, y) = ((w - width) // 2, h - height)
        drawn_text.text((x,y), c_time, font=font, fill=(255, 255, 255))
        img.save(bkpic)
        await client.set_profile_photo(bkpic)
        await asyncio.sleep(50)
        