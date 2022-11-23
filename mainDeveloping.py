from modules.faceDetector import FaceDetector, cv2
from modules.units.eyesUnit import EyeUnit
from modules.units.mouthUnit import MouthUnit
from modules.units.headUnit import HeadUnit
from modules.units.attentionUnit import AttentionUnit
from modules.utils import averageFPS
from modules.predictors import yawn_detection, blink_detection

faceDetector = FaceDetector()
eyeUnit = EyeUnit()
mouthUnit = MouthUnit()
headUnit = HeadUnit()
attentionUnit = AttentionUnit()
cap = cv2.VideoCapture(0)

# counters:
blinkCount = 0
yawnCount = 0
fps, pTime, frame_counter = 0,0,0

lostFocusCount = 0
lostFocusDuration = 0
focusTimer = None

# states
yawning = False
eyeClosed = False
lostFocus = False
eye_closed_frames = 0

# optional drawing:
draw_eyes_ratio = True
draw_mouth_ratio = True
draw_head_pose = True
draw_face_square = True

while True:
    success, frame = cap.read()
    # FPS
    fps, pTime, frame_counter = averageFPS(frame,frame_counter, pTime, fps)
    cv2.putText(frame, f'FPS: {int(fps)}', (80,50), cv2.FONT_HERSHEY_PLAIN, 3, (0,255, 255), 2)

    # Análisis/pipeline
    if success: ## si captura imagen.
        ## cuadro de rostro
        faces = faceDetector.findFaces(frame, d_square=True)
        if not len(faces) == 0: 
            for rostro in faces[0][0]:
                x, y, w, h = faces[0][0] #first point, bridging point
                x1, y1 = x+w, y+h #bottom right point
                cv2.rectangle(frame,(x, y),(x1, y1), (0,255,0), 1)
        else:
            pass # code en caso de no detectar rostros
        
        # Características del frame:
        frame_shape = frame.shape[:2]
        ## resultados de landmarks en rostros. Los resultados deben utilizarse para head_pose y mesh_list.
        results = faceDetector.get_results(frame)
        mesh_list = faceDetector.landmarksDetection(frame, results, frame_shape, draw=False)
        head_pose, x_angle, y_angle, z_angle = headUnit.head_tilting(results, frame, d_line = True)

        # BLINK DETECTION
        if mesh_list is not None: # None cuando no detecta rostro.
            eye_ratio = eyeUnit.blinking_ratio(frame, mesh_list, draw= True )
            # Blink counter:
            eyeClosed, blinkCount = blink_detection(eye_ratio, blinkCount, eyeClosed)
            if draw_eyes_ratio:
                cv2.putText(frame, f'Total Blinks: {blinkCount}', (50, 150), 3, 0.6, (0,255,255), 2)
        
        # YAWN DETECTION
        if mesh_list is not None: # None cuando no detecta rostro.
            mouth_ratio = mouthUnit.mouth_aspect_ratio(frame, mesh_list, draw=True)
            yawning, yawnCount = yawn_detection(mouth_ratio, yawnCount, yawning)
            
            if draw_mouth_ratio:
                cv2.putText(frame, f'Total Blinks: {yawnCount}', (50, 170), 3, 0.6, (0,255,255), 2)

        # HEAD POSE DETECTION
        if mesh_list is not None: # None cuando no detecta rostro.
            if draw_head_pose:
                cv2.putText(frame, f'Head Pose: {head_pose}', (50, 200), 3, 0.6, (0,255,255), 2)

        # ATTENTION LEVEL
        pass


    cv2.imshow('face',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release() 
        break
cv2.destroyAllWindows()