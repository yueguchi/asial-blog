# -*- coding: utf-8 -*-

"""
犬と猫の画像をGoogle画像検索から取得し、
resizeした結果をimages下に保存する
あんま実行するとGoogleに怒られるかも
"""

from bs4 import BeautifulSoup as bs
import requests
import re
import os
from PIL import Image as resizer

SEARCH_URL = r"https://www.google.co.jp/search?q=%s&source=lnms&tbm=isch&sa=X&biw=1439&bih=780"
TARGET_IMG_SRC_PATTERN = r"https://encrypted-"
TARGET_OS_IMAGE_FILES = r"(犬|猫)-"


def saveAnimal(kind):
    """
    Googleに画像検索をかけ、特定のimg srcのみを抽出する
    画像はimages下に保存するが、一気に実行せず、1024kbずつチャンク処理にて読み込む
    """
    html = requests.get(SEARCH_URL % kind).text
    # BeautifulSoupでHTMLを解析
    soup = bs(html, 'html.parser')
    animal_src = []
    images = soup.find_all('img')
    for img in images:
        if re.match(TARGET_IMG_SRC_PATTERN, img['src']):
            animal_src.append(img['src'])
    for url in animal_src:
        print(url)
        res = requests.get(url, stream=True)
        if res.status_code == 200:
            with open("images/%s-%s.png" % (kind, url.split("tbn:")[-1]), 'wb') as file:
                for chunk in res.iter_content(chunk_size=1024):
                    file.write(chunk)


def resizeImages():
    """
    images下の画像を2次元の特徴ベクトルに変換する為に100x100リサイズを行う
    """
    for image in os.listdir('images'):
        if re.match(TARGET_OS_IMAGE_FILES, image):
            img = resizer.open("images/" + image, 'r')
            img = img.resize((100, 100))
            img.save("images/" + image, 'png', quality=100, optimize=True)

animals = ['犬', '猫']
if __name__ == '__main__':
    # DL
    for animal in animals:
        saveAnimal(animal)
    # 縮小
    resizeImages()
