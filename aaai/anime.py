from aaai.util import save_anime_image
from aaai.anime_post import AnimePost
import random
import sys



def convertai(name):
    if len(name) < 2:
        return "Provide a valid Image file"
    
    ALPHABET = "abcdefghijklmnopqrstuvwxyz"
    output_name = ''.join(random.choices(ALPHABET, k=6)) + ".jpg"

    filename = name
    print("Processing image: ", filename)
    anime = AnimePost.get_anime_image(filename)
    save_anime_image(output_name, anime.extra[0])
    
    return output_name
