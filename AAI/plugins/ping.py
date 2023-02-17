from PIL import Image
from telethon import events
from .. import aai, Vars
from aaai.anime import convertai
import random
import sys
import os

sudos = list(map(int, (Vars.SUDO_IDS).split(" ")))
httpsproxy = "http://178.208.66.243:3128"

def crop(out):
    image = Image.open(out)
    w, h = image.size
    image.crop((0, 0, w, h-181)).save(out)
    if w>h:
        image.crop(((w/2)+7, 22, w-22, h-210)).save("sec"+out)
    else:
        image.crop((22, (h-170)/2, w-22, h-210)).save("sec"+out)
    return [out, "sec"+out]


@aai.on(events.NewMessage(incoming=True))
async def start(event):
    user = await aai.get_entity(int(event.sender.id))
    reply = await event.get_reply_message()
    img = None
    if event.text == "/start" and event.is_private:
        await event.reply(f"Hi {user.first_name} 👋 Send me a photo to convert it into a 2D anime art")
    if event.is_private and event.photo:
        img = await event.download_media()
    if reply and reply.photo and event.text == "/convrt" :
        img = await reply.download_media()
    if img:
        kk = await event.reply("Processing... ✨")
        try:
            ome = convertai(img, httpsproxy)

            if os.path.exists(ome):
                crpp = crop(ome)
                await event.reply(file=crpp[0])
                await event.reply(file=crpp[1])
                await kk.delete()
            else:
                await kk.edit(f"Error: {ome}")
            try:
                os.remove(img)
                os.remove(ome)
                os.remove("sec"+ome)
            except:
                pass
        except Exception as e:
            try:
                os.remove(img)
            except:
                pass

            mmm = await aai.send_message(Vars.LOG_GRP, f"{e}")
            await kk.edit(f"Failed. Try again after few min or report/forward [here](t.me/zaroxhub) Error id `{mmm.id}`", link_preview=False)

        
@aai.on(events.NewMessage(incoming=True))
async def _(event):
    user = await aai.get_entity(int(event.sender.id))
    reply = await event.get_reply_message()
    if event.text.startswith("/logs") and user.id in sudos:
        try:
            id = reply.text.split(" ")[-1] if reply else event.text.split(" ")[1]
            if id != None and id.isdigit():
                msg = await aai.get_messages(Vars.LOG_GRP, ids=int(id))
                await event.reply(f"`{msg.message}`")
            else:
                id = id[1:-1]
                if id != None and id.isdigit():
                    msg = await aai.get_messages(Vars.LOG_GRP, ids=int(id))
                    await event.reply(f"`{msg.message}`")
                
            
            
        except Exception as e:
            await event.reply(f"Invalid id {e}")
        
    if event.text.startswith("/chpro") and user.id in sudos:
        proxy = reply.text.split(" ")[-1] if reply else event.text.split(" ")[1]
        global httpsproxy
        httpsproxy = f"https://{proxy}"
        await event.reply(f"Changed proxy url to {httpsproxy}")
        print(httpsproxy)
