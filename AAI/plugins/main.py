import contextlib
import os
import json
from telethon import events, Button
from .. import aai, Vars
from ..utilities.maincl import Animade


@aai.on(events.NewMessage(incoming=True, pattern=f"/qq(3d)?({Vars.BOT_USERNAME})?", func=lambda e: bool(e.reply_to)))
@aai.on(events.NewMessage(incoming=True, func=lambda e: bool(e.is_private and e.media)))
async def main(event):
    reply = await event.get_reply_message()
    message = await event.reply("Processing... ✨")
    if reply and reply.media and event.text:
        img = await reply.download_media()
        mode = event.pattern_match.group(1) or "qq"
    else:
        img = await event.download_media()
        mode = "qq"
    if not img.endswith((".jpg", ".jpeg", ".png", ".webp")):
        return await message.edit("`Invalid image file provided...`")
    animeai = Animade(mode)
    result = await animeai.process(message, img)
    if result:
        await event.reply(file=result)
        await message.delete()
    with contextlib.suppress(Exception):
        os.remove(img)
        [os.remove(out) for out in result]
    