# -*- coding: utf-8 -*-

"""
女優の画像素材を増やすために、すでにあるfaces下の画像を反転させ、
画像素材として扱わせることで、二倍の素材が手に入る
"""
import os
import cv2


def main(targetDir):
    for path, _, files in os.walk(targetDir):
        for file in files: 
            if not file.startswith('.'):
                print(path + '/' + file)
                img = cv2.imread((path + '/' + file), cv2.IMREAD_COLOR)
                reversed_y_img = cv2.flip(img, 1)
                cv2.imwrite(path + '/' + file.replace('target_', 'target_reversed_'), reversed_y_img)

if __name__ == '__main__':
    main("faces")
