# -*- coding: utf-8 -*-

import os
import cv2


def main():
    """
    images下の美人画像一覧を読み出し、faces下に顔画像検出した結果を保存する
    """
    for image_path, _, files in os.walk('images'):
        if len(_):
            continue
        face_path = image_path.replace('images', 'faces')
        if not os.path.exists(face_path): os.makedirs(face_path)
        for filename in files:
            if not filename.startswith('.'):
                save_faces(image_path, face_path, filename)


def save_faces(image_path, face_path, filename):
    """
    真正面顔判定用のOpenCVファイルを使って、顔画像を切り出す
    """
    print(image_path, face_path, filename)
    # カスケード分類器を読み込む(正面顔の検出分類器)
    cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_alt2.xml')
    image = cv2.imread('{}/{}'.format(image_path, filename))
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(gray_image)
    # Extract when just one face is detected
    if (len(faces) == 1):
        (x, y, w, h) = faces[0]
        image = image[y:y+h, x:x+w]
        image = cv2.resize(image, (100, 100))
        cv2.imwrite('{}/{}'.format(face_path, filename), image)
    else:
        cv2.imwrite('{}/{}'.format(face_path + "/misses", filename), image)
        print("skipped.")


if __name__ == '__main__':
    main()
