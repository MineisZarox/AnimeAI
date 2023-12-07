import contextlib
import os
import json
from telethon import events, Button
from somnium import Somnium as Som
from somnium.sync import Somnium
from .. import aai, Vars
from PIL import Image
from ..utilities.maincl import Animade
from itertools import islice            


@aai.on(events.NewMessage(incoming=True, pattern=f"/(qq|generate)(3d)?({Vars.BOT_USERNAME})?"))
@aai.on(events.NewMessage(incoming=True, func=lambda e: bool(e.is_private and e.media)))
async def main(event):
    reply = await event.get_reply_message()
    message = await event.reply("Processing... ✨")
    if event.text and not reply:
        return await message.edit("`Reply to an image...`")
    elif reply:
        if not reply.media:
            return await message.edit("`Reply to an image...`")
    if reply and reply.media and event.text:
        img = await reply.download_media()
        mode = event.pattern_match.group(2) or "qq"
    else:
        img = await event.download_media()
        mode = "qq"
    if not img.endswith((".jpg", ".jpeg", ".png", ".webp")):
        with contextlib.suppress(Exception):
            os.remove(img)
        return await message.edit("`Invalid image file provided...`")
    animeai = Animade(mode)
    result = None
    retires = 5
    while retires >= 0:
        retires -= 1
        try:
            result = await animeai.process(message, img)
            break
        except Exception as e:
            print(e)
            with contextlib.suppress(Exception):
                await message.edit("`Something unexpected happened. Retrying... `✨\n\nYou can try out another mode. Use /qq3d by replying to image.", buttons=[Button.url("Support", url="https://t.me/execalchat")])
            if retires<0:
                await message.edit("`Something unexpected happened. Resend Image`", buttons=[Button.url("Support", url="https://t.me/execalchat")])
    if result:
        await event.reply(file=result)
        await message.delete()
    with contextlib.suppress(Exception):
        os.remove(img)
        [os.remove(out) for out in result]
    
