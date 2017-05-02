# -*- coding: utf-8 -*-
import requests
import re
import os
from PIL import Image as resizer

API_URL = "https://www.googleapis.com/customsearch/v1?key=AIzaSyCriEfww77ytwFzsJ1fxaIdrHofTbcST7w&cx=013797314580565152036:39ywvzmb4jw&q=%s&searchType=image&start=%s"


def getImageFromCustomAPI(start, end, word, kind):
    for i in range(start, end, 10):
        print(API_URL % (word, str(i)))
        response = requests.get(API_URL % (word + ",正面", str(i)))
        for j in range(len(response.json()["items"])):
            json = response.json()["items"][j]
            res = requests.get(json["link"], stream=True)
            if res.status_code == 200:
                with open("images/target_%s_%s.png" % (kind, (str(i) + "_" + str(j))), 'wb') as file:
                    for chunk in res.iter_content(chunk_size=1024):
                        file.write(chunk)


def resizeImages(dirname, regular):
    """
    images下の画像を2次元の特徴ベクトルに変換する為に100x100リサイズを行う
    """
    for image in os.listdir(dirname):
        if re.match(regular, image):
            print(image)
            img = resizer.open("images/" + image, 'r')
            img = img.resize((100, 100))
            img.save("images/" + image, 'png', quality=100, optimize=True)
    print("resized")


def main():
    # 「人名,正面」にすると、より多くの正面画像を拾える
    # words = ['北川景子', '吉高由里子', '新垣結衣', '榮倉奈々', '安室奈美恵', '長澤まさみ', '西内まりや', '麻生久美子', '倉科カナ', '井上真央', '石原さとみ', 'ガッキー']
    # words = ['フィーフィー', '安藤なつ', '澤穂希', '白鳥久美子', '光浦靖子', 'ブルゾンちえみ', 'おかずクラブオカリナ']
    words = ['ガッキー']
    for word in words:
        getImageFromCustomAPI(1, 92, word, "YES-" + word + "_")

    resizeImages("images", "target_")

if __name__ == '__main__':
    main()
