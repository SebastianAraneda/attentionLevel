import math
import cv2

class MouthUnit():
    def __init__(self):
        ## Landmarks keypoints:
        ## https://github.com/tensorflow/tfjs-models/blob/838611c02f51159afdd77469ce67f0e26b7bbb23/face-landmarks-detection/src/mediapipe-facemesh/keypoints.ts
        self.lipsUpperOuter = [61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291]
        self.lipsLowerOuter = [146, 91, 181, 84, 17, 314, 405, 321, 375, 291]
        self.lipsUpperInner = [78, 191, 80, 81, 82, 13, 312, 311, 310, 415, 308]
        self.lipsLowerInner = [78, 95, 88, 178, 87, 14, 317, 402, 318, 324, 308]
        
        # Datos
        pass
        
        # Variables
        pass

    def mouth_aspect_ratio(self, img, landmarks, draw = False):
        # Horizontal key points
        mh_right = landmarks[self.lipsUpperInner[0]] # 78
        mh_left = landmarks[self.lipsUpperInner[-1]] # 308
        
        # Vertical key points
        # upeer lip
        mv_upper = landmarks[self.lipsUpperInner[5]] # 13
        # lower lip
        mv_lower = landmarks[self.lipsLowerInner[5]] # 14}

        h_distance = self.euclaidean_distance(mh_right, mh_left)
        v_distance = self.euclaidean_distance(mv_upper, mv_lower)

        if draw: 
            cv2.line(img, mh_right, mh_left, (255,128,0), 2)
            cv2.line(img, mv_upper, mv_lower,(255,0,128), 2)

        if v_distance == 0:
            v_distance = 0.000001
        mouth_ratio = (h_distance/v_distance)
        return mouth_ratio
    
    def euclaidean_distance(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        return distance