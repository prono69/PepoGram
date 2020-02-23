"""test module"""

from pyrogram import Client, Filters


from pyrobot import (
    MAX_MESSAGE_LENGTH,
    COMMAND_HAND_LER,
    LOGGER
)


@Client.on_message(Filters.command("testcmd", COMMAND_HAND_LER)  & Filters.me)
async def _(client, message):
    await message.edit("`test ing ... failed`")
