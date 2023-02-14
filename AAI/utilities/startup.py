from .. import aai, Vars
from telethon import Button

async def startup():
    await aai.send_message(Vars.LOG_GRP, "**AnimeAI has been started successfully.**", buttons=[(Button.url("Shinichi", "https://t.me/catuserbotot"),)],)
