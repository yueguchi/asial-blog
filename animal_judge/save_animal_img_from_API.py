# -*- coding: utf-8 -*-
import requests
import re
import os
from PIL import Image as resizer

TARGET_OS_IMAGE_FILES = r"(犬|猫)-"

API_URL = "https://www.googleapis.com/customsearch/v1?key=AIzaSyCriEfww77ytwFzsJ1fxaIdrHofTbcST7w&cx=013797314580565152036:39ywvzmb4jw&q=%s&searchType=image&start=%s"


def saveAnimal(kind):
    for i in range(1, 92, 10):
        print(API_URL % (kind, str(i)))
        response = requests.get(API_URL % (kind, str(i)))
        for j in range(len(response.json()["items"])):
            json = response.json()["items"][j]
            res = requests.get(json["link"], stream=True)
            if res.status_code == 200:
                with open("images/%s-%s.png" % (kind, (str(i) + "_" + str(j))), 'wb') as file:
                    for chunk in res.iter_content(chunk_size=1024):
                        file.write(chunk)
        print("saved")

def resizeImages():
    """
    images下の画像を2次元の特徴ベクトルに変換する為に100x100リサイズを行う
    """
    for image in os.listdir('images'):
        if re.match(TARGET_OS_IMAGE_FILES, image):
            img = resizer.open("images/" + image, 'r')
            img = img.resize((100, 100))
            img.save("images/" + image, 'png', quality=100, optimize=True)
    print("resized")


if __name__ == '__main__':
    animals = ['犬', '猫']
    # DL
    for animal in animals:
        saveAnimal(animal)

    resizeImages()
