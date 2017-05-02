# -*- coding: utf-8 -*-
"""
Face画像特徴ベクトルに変換し、保存する
"""
from PIL import Image
import os
import re
import numpy as np
from sklearn.externals import joblib
from sklearn import svm


def convertImageVector3(img):
    """
    3次元(100x100x3(RGB))から1次元に変換する
    """
    s = img.shape[0] * img.shape[1] * img.shape[2]
    img_vector3 = img.reshape(1, s)
    return img_vector3[0]


def main():
    """
    3次元ベクトル学習画像データと正解ラベルを対にして、pickleファイルにして保存する
    """
    files = ["faces/" + f for f in os.listdir("faces") if re.match("target_", f)]
    labels = []
    datas = []
    for image in files:
        as_arrayed_img = np.asarray(Image.open(image))
        # 3次元かどうか
        if (len(as_arrayed_img.shape) == 3):
            # RGBが3がどうか
            if (as_arrayed_img.shape[2] == 3):
                datas.append(convertImageVector3(np.asarray(Image.open(image))))
                # 「YES」と「NO」を抽出
                labels.append(image.split("faces/target_")[1].split("-")[0])
            else:
                print("skip not rgb3")
    print("converted.")
    return (datas, labels)


def learn(datas, labels):
    """
    データを学習
    """
    clf = svm.LinearSVC()
    clf.fit(datas, labels)
    joblib.dump(clf, "pkls/beauty.pkl")
    print("learned.")

if __name__ == '__main__':
    datas, labels = main()
    print(len(datas), len(labels))
    learn(datas, labels)
