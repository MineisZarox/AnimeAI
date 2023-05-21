from . import aai
from .utilities.utility import load_plugins, startup

async def initiation():
    load_plugins("plugins")
    print("Anime AI Deployed Successfully!")
    await startup()
    return

aai.loop.run_until_complete(initiation())

if __name__ == "__main__":
    aai.run_until_disconnected()
