import os
import re
import json
import base64
import random
import hashlib
import requests
from PIL import Image
from io import BytesIO
from aiohttp import ClientSession
from urllib.parse import quote
from telethon import Button

from .. import Vars
# "ai_painting_spring_entry"
# "ai_painting_spring_img_entry"
# "different_dimension_me_img_entry"
# "ai_painting_anime_img_entry"
# "ai_painting_anime_video_entry"
# "aigcsdk_ai_painting_anime_img_entry"
mode = "different_dimension_me_img_entry"

class Animade:
    def __init__(self, mode:str):
        self.MODE = mode

    async def face_hack(self, source_img_buffer):
        print("Face Hack")
        FACE_HACK_SIZE = 170
        FACE_HACK_SPACE = 200
        face_hack_buffer = Image.open("AAI/res/face.jpg")
        source_img = Image.open(source_img_buffer)
        source_img_width, source_img_height = source_img.size

        img_width = source_img_width
        img_height = source_img_height
        img = source_img.copy()

        if source_img_height > source_img_width:
            ratio = source_img_height / source_img_width
            if ratio > 1.5:
                img_height = int(source_img_width * 1.5)
            else:
                img_width = int(source_img_height / 1.5)
        else:
            ratio = source_img_width / source_img_height
            if ratio > 1.5:
                img_width = int(source_img_height * 1.5)
            else:
                img_height = int(source_img_width / 1.5)

        img_width = max(img_width, FACE_HACK_SIZE)
        img_height = max(img_height, FACE_HACK_SIZE)

        img = img.resize((img_width, img_height), resample=Image.LANCZOS)

        img_buffer = BytesIO()
        img.save(img_buffer, format='JPEG')
        img_buffer.seek(0)
        img_buffer = Image.open(img_buffer)
        if img_height > img_width:
            result_img = Image.new("RGB", (img_width, img_height + FACE_HACK_SIZE * 2 + FACE_HACK_SPACE * 2), (255, 255, 255))
            result_img.paste(img_buffer, (0, FACE_HACK_SIZE + FACE_HACK_SPACE))

            face_hack_img = face_hack_buffer.resize((FACE_HACK_SIZE, FACE_HACK_SIZE), resample=Image.LANCZOS)
            result_img.paste(face_hack_img, (int(img_width / 2 - FACE_HACK_SIZE / 2), 0))
            result_img.paste(face_hack_img, (int(img_width / 2 - FACE_HACK_SIZE / 2), FACE_HACK_SIZE + FACE_HACK_SPACE + img_height + FACE_HACK_SPACE))
        else:
            result_img = Image.new("RGB", (img_width + FACE_HACK_SIZE * 2 + FACE_HACK_SPACE * 2, img_height), (255, 255, 255))
            result_img.paste(img_buffer, (FACE_HACK_SIZE + FACE_HACK_SPACE, 0))

            face_hack_img = face_hack_buffer.resize((FACE_HACK_SIZE, FACE_HACK_SIZE), resample=Image.LANCZOS)
            result_img.paste(face_hack_img, (0, int(img_height / 2 - FACE_HACK_SIZE / 2)))
            result_img.paste(face_hack_img, (FACE_HACK_SIZE + FACE_HACK_SPACE + img_width + FACE_HACK_SPACE, int(img_height / 2 - FACE_HACK_SIZE / 2)))

        result_buffer = BytesIO()
        result_img.save(result_buffer, format='JPEG')
        result_buffer.seek(0)
        return result_buffer.getvalue()

    async def save_crop(self, url, strip=False):
        output_name = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz1234567890", k=6)) + ".jpg"
        image_bytes = requests.get(url).content
        with open(output_name, "wb") as img:
            img.write(image_bytes)
        image = Image.open(output_name)
        w, h = image.size
        image.crop((0, 0, w, h-181)).save(output_name)
        if w>h:
            image.crop(((w/2)+7, 22, w-22, h-210)).save(f"sec{output_name}")
        else:
            image.crop((22, (h-170)/2, w-22, h-210)).save(f"sec{output_name}")
        return [output_name, f"sec{output_name}"]

    def auth(self, data: dict):
        r = json.dumps(data)
        pattern = "/%[89ABab]/g"
        parse = quote(r)
        count = sum(1 for _ in re.finditer(pattern, parse))
        return hashlib.md5(f"https://h5.tu.qq.com{len(r)+count}HQ31X02e".encode()).hexdigest()

    async def qq3d(self, baseimage):
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
                    "media_data": baseimage,
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
        return response

    async def qq(self, baseimage, mode=mode):
        proxy = Vars.PROXY
        if Vars.LOCALCH:
            url = "https://ai.tu.qq.com/overseas/trpc.shadow_cv.ai_processor_cgi.AIProcessorCgi/Process"
        else:
            url = "https://ai.tu.qq.com/trpc.shadow_cv.ai_processor_cgi.AIProcessorCgi/Process"
        data = {
            "busiId": mode,
            "extra": "{\"face_rects\":[],\"version\":2,\"platform\":\"web\",\"data_report\":{\"parent_trace_id\":\"2ac8ec9d-a574-7952-0f8c-e80f2adf7105\",\"root_channel\":\"\",\"level\":0}}",#'{"face_rects":[],"version":2,"platform":"web","data_report":{"parent_trace_id":"2ac8ec9d-a574-7952-0f8c-e80f2adf7105","root_channel":"","level":0}}',
            "images": [baseimage]
        }
        headers = {
            'Host': 'ai.tu.qq.com',
            'Content-Type': 'application/json',
            'Origin': 'https://h5.tu.qq.com',
            'Referer': 'https://h5.tu.qq.com/',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'x-sign-value': str(self.auth(data)),
            'x-sign-version': 'v1',
        }
        
        async with ClientSession() as session:
            async with session.post(url, 
                                    json=data, 
                                    headers=headers,
                                    proxy=proxy
                                    ) as resp:
                response: dict = await resp.json()
        return response

    async def process(self, event, filename):
        retries = 7
        if self.MODE == "3d":
            result = await self.qq3d(base64.encodebytes(open(filename, "rb").read()).decode())
            return result['media_info_list'][0]['media_data']
        
        elif self.MODE == "qq":
            baseImage = base64.encodebytes(open(filename, "rb").read()).decode()
            result = await self.qq(baseImage)
            if result['code'] == 1001:
                result = await self.qq(base64.b64encode((await self.face_hack(filename))).decode('utf-8'))
            while result['code'] == 2111 and retries > 0:
                retries -= 1
                result = await self.qq(event, baseImage)
            if result['code'] != 0:
                os.remove(filename)
                await event.edit(f'Error :`{result["msg"]}`\n\nIf you would like to support this free project and move it to better server with less errors. Contact @zarox', buttons=[Button.url("Support", url="https:/t.me/execal")])
                return None
            output = json.loads(result['extra'])['img_urls'][0]
            output = await self.save_crop(output)
            return output