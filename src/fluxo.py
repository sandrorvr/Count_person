import numpy as np
import cv2
import time

def set_min_th(valor):
	pass
def set_min_gaus(valor):
	pass
def get_pos_mouse(evento,x,y,flag,param):
	global pos_mouse
	if evento == cv2.EVENT_LBUTTONDOWN:
		pos_mouse = np.append(pos_mouse,[[x,y]],axis=0)
			

cv2.namedWindow('controles')
cv2.namedWindow('frame')

cv2.createTrackbar('th_min','controles',50,255,set_min_th)
cv2.createTrackbar('gaus','controles',3,17,set_min_gaus)

flag = False


kernel = np.ones((5,5),np.uint8)
sub = cv2.createBackgroundSubtractorMOG2()
cap = cv2.VideoCapture("..\\videos\\1.mp4")

pos_mouse = np.empty((0,2), dtype=np.int32)
cv2.setMouseCallback('frame', get_pos_mouse)
while True:
	rec,frame = cap.read()
	v = cv2.getTrackbarPos('th_min','controles')
	g = cv2.getTrackbarPos('gaus','controles')
	if g%2 ==0:
		g=g+1
	#print(v)
	if rec:
		
		frame = cv2.resize(frame,(int(frame.shape[1]*0.5),int(frame.shape[0]*0.5)),interpolation = cv2.INTER_AREA)
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		frame = cv2.GaussianBlur(frame,(g,g),0)
		subtracion = sub.apply(frame)
		_, th = cv2.threshold(frame, v, 255, cv2.THRESH_BINARY_INV)
		dilatacao = cv2.dilate(th, kernel, iterations=1)
		
		if len(pos_mouse):
			cv2.polylines(frame,[pos_mouse],True,(0,255,255))

			croped = dilatacao
			#pos_mouse = pos_mouse - pos_mouse.min(axis=0)
			mask = np.zeros(croped.shape[:2], np.uint8)
			cv2.drawContours(mask,[pos_mouse],-1,(255,255,255),-1, cv2.LINE_AA)
			corte = cv2.bitwise_and(croped, croped, mask=mask)
			cv2.imshow("corte", corte)

		cv2.imshow("frameD", dilatacao)
		cv2.imshow("frame", frame)

	else:
		break

	#if cv2.waitKey(40) & 0xFF == ord('q'):
	#	break
	key = cv2.waitKey(70)
	if key == ord('q'):
		break
	elif key == ord('p'):
		while not flag:
			y = cv2.waitKey(10)
			if y == ord('p'):
				break

cap.release()
cv2.destroyAllWindows()
'''

import numpy as np
import cv2

img = cv2.imread("..\\videos\\x.png")
pts = np.array([[10,150],[150,150],[150,100],[10,100]])

## (1) Crop the bounding rect
rect = cv2.boundingRect(pts)
x,y,w,h = rect

croped = img[y:y+h, x:x+w].copy()

## (2) make mask
pts = pts - pts.min(axis=0)

mask = np.zeros(croped.shape[:2], np.uint8)

#cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)

## (3) do bit-op
#dst = cv2.bitwise_and(croped, croped, mask=mask)

## (4) add the white background
bg = np.ones_like(croped, np.uint8)*255
cv2.bitwise_not(bg,bg, mask=mask)
#dst2 = bg+ dst


#cv2.imwrite("croped.png", croped)
#cv2.imwrite("mask.png", mask)
#cv2.imwrite("dst.png", dst)
#cv2.imwrite("dst2.png", dst2)

cv2.imshow("frame", mask)
cv2.waitKey(0)
cv2.destroyAllWindows()'''