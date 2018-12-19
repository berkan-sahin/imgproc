from networktables import NetworkTables
import cv2


def nt_init(ip):
    NetworkTables.initialize(server=ip)


def get_stream_link():
    cam_table = NetworkTables.getTable('CameraPublisher')
    sub_table = cam_table.getSubTable('USB Camera 0')
    a = sub_table.getEntry('streams').get()[0]
    return (a[5:] + '&type=mjpg')


def get_cv_stream():
    return cv2.VideoCapture(get_stream_link())

def get_robot_camera(ip):
    fail = True
    while fail:
        try:
            nt_init(ip)
            cap = get_cv_stream()
            fail = False
        except TypeError:
            fail = True

    return cap

if __name__ == "__main__":
    print('Robota bağlanıyor')
    cap = get_robot_camera('10.69.85.2')
    print('Bağlantı başarılı')
    while True:
        '''
        try:
            cap = get_cv_stream()
        except TypeError:
            nt_init('10.69.85.2')
            continue
        '''
        ret, frame = cap.read()
        #sjsj = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            exit(0)
