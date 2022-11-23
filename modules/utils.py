import cv2
import numpy as np
import time

def draw_polyline(img, l):
    cv2.polylines(img, np.array([l], dtype=np.int32), True, (0,255,0), 1, cv2.LINE_AA)

def showFPS(img, pTime):
    cTime = time.time()
    fps = 1 / (cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20,50), cv2.FONT_HERSHEY_PLAIN, 3, (0,255, 255), 2)
    return pTime, cTime

def averageFPS(img, counter, pTime, prev_fps, interval = 1 ):
    counter +=1
    cTime = time.time()
    
    if cTime-pTime > interval:
        if (cTime-pTime) == 0:
            print("holo wololo")
        fps = int(counter/(cTime-pTime))
        counter = 0
        pTime = cTime
    else:
        fps = prev_fps
    return fps, pTime, counter

