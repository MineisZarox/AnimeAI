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

prompts = {}

def chunks(data, SIZE=10000):                        
    it = iter(data)
    for i in range(0, len(data), SIZE):           
        yield {k:data[k] for k in islice(it, SIZE)} 

def genbtns(styles, rows, uid, indexx=0):
    plugins = list(styles.keys())
    dt = list(styles.values())
    row = len(plugins)//rows
    row += 0 if len(plugins)%rows == 0 else 1
    buttons = [[]*i for i in range(0, row)]
    for k ,i in enumerate(buttons):
        for ii in range(k*rows, (k+1)*rows):
            try:
                i.append(Button.inline(plugins[ii].title(), data=f"{dt[ii]}_{uid}_{indexx}"))
            except:
                break
    return buttons
  
styless = Som.Styles()
styles = [i for i in chunks(styless, 16)]

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
    
    

@aai.on(events.NewMessage(incoming=True, pattern=f"/dream(s)?({Vars.BOT_USERNAME})?(?:\s|$)([\s\S]*)"))
async def dream(event):
    user = await aai.get_entity(event.sender_id)
    s = event.pattern_match.group(1)
    prompt = "".join(event.message.message.split(maxsplit=1)[1:])
    if not prompt:
        return await event.reply("Empty Prompt...")
    if s:
        prompts[user.id] = {'prompt': prompt, 'gen': 0}
        buttons = genbtns(styles[0], 2, user.id)
        buttons.append([Button.inline("Next", data=f"_1_nav_{user.id}")])
        return await event.reply(f"👾 **Dream: **`{prompt}`", buttons=buttons)
    
    if prompt.split(" ", 1)[0].isdigit():
        style, prompt = prompt.split(" ", 1)
    else:
        style = '80'
    

    message = await event.reply("Processing... ✨")
    try:
        await event.reply(file=(await Somnium.Generate(prompt, int(style))))
        await message.delete()
    except Exception as e:
        print(e)
        await message.edit(str(e))

        
#aai.on(events.NewMessage(incoming=True, pattern=f"/dream({Vars.BOT_USERNAME})?(?:\s|$)([\s\S]*)"))
async def dream(event):
    prompt = "".join(event.message.message.split(maxsplit=1)[1:])
    if not prompt:
        return await event.reply("Empty Prompt...")
                                                                                                                     
#Next | Back
@aai.on(events.CallbackQuery(pattern="_(\d+)_nav_(\d+)"))
async def cg(event):
    user_ = int(event.sender_id)
    user = int(event.pattern_match.group(2).decode("UTF-8"))
    if user != user_: return await event.answer("Send your own query")
    indexx = int(event.pattern_match.group(1).decode("UTF-8"))
    buttons = genbtns(styles[indexx], 2,  int(event.sender_id), indexx=indexx)
    buttons.append([])
    if indexx >= 1: buttons[-1].insert(0, Button.inline("Back", data=f"_{indexx-1}_nav_{user}"))
    if indexx < (len(styles)-1): buttons[-1].insert(1, Button.inline("Next", data=f"_{indexx+1}_nav_{user}"))                                               
    prompt = prompts[user]['prompt']
    gen = prompts[user]['gen']
    await event.edit(f"👾 **Dream: **`{prompt}`\n🫧 **Gens: **`{gen}`", buttons=buttons)                                        
      
@aai.on(events.CallbackQuery(pattern="(\d+)_(\d+)_(\d+)"))
async def btns(event):
    user_ = int(event.sender_id)
    style = event.pattern_match.group(1).decode("UTF-8")
    user = int(event.pattern_match.group(2).decode("UTF-8"))
    indexx = int(event.pattern_match.group(3).decode("UTF-8"))
    if user != user_: return await event.answer("Send your own query")
    prompt = prompts[user]['prompt']
    gen = prompts[user]['gen']
    gen += 1
    buttons = genbtns(styles[indexx], 2, int(event.sender_id), indexx=indexx)
    buttons.append([])
    if indexx >= 1: buttons[-1].insert(0, Button.inline("Back", data=f"_{indexx-1}_nav_{user}"))
    if indexx < (len(styles)-1): buttons[-1].insert(1, Button.inline("Next", data=f"_{indexx+1}_nav_{user}"))
    await event.edit(f"👾 **Dream: **`{prompt}`\n\n🌀 **Gens: ** `{gen}`", buttons=buttons)
    await aai.send_message(event.chat_id, file=(await Somnium.Generate(prompt, style))) 