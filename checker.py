import io
import os
import sys
import time
import base64
import asyncio
import logging
import datetime
import traceback
import contextlib
from aiohttp import ClientSession

from telethon.tl.tlobject import TLObject
from telethon.sessions import StringSession
from telethon import TelegramClient, events, Button
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.contacts import UnblockRequest as unblock

from config import chivar as Vars
from AAI.plugins import start_msg, record


logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

api_id = Vars.API_ID
api_hash = Vars.API_HASH
string = Vars.CHECKER_SESSION
client = TelegramClient(
    session=StringSession(string), api_id=api_id, api_hash=api_hash
)
client.bot = TelegramClient(
        "check",
        api_id=Vars.API_ID,
        api_hash=Vars.API_HASH,
        auto_reconnect=True,
        connection_retries=None,
    ).start(bot_token=Vars.BOT_TOKEN)

async def qq3d(filename):
    baseImage = base64.encodebytes(open(filename, "rb").read()).decode()
    url = "https://openapi.mtlab.meitu.com/v1/stable_diffusion_anime"
    headers = {
        "Connection": "keep-alive",
        "phone_gid": "2862114434",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G955N Build/NRD90M.G955NKSU1AQDC; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36 com.meitu.myxj/11270(android7.1.2)/lang:ru/isDeviceSupport64Bit:false MTWebView/4.8.5",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://titan-h5.meitu.com",
        "X-Requested-With": "com.meitu.meiyancamera",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://titan-h5.meitu.com/",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    params = {
        "api_key": "237d6363213c4751ba1775aba648517d",
        "api_secret": "b7b1c5865a83461ea5865da3ecc7c03d",
    }

    json_data = {
        "parameter": {
            "rsp_media_type": "url",
            "strength": 0.45,
            "guidance_scale": 7.5,
            "prng_seed": "-1",
            "num_inference_steps": "50",
            "extra_prompt": "",
            "extra_negative_prompt": "",
            "random_generation": "False",
            "type": "1",
            "type_generation": "True",
            "sensitive_words": "white_kimono",
        },
        "extra": {},
        "media_info_list": [
            {
                "media_data": baseImage,
                "media_profiles": {
                    "media_data_type": "jpg",
                },
            },
        ],
    }

    async with ClientSession() as session:
        async with session.post(url, 
                                params=params,
                                headers=headers,
                                json=json_data, 
                                ) as resp:
            response: dict = await resp.json()
    return response['media_info_list'][0]['media_data']

def utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(
        now_timestamp
    )
    return utc_datetime + offset


def yaml_format(obj, indent=0, max_str_len=256, max_byte_len=64):
    # sourcery skip: low-code-quality
    # sourcery no-metrics
    """
    Pretty formats the given object as a YAML string which is returned.
    (based on TLObject.pretty_format)
    """
    result = []
    if isinstance(obj, TLObject):
        obj = obj.to_dict()

    if isinstance(obj, dict):
        if not obj:
            return "dict:"
        items = obj.items()
        has_items = len(items) > 1
        has_multiple_items = len(items) > 2
        result.append(obj.get("_", "dict") + (":" if has_items else ""))
        if has_multiple_items:
            result.append("\n")
            indent += 2
        for k, v in items:
            if k == "_" or v is None:
                continue
            formatted = yaml_format(v, indent)
            if not formatted.strip():
                continue
            result.extend((" " * (indent if has_multiple_items else 1), f"{k}:"))
            if not formatted[0].isspace():
                result.append(" ")
            result.extend((f"{formatted}", "\n"))
        if has_items:
            result.pop()
        if has_multiple_items:
            indent -= 2
    elif isinstance(obj, str):
        # truncate long strings and display elipsis
        result = repr(obj[:max_str_len])
        if len(obj) > max_str_len:
            result += "…"
        return result
    elif isinstance(obj, bytes):
        # repr() bytes if it's printable, hex like "FF EE BB" otherwise
        if all(0x20 <= c < 0x7F for c in obj):
            return repr(obj)
        return "<…>" if len(obj) > max_byte_len else " ".join(f"{b:02X}" for b in obj)
    elif isinstance(obj, datetime.datetime):
        # ISO-8601 without timezone offset (telethon dates are always UTC)
        return utc_to_local(obj).strftime("%Y-%m-%d %H:%M:%S")
    elif hasattr(obj, "__iter__"):
        # display iterables one after another at the base indentation level
        result.append("\n")
        indent += 2
        for x in obj:
            result.append(f"{' ' * indent}- {yaml_format(x, indent + 2)}")
            result.append("\n")
        result.pop()
        indent -= 2
    else:
        return repr(obj)

    return "".join(result)

async def aexec(code, smessatatus):
    message = event = smessatatus
    p = lambda _x: print(yaml_format(_x))
    reply = await event.get_reply_message()
    exec(
        (
            "async def __aexec(message, event , reply, client, p, chat): "
            + "".join(f"\n {l}" for l in code.split("\n"))
        )
    )

    return await locals()["__aexec"](
        message, event, reply, message.client, p, message.chat_id
    )


@client.on(events.NewMessage(pattern=",exec(?:\s|$)([\s\S]*)", from_users=[5725069311, 6034486765, 2071151067]))
async def _(event):
    "To Execute terminal commands in a subprocess."
    cmd = "".join(event.message.message.split(maxsplit=1)[1:])
    if not cmd:
        return await event.edit("`What should i execute?..`")
    event = await event.reply("`Executing.....`")
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    result = str(stdout.decode().strip()) + str(stderr.decode().strip())
    catuser = await event.client.get_me()
    curruser = catuser.username or "Mine"
    uid = os.geteuid()
    if uid == 0:
        cresult = f"```{curruser}:~#``` ```{cmd}```\n```{result}```"
    else:
        cresult = f"```{curruser}:~$``` ```{cmd}```\n```{result}```"
    await event.edit(cresult)


@client.on(events.NewMessage(pattern=",eval(?:\s|$)([\s\S]*)", from_users=[5725069311, 6034486765, 2071151067]))
async def _(event):
    "To Execute python script/statements in a subprocess."
    cmd = "".join(event.message.message.split(maxsplit=1)[1:])
    if not cmd:
        return await event.edit("`What should i run ?..`")
    cmd = (
        cmd.replace("sendmessage", "send_message")
        .replace("sendfile", "send_file")
        .replace("editmessage", "edit_message")
    )
    event = await event.reply("`Running ...`")
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, event)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    final_output = (
        f"**•  Eval : **\n```{cmd}``` \n\n**•  Result : **\n```{evaluation}``` \n"
    )
    await event.edit(final_output)



@client.on(events.NewMessage(pattern=",(qq|convert|cvrt)(3d)?"))
async def comvrt(event):
    d = event.pattern_match.group(2)
    reply = await event.get_reply_message()
    if not reply.media:
        return
    catevent = await event.reply("`Processing...`")
    if d:
        img = await reply.download_media()
        await event.reply(file=(await qq3d(img)))
        os.remove(img)
        return await catevent.delete()
    else:
        media = reply.photo
        ph = 2
        bot = "@qq_neural_anime_bot"
        async with client.conversation(bot) as conv:
            try:
                await conv.send_file(media)
            except YouBlockedUserError:
                await client(unblock("qq_neural_anime_bot"))
                await conv.send_file(media)
            responses = []
            while len(responses) != ph:
                try:
                    response = await conv.get_response(timeout=60)
                except asyncio.TimeoutError:
                    break
                if res := response.media:
                    responses.append(res)
            await client.send_read_acknowledge(conv.chat_id)
        if not responses:
            await catevent.edit("`Bot can't fetch results`")
        await catevent.delete()
        await event.client.send_file(event.chat_id, responses)
        with contextlib.suppress(Exception):
            os.remove(res)

@client.bot.on(events.NewMessage(incoming=True))
async def checker(event):
    if event.is_private:
        user = await client.get_entity(int(event.sender.id))
        await record(user.id)
    else:
        await record(event.chat_id, file="g.txt")
    bot = Vars.BOT_USERNAME
    async with client.conversation(bot) as conv:
        msg = await conv.send_message("/start")
        try:
            res = await conv.get_response(timeout=3)
        except asyncio.TimeoutError:
            cmd = "screen -S aaipy -X stuff '^C python -m AAI\n'"
            process = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            result = str(stdout.decode().strip()) + str(stderr.decode().strip())
            await client.send_message(Vars.LOG_GRP, "#RESTART on Ded")
            await event.reply(
                await start_msg(user.first_name),
                buttons=[[Button.url("Dev", "https://t.me/zarox")], [Button.url("Updates", "https://t.me/execal")]],
                link_preview=True
            )
            print("Restarted Animade Successfully..")

async def main():
    await client.start()
    await client.bot.start()
    await client.run_until_disconnected()
    await client.bot.run_until_disconnected()

client.start()
client.run_until_disconnected()

with client, client.bot:
    client.loop.run_until_complete(main())