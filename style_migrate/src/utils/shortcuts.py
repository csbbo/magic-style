from PIL import Image

import numpy as np
import random


def rand_str():
    random_list = [random.choice("123456789abcdef") for i in range(16)]
    return "".join(random_list)


def read_image(image_path):
    img = Image.open(image_path).convert('RGB')
    while img.width * img.height > 500000:
        img = img.resize((int(img.width / 1.5), int(img.height / 1.5)))
    img = np.array(img)
    return img
