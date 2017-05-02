# -*- coding: utf-8 -*-

import os
import io
import urllib.request
from PIL import Image
from sklearn.externals import joblib
import numpy as np
import cv2
from datetime import datetime as dt
import requests
from bs4 import BeautifulSoup as bs
import uuid


def convertImageVector3(img):
    """
    3次元(100x100x3(RGB))から1次元に変換する
    """
    s = img.shape[0] * img.shape[1] * img.shape[2]
    img_vector3 = img.reshape(1, s)
    return img_vector3[0]


def saveFaceImg(img):
    image = np.asarray(img)
    cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_alt2.xml')
    faces = cascade.detectMultiScale(image)

    if (len(faces) == 1):
        (x, y, w, h) = faces[0]
        image = image[y:y+h, x:x+w]
        image = cv2.cvtColor(cv2.resize(image, (100, 100)), cv2.COLOR_BGR2RGB)
        cv2.imwrite('{}/{}'.format("targets", dt.now().strftime("%Y%m%d%H%M%S") + "_" + str(uuid.uuid1()) + ".png"), image)
        return image
    return ""


def main(imgs):
    # 試験データをhttp経由で取得し、100x100にリサイズ
    t_image_vector3 = []
    for img in imgs:
        target = saveFaceImg(Image.open(io.BytesIO(urllib.request.urlopen(img).read())).resize((100, 100)))
        if (len(target)):
            print(img)
            t_image_vector3.append(convertImageVector3(target))
    # 学習済みデータの取得
    learnedFile = os.path.dirname(__file__) + "/pkls/beauty.pkl"
    clf = joblib.load(learnedFile)
    # 予測開始
    res = clf.predict(t_image_vector3)
    for ret in res: print(ret)

if __name__ == '__main__':
    SEARCH_URL = r"https://www.google.co.jp/search?q=%s&source=lnms&tbm=isch&sa=X&biw=1439&bih=780"
    TARGET_IMG_SRC_PATTERN = r"https://encrypted-"

    targets = []
    html = requests.get(SEARCH_URL % "ガッキー").text
    # BeautifulSoupでHTMLを解析
    soup = bs(html, 'html.parser')
    target_src = []
    images = soup.find_all('img')
    for img in images:
        targets.append(img['src'])
    main(targets)
    # main(['http://blog-imgs-42.fc2.com/m/e/m/memoriup/03267.jpg'])
