from modules.faceDetector import FaceDetector
from modules.units.eyesUnit import EyeUnit
from modules.units.mouthUnit import MouthUnit
from modules.units.headUnit import HeadUnit
from modules.units.attentionUnit import AttentionUnit
import time

class Predictor():
    def __init__(self):
        # objects
        self.faceDetector = FaceDetector()
        self.eyeUnit = EyeUnit()
        self.mouthUnit = MouthUnit()
        self.headUnit = HeadUnit()
        self.attentionUnit = AttentionUnit()

        # Counters
        self.blinkCount = 0
        self.yawnCount = 0
        
        # counter for attention
        self.lostFocusCount = 0
        self.lostFocusDuration = 0
        self.faceNotPresentDuration = 0

        self.atencion = 50
        self.prevYawn = 0
        self.prev_lostfocus = 0
        self.prev_fnp = 0
        self.att_prev = 0
        self.cont_prev = 0
   

        # States
        self.yawning = False
        self.eyeClosed = False
        self.lostFocus = False

    def attention_calc(self, yawnCount):
        lostFocusCount = self.lostFocusCount 
        lostFocusDuration = self.lostFocusDuration 
        faceNotPresentDuration = self.faceNotPresentDuration 
        atencion = self.atencion 
        prevYawn = self.prevYawn 
        prev_lostfocus = self.prev_lostfocus 
        prev_fnp = self.prev_fnp 
        att_prev = self.att_prev 
        cont_prev = self.cont_prev 

        if time.time() - cont_prev > 2:
            cont_prev = time.time()
            counter_attention = 0
            
            if prevYawn - yawnCount != 0:
                prevYawn = yawnCount
                counter_attention = counter_attention + 4*yawnCount
            else:
                pass
            if prev_lostfocus - lostFocusCount != 0:
                prev_lostfocus = lostFocusCount
                counter_attention = counter_attention + round(lostFocusCount*(lostFocusDuration))
            else:
                pass
            if prev_fnp - faceNotPresentDuration != 0:
                prev_fnp = faceNotPresentDuration
                counter_attention += round(faceNotPresentDuration)
            else:
                pass
            atencion = atencion - counter_attention
            
        if time.time() - att_prev > 5:
            att_prev = time.time()
            if prevYawn - yawnCount == 0:
                atencion += 1
            if prev_lostfocus - lostFocusCount == 0:
                atencion += 1
            
        if atencion > 60:
            atencion = 60
        if atencion < 0:
            atencion = 0

        return atencion

    def get_predictions(self, frame_input):

        frame = frame_input
        frame_shape = frame.shape[:2]

        # Características del frame:
        frame_shape = frame.shape[:2]
        ## resultados de landmarks en rostros. Los resultados deben utilizarse para head_pose y mesh_list.
        results = self.faceDetector.get_results(frame)
        mesh_list = self.faceDetector.landmarksDetection(frame, results, frame_shape, draw=False)
        
        if mesh_list is not None: # None cuando no detecta rostro.
        # BLINK DETECTION
            eye_ratio = self.eyeUnit.blinking_ratio(frame, mesh_list, draw= True )
            self.eyeClosed, self.blinkCount = blink_detection(eye_ratio, self.blinkCount, self.eyeClosed)

        # YAWN DETECTION
            mouth_ratio = self.mouthUnit.mouth_aspect_ratio(frame, mesh_list, draw=True)
            self.yawning, self.yawnCount = yawn_detection(mouth_ratio, self.yawnCount, self.yawning)
            
        # HEAD POSE DETECTION
            if results is not None:
                head_pose, x_angle, y_angle, z_angle = self.headUnit.head_tilting(results, frame, d_line = True)

        # ATTENTION LEVEL
        atencion = self.attention_calc(self.yawnCount)

        states = {
            'blinks': self.blinkCount,
            'yawns' : self.yawnCount,
            'atention': atencion
        }
        return states

def yawn_detection(mouth_ratio, yawnCount, yawning):
    if mouth_ratio < 0.95:
        yawning = True
    if yawning and mouth_ratio > 4.00:
       yawnCount += 1
       yawning = False
    return yawning, yawnCount

def blink_detection(eye_ratio, blink_count, eye_closed):
    if eye_ratio < 5: # Si se cierra el ojo,
        eye_closed = True
    if eye_ratio > 5 and eye_closed: # y luego se abre el ojo:
        blink_count += 1   # Cuenta como pestañeo.
        eye_closed = False
    return eye_closed, blink_count



