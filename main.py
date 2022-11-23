from modules.predictor import Predictor
from modules.utils import averageFPS
import cv2

predictor = Predictor()
cap = cv2.VideoCapture(0)
fps, pTime, frame_counter = 0,0,0

while True:
    success, frame = cap.read()
    # FPS
    fps, pTime, frame_counter = averageFPS(frame,frame_counter, pTime, fps)

    states = predictor.get_predictions(frame)

    cv2.putText(frame, f'FPS: {int(fps)}', (80,50), cv2.FONT_HERSHEY_PLAIN, 2, (0,255, 255), 2)
    cv2.putText(frame, f"Attention level: { states['atention'] }", (50, 130), 3, 0.6, (0,255,255),1)
    cv2.putText(frame, f"Total yawns: { states['yawns'] } ", (50, 150), 3, 0.6, (0,255,255), 1)
    cv2.putText(frame, f"Total Blinks: { states['blinks'] }", (50, 170), 3, 0.6, (0,255,255), 1)


    cv2.imshow('face',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release() 
        break
cv2.destroyAllWindows()