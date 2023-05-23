async def start_msg(name):
    return f"""Hi {name} 👋[‍](https://telegra.ph/file/8c2160c0b218d61ac0b39.jpg). Send me a photo to convert it into a 2D anime art using AI
    
If the bot stops or not convert images contact the dev, [@zarox]

Send /help
"""


help_msg = """Send your photos or selfies to convert them in 2d Anime art using AI
or
Use /convrt command by replying to any image anywhere

For any concern, appreciation or suggestion contact @Zarox
"""

async def record(id, file="u.txt"):
    ids = []
    with open(f"AAI/res/{file}")as file:
        ids = list(map(lambda x: int(x[:-1]), list(set(file.readlines()))))
        
    with open(f"AAI/res/{file}", "a+")as file:
        if id in ids:
            return 
        else:
            file.write(f"{id}\n")
