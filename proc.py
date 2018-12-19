#!/usr/bin/env python3

import cv2
import numpy as np

def detect_box(cap):
    # Bir kare al
    ret, capture = cap.read()
    # Gürültü kaldırma için gerekli kerneller
    kernel = np.ones((9,9),np.uint8)
    kernel2 = np.ones((13,13),np.uint8)
    if ret:
        # BGR'yi HSV'ye çevir
        hsv = cv2.cvtColor(capture, cv2.COLOR_BGR2HSV)
        # Sarı renk aralığı
        lower_yellow = np.array([15,40,40])
        upper_yellow = np.array([40,255,255])
        # Sarı renk filtresi
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        # Filtreyi yumuşat(blur)
        blur = cv2.blur(mask, (3, 3))
        _, result = cv2.threshold(blur,127,255,cv2.THRESH_BINARY)
        # Arkaplandaki beyaz noktaları ve cisim üzerindeki siyah noktaları yok et
        result = cv2.morphologyEx(result, cv2.MORPH_OPEN, kernel)
        result = cv2.morphologyEx(result, cv2.MORPH_CLOSE, kernel2)
        # Kenar ve köşe bul
        im2, contours, hierarchy = cv2.findContours(result,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        try:
            #Eğer kontur geldiyse dikdörtgen içine al
            cnt = contours[0]
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(capture,(x,y),(x+w,y+h),(0,255,0),2)
        except IndexError:
            contours = None

        return capture,result,contours
    else:
        return None, None, None


def find_centroids(contours):
    cnt = contours[0]
    # X ve Y eksenlerinde ağırlık merkezi bul
    x,y,w,h = cv2.boundingRect(cnt)
    return x+(w/2),y+(h/2)

def area_ratio(contours):
    try:
        cnt = contours[0]
        x,y,w,h = cv2.boundingRect(cnt)
    except TypeError:
        w = 0
        h = 0
    screen_area = 640*480
    return (w*h)/screen_area

def box_angle(contours):
    if type(contours) == type(None):
        return 0
    else:
        cx, cy = find_centroids(contours)
        ppd = 640/120
        angle = (cx/ppd)-60
        return angle

if __name__ == "__main__":
    cam = cv2.VideoCapture(0)

    while cam.isOpened():
        capture,result,contours = detect_box(cam)
        if type(capture) == type(None):
            print('Görüntü yok!')

        else:
            cv2.imshow('Image',capture)
            cv2.imshow('Filter',result)
            print('Gerekli açı:' + str(box_angle(contours)))
            print('Alanlar oranı:' + str(area_ratio(contours)))

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()


