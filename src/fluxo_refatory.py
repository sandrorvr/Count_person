import numpy as np
import cv2

class count_person():
    def __init__(self):
        self.url_video = '..\\videos\\people.mp4'
        self.cap = cv2.VideoCapture(self.url_video)
        self.kernel = np.ones((5,5),np.uint8)
        self.FLAG = False
        self.FLAG_LINE = False
        self.AJUST_MASK = False
        #cv2.namedWindow('frame') Depois apagar
        self.frame = None
        self.pos_mouse = np.empty((0,2), dtype=np.int32)

    def set_min_th(self,valor):
        pass
    def set_max_th(self,valor):
        pass
    def set_gaus(self,valor):
        pass
    def set_dilatation(self,valor):
        pass
    def save_config(self,valor):
        pass

    def set_tela_configuration(self):
        cv2.namedWindow('controles')
        cv2.createTrackbar('th_min','controles',50,255,self.set_min_th)
        cv2.createTrackbar('th_max','controles',255,255,self.set_max_th)
        cv2.createTrackbar('gaus','controles',3,20,self.set_gaus)
        cv2.createTrackbar('dilatation','controles',1,20,self.set_dilatation)
        cv2.createTrackbar('save','controles',0,1,self.save_config)
    def get_tela_configuration(self):
        self.config_mask = {}
        self.config_mask['th_min'] = cv2.getTrackbarPos('th_min','controles')
        self.config_mask['th_max'] = cv2.getTrackbarPos('th_max','controles')
        self.config_mask['gaus'] = cv2.getTrackbarPos('gaus','controles')
        if self.config_mask['gaus'] % 2 == 0:
            self.config_mask['gaus'] +=1
        self.config_mask['dilatation'] = cv2.getTrackbarPos('dilatation','controles')
        self.config_mask['save'] = cv2.getTrackbarPos('save','controles')
        return self.config_mask

    def create_point_line(self, evento, x, y, flag, params):
        global POS_XY1, POS_XY2
        if evento == cv2.EVENT_LBUTTONDOWN:
            #POS_XY = np.append(POS_XY,[[x,y]],axis=0)
            if POS_XY1 == None:
                POS_XY1 = (x,y)
            else:
                POS_XY2 = (x,y)
        elif evento == cv2.EVENT_RBUTTONDOWN:
            POS_XY1 = None
            POS_XY2 = None
    def get_pos_mouse(self,evento,x,y,flag,param):
        self.pos_mouse
        if evento == cv2.EVENT_LBUTTONDOWN:
            self.pos_mouse = np.append(self.pos_mouse,[[x,y]],axis=0)
            if len(self.pos_mouse) >= 4:
                self.FLAG_LINE = True
            #print(self.pos_mouse)
    def draw_line(self):
        cv2.polylines(self.frame,[self.pos_mouse],True,(0,0,255))

    def center(self, x, y, w, h):
        x1 = int(w / 2)
        y1 = int(h / 2)
        cx = x + x1
        cy = y + y1
        return cx,cy

    def resize_img(self,rate):
        self.frame = cv2.resize(self.frame,(int(self.frame.shape[1]*rate),int(self.frame.shape[0]*rate)),interpolation = cv2.INTER_AREA)
    def correct_image(self):
        if self.AJUST_MASK :
            self.config_mask = self.get_tela_configuration()
        else:
            self.config_mask = {'th_min':118, 'th_max':255, 'gaus':17, 'dilatation':1}
        
        self.img = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        self.img = cv2.GaussianBlur(self.img,(self.config_mask['gaus'],self.config_mask['gaus']),0)
        _, self.img = cv2.threshold(self.img, self.config_mask['th_min'], self.config_mask['th_max'], cv2.THRESH_BINARY_INV)
        self.img = cv2.dilate(self.img, self.kernel, iterations=self.config_mask['dilatation'])
        #print('shape={}'.format(self.img.shape))
        return self.img

    def point_is_in(self,point):
        self._max = list(point)
        self._min = list(point)
        for el in self.pos_mouse:
            if self._max[0] < el[0]:
                self._max[0] = el[0]
            if self._max[1] < el[1]:
                self._max[1] = el[1]
            if self._min[0] > el[0]:
                self._min[0] = el[0]
            if self._min[1] > el[1]:
                self._min[1] = el[1]
        
        if point[0] < self._max[0] and point[0] > self._min[0] and point[1] < self._max[1] and point[1] > self._min[1]:
            return True
        return False

    def detect_person(self,frame):
        self.centro = []
        self.contours, _ = cv2.findContours(frame, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        self.i = 0
        for cnt in self.contours:
            (self.x,self.y,self.w,self.h) = cv2.boundingRect(cnt)

            self.area = cv2.contourArea(cnt)
            
            if int(self.area) > 1 and self.FLAG_LINE:
                self.point_center = self.center(self.x, self.y, self.w, self.h)
                if len(self.centro)<=self.i:
                    self.centro.append([])
                if self.point_is_in(self.point_center):
                    self.centro[self.i].append(self.point_center)
                cv2.circle(self.frame, self.point_center, 4, (0, 0,255), -1)
                self.i += 1
        return self.centro
                
    def main(self):
        while True:
            self.rec, self.frame = self.cap.read()

            if self.rec:
                if len(self.pos_mouse):
                    self.draw_line()
                
                self.img_correct = self.correct_image()
                
                print(self.detect_person(self.img_correct))
                cv2.imshow('frame',self.frame)
                cv2.imshow('img_correct',self.img_correct)
                cv2.setMouseCallback('frame', self.get_pos_mouse)

                if self.get_tela_configuration().get('save') == 1:
                    print(self.get_tela_configuration())
                    print(self.pos_mouse)
                    break

                self.key = cv2.waitKey(120)
                if self.key == ord('q'):
                    break
                elif self.key == ord('p'):
                    self.set_tela_configuration()
                    self.AJUST_MASK = True
                    while not self.FLAG:
                        self.img_correct = self.correct_image()
                        cv2.imshow('frame',self.frame)
                        cv2.imshow('img_correct',self.img_correct)
                        self.y = cv2.waitKey(10)
                        if self.y == ord('p'):
                            break
            else:
                break
        self.cap.release()
        cv2.destroyAllWindows()


contdor = count_person()
contdor.main()