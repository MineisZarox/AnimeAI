async def start_msg(name):
    return f"""Hi {name} 👋[‍](https://telegra.ph/file/8c2160c0b218d61ac0b39.jpg). Send me a photo to convert it into a 2D and 3d anime art using AI
    
If the bot stops or not convert images contact the dev report here [@ExecalChat]
Commands = /qq and /qq3d

Send /help to check the Usage in details.
"""


help_msg = """Send your photos or selfies to convert them in 2d Anime or 3d Anime art using AI

Use /qq for 2d Anime AI
Use /qq3d for 3d Anime AI

For any concern, appreciation or suggestion message here [@ExecalChat]
"""

async def record(idd, fi="u.txt"):
    ids = []
    with open(f"AAI/res/{fi}")as file:
        ids = list(map(lambda x: int(x[:-1]), list(set(file.readlines()))))
        
    with open(f"AAI/res/{fi}", "a+")as file:
        if idd in ids:
            return 
        else:
            file.write(f"{idd}\n")
