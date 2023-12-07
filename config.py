import os

class chivar(object):
    API_ID = int(os.getenv("API_ID"))
    API_HASH = os.getenv("API_HASH")
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    BOT_USERNAME = os.getenv("BOT_USERNAME")
    OWNER_ID = int(os.getenv("OWNER_ID"))
    SUDO_IDS = os.getenv("SUDO_IDS")
    LOG_GRP = int(os.getenv("LOG_GRP"))
    PROXY = os.getenv("PROXY")
    LOCALCH = bool(os.getenv("LOCALCH"))
