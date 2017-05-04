# -*- coding: utf-8 -*-
"""
Face画像特徴ベクトルに変換し、保存する
"""
from PIL import Image
import os
import re
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
import pylab as pl
from sklearn.externals import joblib
from sklearn import svm


def convertImageVector3to1(img):
    """
    3次元(100x100x3(RGB))から1次元に変換する
    """
    s = img.shape[0] * img.shape[1] * img.shape[2]
    img_vector3 = img.reshape(1, s)
    return img_vector3[0]


def getDatas():
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
                datas.append(convertImageVector3to1(np.asarray(Image.open(image))))
                # 「YES」と「NO」を抽出
                labels.append(image.split("faces/target_")[1].split("-")[0].replace("reversed_", ""))
            else:
                print("skip not rgb3")
    print("converted.")
    return (datas, labels)


def scatterData(datas, labels):
    """
    YES NO頒布図を描画する
    """
    data = np.array(datas)
    y = np.where(np.array(labels) == 'YES', 1, 0)

    # plot
    pca = PCA(n_components=2)
    X = pca.fit_transform(data)
    df = pd.DataFrame({"x": X[:, 0],
                       "y": X[:, 1],
                       "label": np.where(y == 1, 'YES', 'NO')})
    colors = ['red', 'yellow']
    for label, color in zip(df['label'].unique(), colors):
        mask = df['label'] == label
        pl.scatter(df[mask]['x'], df[mask]['y'], c=color, label=label)


def learn(datas, labels):
    """
    データを学習
    """
    clf = svm.LinearSVC()
    clf.fit(datas, labels)
    joblib.dump(clf, "pkls/beauty.pkl")
    print("learned.")

if __name__ == '__main__':
    datas, labels = getDatas()
    print(len(datas), len(labels))
    scatterData(datas, labels)
    learn(datas, labels)
