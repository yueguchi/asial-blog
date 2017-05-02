# -*- coding: utf-8 -*-

import os
import io
import urllib.request
from PIL import Image
from sklearn.externals import joblib
import numpy as np

TARGET_OS_IMAGE_FILES = r"(犬|猫)-"


def convertImageVector3(img):
    """
    3次元(100x100x3(RGB))から1次元に変換する
    """
    print(img.shape)
    s = img.shape[0] * img.shape[1] * img.shape[2]
    img_vector3 = img.reshape(1, s)
    return img_vector3[0]


def main(imgs):
    # 試験データをhttp経由で取得し、100x100にリサイズ
    t_image_vector3 = []
    for img in imgs:
        target = Image.open(io.BytesIO(urllib.request.urlopen(img).read())).resize((100, 100))
        t_image_vector3.append(convertImageVector3(np.asarray(target)))

    # 学習済みデータの取得
    learnedFile = os.path.dirname(__file__) + "/save/animals.pkl"
    clf = joblib.load(learnedFile)

    # 予測開始
    res = clf.predict(t_image_vector3)
    print(res)

if __name__ == '__main__':
    dogs = ["https://ssl-stat.amebame.com/pub/content/8265872137/user/article/unknown/unknown/223105560820719701/663d206ab45ac8b27dc7930827123c4e/uploaded.jpg?option=crop&width=700",
            "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcRDF49Z0NPvq5RSBtVYxgWNCEbMln_Bk5ClnMVly1VytI1yHcaK",
            "https://i.ytimg.com/vi/QFcHl11dX0M/maxresdefault.jpg"]
    main(dogs)
