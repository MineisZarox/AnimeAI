from aaai.util import save_anime_image
from aaai.anime_post import AnimePost
import random
import sys



def convertai(name, proxy):
    if len(name) < 2:
        return "Provide a valid Image file"
    
    ALPHABET = "abcdefghijklmnopqrstuvwxyz"
    output_name = ''.join(random.choices(ALPHABET, k=6)) + ".jpg"

    filename = name
    print("Processing image: ", filename)
    anime = AnimePost.get_anime_image(filename, proxy)
    if anime.onem == 0:
        output_name = anime.errormsg
        print(anime.errormsg)
    else:
        save_anime_image(output_name, anime.extra[0])
        print("Done 2")
    
    return output_name
