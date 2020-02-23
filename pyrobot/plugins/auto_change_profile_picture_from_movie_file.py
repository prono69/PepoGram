from pyrogram import Client, Filters

import asyncio
import os
import sys
import traceback
import time
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import (
    Image,
    ImageDraw,
    ImageFont
)

from pyrobot import (
    MAX_MESSAGE_LENGTH,
    COMMAND_HAND_LER,
    TMP_DOWNLOAD_DIRECTORY
)

SLEEP_DELAY = 49
START_TIME = os.environ.get("MOVIE_L_START_TIME", None)
MOVIE_IS_RUNNING = False


@Client.on_message(Filters.command("stopmoviepp", COMMAND_HAND_LER)  & Filters.me)
async def test_command_one(client, message):
    MOVIE_IS_RUNNING = False
    await message.reply_text("hmm")


@Client.on_message(Filters.command("startmoviepp", COMMAND_HAND_LER)  & Filters.me)
async def test_command_zero(client, message):
    # await message.edit("Processing ...")
    movie_location = " ".join(message.command[1:])
    print(movie_location)
    metadata = extractMetadata(createParser(movie_location))
    duration = 0
    if metadata.has("duration"):
        duration = metadata.get('duration').seconds
    print(duration)
    MOVIE_IS_RUNNING = True
    for current_t_s in list(reversed(range(duration))):
        if not MOVIE_IS_RUNNING:
            await message.reply_text(
                "stopped playing at <code>{}</code>".format(
                    p_t_m_f_te(current_t_s)
                )
            )
            break
        print(current_t_s)
        one_screenshot = await take_screen_shot(
            movie_location,
            TMP_DOWNLOAD_DIRECTORY,
            current_t_s
        )
        print(one_screenshot)
        duration_as_text = p_t_m_f_te(current_t_s)
        s_i_sed_scsht = await super_impose_text_o_img(
            one_screenshot,
            duration_as_text
        )
        # os.remove(one_screenshot)
        print(s_i_sed_scsht)
        await client.set_profile_photo(s_i_sed_scsht)
        os.remove(s_i_sed_scsht)
        await asyncio.sleep(SLEEP_DELAY)


async def take_screen_shot(video_file, output_directory, ttl):
    # https://stackoverflow.com/a/13891070/4723940
    out_put_file_name = os.path.join(
        output_directory,
        str(time.time()) + ".jpg"
    )
    #
    file_genertor_command = [
        "ffmpeg",
        "-ss",
        str(ttl),
        "-i",
        video_file,
        "-vframes",
        "1",
        out_put_file_name
    ]
    # width = "90"
    process = await asyncio.create_subprocess_exec(
        *file_genertor_command,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    #
    if os.path.lexists(out_put_file_name):
        return out_put_file_name
    else:
        return None


def p_t_m_f_te(duration):
    dict_tme = convert_to_HH_MM_SS(duration)
    return "{} : {} : {}".format(
        dict_tme.get("H"),
        dict_tme.get("M"),
        dict_tme.get("S")
    )


def convert_to_HH_MM_SS(duration):
    seconds_p = duration % 60
    duration = duration // 60
    minutes_p = duration % 60
    duration = duration // 60
    hours_p = duration % 60
    return {
        "H": c_1_t_2_d(hours_p),
        "M": c_1_t_2_d(minutes_p),
        "S": c_1_t_2_d(seconds_p)
    }


def c_1_t_2_d(number):
    return "{0:0=2d}".format(number)


async def super_impose_text_o_img(img_path, text):
    # create Image object with the input image
    image = Image.open(img_path)
    w, h = image.size
    # initialise the drawing context with
    # the image object as background
    draw = ImageDraw.Draw(image)
    # create font object with the font file and specify
    # desired size
    font_location = os.path.join(
        TMP_DOWNLOAD_DIRECTORY,
        "Manjari-Bold.ttf"
    )
    font = ImageFont.truetype(
        font_location,
        size=45
    )
    # calculation for the offset
    text_w, text_h = draw.textsize(text, font)
    # starting position of the message
    (x, y) = ((w - text_w) // 2, h - text_h)
    color = "rgb(255, 255, 255)" # white color
    draw.text((x, y), text, fill=color, font=font)
    # save the edited image
    image.save(img_path)
    return img_path
