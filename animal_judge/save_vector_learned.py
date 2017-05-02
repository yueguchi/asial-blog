# -*- coding: utf-8 -*-
"""
画像特徴ベクトルに変換し、学習済みファイル(pkl)に保存する
"""
from PIL import Image
import os
import re
import numpy as np
from sklearn.externals import joblib
from sklearn import svm

TARGET_OS_IMAGE_FILES = r"(犬|猫)-"


def convertImageVector3(img):
    """
    3次元(100x100x3(RGB))から1次元に変換する
    """
    print(img.shape)
    s = img.shape[0] * img.shape[1] * img.shape[2]
    img_vector3 = img.reshape(1, s)
    return img_vector3[0]


def main():
    files = ["images/" + f for f in os.listdir("images") if re.match(TARGET_OS_IMAGE_FILES, f)]
    labels = []
    datas = []
    for image in files:
        if re.match("images/" + TARGET_OS_IMAGE_FILES, image):
            print(image)
            as_arrayed_img = np.asarray(Image.open(image))
            # 3次元かどうか
            if (len(as_arrayed_img.shape) == 3):
                # RGBが3がどうか
                if (as_arrayed_img.shape[2] == 3):
                    datas.append(convertImageVector3(np.asarray(Image.open(image))))
                    labels.append(image.split("images/")[1].split("-")[0])
                else:
                    print("skip not rgb3")
            else:
                print("skip not vector3")
    # データを学習
    clf = svm.SVC()
    print(labels)
    clf.fit(datas, labels)
    joblib.dump(clf, "save/animals.pkl")
    print("OK")

if __name__ == '__main__':
    main()
