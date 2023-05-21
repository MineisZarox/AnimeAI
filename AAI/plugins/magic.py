import contextlib
import os
import json
from telethon import events
from .. import aai, Vars
from ..utilities.maincl import Animade


@aai.on(events.NewMessage(incoming=True, pattern=f"/qq(vid|3d)?({Vars.BOT_USERNAME})?", func=lambda e: bool(e.reply_to)))
@aai.on(events.NewMessage(incoming=True, func=lambda e: bool(e.is_private and e.media)))
async def main(event):
    reply = await event.get_reply_message()
    pros = await event.reply("Processing... ✨")
    if reply and reply.media and event.text:
        img = await reply.download_media()
        mode = event.pattern_match.group(1) or "qq"
    else:
        img = await event.download_media()
        mode = "qq"
    if not img.endswith((".jpg", ".jpeg", ".png", ".webp")):
        return
    animeai = Animade(mode)
    result = await animeai.process(img)
    if mode == "qq3d":
        output = result['media_info_list'][0]['media_data']
    else:
        if result['code'] != 0:
            os.remove(img)
            await pros.delete()
            return await event.reply(f'Error {result["msg"]}')
        output = json.loads(result['extra'])['img_urls'][0]
        output = await animeai.save_crop(output)
    try:
        await event.reply(file=output)
    except Exception:
        os.remove(img)
    os.remove(img)
    await pros.delete()
    with contextlib.suppress(Exception):
        [os.remove(out) for out in output]
    