from aaai.anime_response import AnimeResponse
from dataclasses import dataclass
from aaai.util import image_to_base64
import requests
import json
import hashlib

# Even though images is a list, you can't actually provide more than one image.
# you get the msg "list index out of range"
async def get_anime_image(filename: str, proxy) -> AnimeResponse:
    post_url = "https://ai.tu.qq.com/overseas/trpc.shadow_cv.ai_processor_cgi.AIProcessorCgi/Process"
    base64_image = await image_to_base64(filename)
    post_data = AnimePost(images=[base64_image])
    post_str = json.dumps(post_data.__dict__)
    url = f'https://h5.tu.qq.com{str(len(post_str))}HQ31X02e'.encode()
    sign_value = hashlib.md5(url).hexdigest()
    # proxies = {
    #    'http': 'http://86.92.97.181:80',
    #    'https': proxy,
    # }
    
    headers = {
    'Host': 'ai.tu.qq.com',
    "x-sign-value": sign_value, 
    "x-sign-version": "v1",
    'Origin': 'https://h5.tu.qq.com'
    }
    res = requests.post(post_url, headers=headers,  json=post_data.__dict__) #proxies=proxies,
    json_data = res.json()
    print("Done 0")
    anime = AnimeResponse(onem=0, errormsg="", **json_data)
    print("Done 1")
    return anime
