import os
import logging
from telethon import TelegramClient
from telethon.network.connection.tcpabridged import ConnectionTcpAbridged
from config import chivar as Vars

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

aai = TelegramClient(
        "animeai",
        api_id=Vars.API_ID,
        api_hash=Vars.API_HASH,
        connection=ConnectionTcpAbridged,
        auto_reconnect=True,
        connection_retries=None,
    ).start(bot_token=Vars.BOT_TOKEN)

"""Shinichi = TelegramClient(
    session=STR,
    api_id=API_ID,
    api_hash=API_HASH,
    loop=loop,
    app_version=__version__,
    connection=ConnectionTcpAbridged,
    auto_reconnect=True,
    connection_retries=None,
)"""


