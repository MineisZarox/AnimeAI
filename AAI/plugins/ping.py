from telethon import events
from .. import aai, Vars
from aaai.anime import convertai
import random
import sys
import os


@aai.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def start(event):
    user = await aai.get_entity(int(event.sender.id))
    if event.text == "/start":
        await event.respond("Hi 👋 Send me a photo to convert it into a 2D anime art")
    elif event.photo:
        img = await event.download_media()
        try:
            await event.respond("Photo has been received, please wait")
            ome = convertai(img)

            await event.respond(file=ome)
            try:
                os.remove(img)
                os.remove(ome)
            except:
                pass
        except Exception as e:
            try:
                os.remove(img)
            except:
                pass
            await event.respond(f"Failed ERROR:{e}")
        


