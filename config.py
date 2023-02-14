import os 

class chivar(object):
    API_ID = int(os.getenv("API_ID")) or 7252696
    API_HASH = os.getenv("API_HASH") or "5258ec8dcf079134364225fe060fcf37"
    BOT_TOKEN = os.getenv("BOT_TOKEN") or "6150871974:AAGAv2dOGKfq02ItL2kjsRHJAlzFNJHb5nA"
    BOT_USERNAME = os.getenv("BOT_UN") or "@Paintyourselfrobot"
    OWNER_ID = int(os.getenv("OWNER_ID")) or 2071151067
    SUDO_IDS = os.getenv("SUDO_IIDS") or "2071151067 5725069311"
    LOG_GRP = int(os.getenv("LOG_GRP")) or -1001543387017
