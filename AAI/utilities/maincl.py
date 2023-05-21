import re
import json
import base64
import random
import hashlib
import requests
from PIL import Image
from aiohttp import ClientSession
from urllib.parse import quote

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

    async def concat(self, image, resample=Image.BICUBIC, resize_big_image=True):
        im1 = Image.open('AAI/res/faceu.png')
        im2 = Image.open(image)
        im3 = Image.open('AAI/res/faced.png')
        if im1.width == im2.width:
            _im1 = im1
            _im2 = im2
            _im3 = im3
        elif (((im1.width > im2.width) and resize_big_image) or
            ((im1.width < im2.width) and not resize_big_image)):
            _im1 = im1.resize((im2.width, int(im1.height * im2.width / im1.width)), resample=resample)
            _im2 = im2
            _im3 = im3.resize((im2.width, int(im3.height * im2.width / im3.width)), resample=resample)
        else:
            _im1 = im1
            _im2 = im2.resize((im1.width, int(im2.height * im1.width / im2.width)), resample=resample)
            _im3 = im3

        dst = Image.new('RGB', (_im1.width, _im1.height*2 + _im2.height))
        dst.paste(_im1, (0, 0))
        dst.paste(_im2, (0, _im1.height))
        dst.paste(_im3, (0, _im1.height+_im2.height))
        dst.save(image)
        return image

    async def save_crop(self, url):
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
        url = "https://ai.tu.qq.com/overseas/trpc.shadow_cv.ai_processor_cgi.AIProcessorCgi/Process"#"https://ai.tu.qq.com/trpc.shadow_cv.ai_processor_cgi.AIProcessorCgi/Process"
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
                                    proxy="http://dqwelxzk:ngkidbpl2ci0@45.155.68.129:8133"
                                    ) as resp:
                response: dict = await resp.json()
        return response

    async def process(self, filename):
        baseImage = base64.encodebytes(open(filename, "rb").read()).decode()
        if self.MODE == "qq":
            image = await self.concat(filename)
            baseImage = base64.encodebytes(open(image, "rb").read()).decode()
            return await self.qq(baseImage)
        elif self.MODE == "vid":
            return await self.qq(baseImage, mode="ai_painting_anime_video_entry")
        elif self.MODE == "3d":
            return await self.qq3d(baseImage)
        else:
            None
