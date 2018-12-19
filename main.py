from comm import *
from proc import *
import cv2
import numpy as np
from networktables import NetworkTables

if __name__ == '__main__':
    print('Robota bağlanıyor')
    cam = get_robot_camera('10.69.85.2')
    proc_table = NetworkTables.getTable('imgproc')
    angle = proc_table.getEntry('angle')
    ratio = proc_table.getEntry('area ratio')
    print('Bağlantı başarılı')

    while cam.isOpened():
        capture,result,contours = detect_box(cam)
        if type(capture) == type(None):
            print('Görüntü yok!')

        else:
            cv2.imshow('Image',capture)
            cv2.imshow('Filter',result)
            ang = box_angle(contours)
            ra = area_ratio(contours)
            print('Gerekli açı:' + str(ang))
            angle.setDouble(float(ang))
            print('Alanlar oranı:' + str(ra))
            ratio.setDouble(float(ra))

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()
