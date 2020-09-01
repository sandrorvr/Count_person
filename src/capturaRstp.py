#cap = cv2.VideoCapture('rtsp://admin:TDGCES@192.168.0.9:554/live/mpeg4')
from threading import Thread
from queue import Queue
import cv2 as cv
import time

class Camera:
    def __init__(self, user, password, ip):
        self.rtsp = 'rtsp://{}:{}@{}:554/live/mpeg4'.format(user, password, ip)
        self.fila = Queue()
        self.stop = False
        self.state_read = None
    def captura(self):
        self.cap = cv.VideoCapture(self.rtsp)
        while not self.stop:
            self.state_read, self.frame = self.cap.read()
            self.fila.put(self.frame)
        self.cap.release()
    def start(self):
        self.t = Thread(target=self.captura, daemon=True)
        self.t.start()

'''
camera = Camera('admin','TDGCES','192.168.0.9')
camera.start()
time.sleep(1)
frame = camera.fila.get()
print(frame.shape[0],frame.shape[1])
while True:
    frame = camera.fila.get()
    frame = cv.resize(frame,(int(frame.shape[1]*0.6),int(frame.shape[0]*0.6)),interpolation = cv.INTER_AREA)
    cv.imshow('frame', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        camera.stop = True
        break
cv.destroyAllWindows()'''




