import sys
import glob
import shlex
import asyncio
import logging
import importlib
from typing import Tuple
from pathlib import Path
from subprocess import PIPE, Popen
from telethon import Button

from .. import aai, Vars

def install_pip(pipfile):
    print(f"installing {pipfile}")
    pip_cmd = ["pip", "install", f"{pipfile}"]
    process = Popen(pip_cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    return stdout

def load_module(plugin_name, p_path=None):
    if p_path is None:
        path = Path(f"AAI/plugins/{plugin_name}.py")
        name = f"AAI.plugins.{plugin_name}"
    else:
        path = Path(f"{p_path}/{plugin_name}.py")
        name = f"{p_path}/{plugin_name}".replace("/", ".")
    spec = importlib.util.spec_from_file_location(name, path)
    load = importlib.util.module_from_spec(spec)
    load.logger = logging.getLogger(plugin_name)
    spec.loader.exec_module(load)
    sys.modules[f"AAI.plugins.{plugin_name}"] = load
    print(f"★ Successfully Installed: {plugin_name}")
    
#from catuserbot
def load_plugins(folder):
    path = f"AAI/{folder}/*.py"
    files = glob.glob(path)
    files.sort()
    for name in files:
        with open(name) as f:
            path1 = Path(f.name)
            shortname = path1.stem
            try:
                flag = True
                check = 0
                while flag:
                    try:
                        load_module(
                            shortname.replace(".py", ""),
                            p_path=f"AAI/{folder}",
                        )
                        break
                    except ModuleNotFoundError as e:
                        install_pip(e.name)
                        check += 1
                        if check > 5:
                            break
            except Exception as e:
                print(f"unable to load {shortname} because of error {e}")

async def rid(e):
    rid = await e.get_reply_message()
    return rid.id if rid else e.id

def mentionuser(name, userid):
    return f"[{name}](tg://user?id={userid})"

async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )




async def startup():
    await aai.send_message(Vars.LOG_GRP, "**AnimeAI has been started from host successfully.**", buttons=[(Button.url("Shinichi", "https://t.me/catuserbotot"),)],)
