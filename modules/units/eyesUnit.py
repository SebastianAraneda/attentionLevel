import math
import cv2

class EyeUnit():
    def __init__(self):
        ## Landmarks keypoints:
        ## https://github.com/tensorflow/tfjs-models/blob/838611c02f51159afdd77469ce67f0e26b7bbb23/face-landmarks-detection/src/mediapipe-facemesh/keypoints.ts
        self.LEFT_EYE =[ 362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385,384, 398 ]
        self.RIGHT_EYE=[ 33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161 , 246 ] 
        self.LEFT_IRIS = [474, 475, 476, 477]
        self.RIGHT_IRIS = [469, 470, 471, 472]
        
        # Datos:
        self.blink_time = 1/10 # (segundos) duración de un parpadeo
        
        # Variables
        pass
    
    def blinking_ratio(self, img, landmarks, draw = False):
        # right eye
        rh_right = landmarks[self.RIGHT_EYE[0]]
        rh_left = landmarks[self.RIGHT_EYE[8]]
        rv_top = landmarks[self.RIGHT_EYE[12]]
        rv_bottom = landmarks[self.RIGHT_EYE[4]]

        right_h_distance = self.euclaidean_distance(rh_right, rh_left)
        right_v_distance = self.euclaidean_distance(rv_top, rv_bottom)

        # left eye
        lh_right = landmarks[self.LEFT_EYE[0]]
        lh_left = landmarks[self.LEFT_EYE[8]]
        lv_top = landmarks[self.LEFT_EYE[12]]
        lv_bottom = landmarks[self.LEFT_EYE[4]]

        lelf_h_distance = self.euclaidean_distance(lh_right, lh_left)
        left_v_distance = self.euclaidean_distance(lv_top, lv_bottom)

        if draw:
            cv2.line(img, rh_right,rh_left, (255,128,0)     , 2)
            cv2.line(img, rv_top,rv_bottom, (255,255,255)   , 2)
            cv2.line(img, lh_right, lh_left, (255,128,0), 2)
            cv2.line(img, lv_top, lv_bottom, (255,255,255), 2)
        
        right_ratio = (right_h_distance/right_v_distance)

        if left_v_distance == 0:
            left_v_distance = 0.000001
            print("... Left went zero!")
        left_ratio = (lelf_h_distance/left_v_distance)

        eyes_ratio = (right_ratio + left_ratio)/2
        return eyes_ratio

    def euclaidean_distance(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        return distance