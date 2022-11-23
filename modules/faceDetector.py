import cv2
import mediapipe as mp
import numpy as np


class FaceDetector():
    def __init__(self, minDetConf = 0.5):
        self.mpFaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.faceDetection = self.mpFaceDetection.FaceDetection(minDetConf)
        self.mpFaceMesh = mp.solutions.face_mesh
        self.mpFaceMeshConnections = mp.solutions.face_mesh_connections
        self.faceMesh = self.mpFaceMesh.FaceMesh(
            max_num_faces=2,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)
        self.drawSpec = self.mpDraw.DrawingSpec(thickness=1, circle_radius=1)
        self.results = None
        self.curretnFrame = None

    def findFaces(self, img, d_square=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgRGB.flags.writeable = False
        results = self.faceDetection.process(imgRGB)

        bboxs = []
        if results.detections:
            for face_id, detection in enumerate(results.detections):
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, ic = img.shape
                bbox =  int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                        int(bboxC.width * iw), int(bboxC.height * ih)

                if d_square: 
                    self.squareDraw(img, bbox)
                    cv2.putText(img, 
                        f'{ int(detection.score[0]*100) }%', 
                        (bbox[0], bbox[1]-20),
                        cv2.FONT_HERSHEY_PLAIN, 
                        2, (255, 0, 255), 2)
                bboxs.append([bbox, detection.score])

        return bboxs

    def get_results(self,img):
        self.curretnFrame = img
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   
        self.results = self.faceMesh.process(imgRGB)
        if self.results:
            return self.results

    def squareDraw(self, img, bbox, l = 20, refctangle_t = 1, corner_t = 5):
        x, y, w, h = bbox #first point, bridging point
        x1, y1 = x+w, y+h #bottom right point
        corner_color_y =  (0,225,128)
        corner_color_x =  (0,225,128)
        rectangle_color = (255,0,255)

        cv2.rectangle(img, bbox, rectangle_color, refctangle_t)
        cv2.line(img, (x,y), (x+l,y), corner_color_x, corner_t )
        cv2.line(img, (x,y), (x,y+l), corner_color_y, corner_t )

        cv2.line(img, (x1,y), (x1-l,y), corner_color_x, corner_t )
        cv2.line(img, (x1,y), (x1,y+l), corner_color_y, corner_t )

        cv2.line(img, (x,y1), (x+l,y1), corner_color_x, corner_t )
        cv2.line(img, (x,y1), (x,y1-l), corner_color_y, corner_t )

        cv2.line(img, (x1,y1), (x1-l,y1), corner_color_x, corner_t )
        cv2.line(img, (x1,y1), (x1,y1-l), corner_color_y, corner_t )
    
    def facemeshing(self, results, img, draw = True):
        if self.results is None:
            print("run get_results before facemeshing")
            return
        faces = []
        face = {}
        if results.multi_face_landmarks:
            for faceLms in results.multi_face_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, faceLms, self.mpFaceMesh.FACEMESH_CONTOURS,
                                            self.drawSpec,self.drawSpec )

                for id, lm in enumerate(faceLms.landmark):
                    ih, iw, ic = img.shape
                    x,y = int(lm.x*iw), int(lm.y*ih)
                    #faces.append({id: [x,y]}) 
                    face[id]= [x,y]     ## adds every 478 landmark with its coordetates, for each face in list
                faces.append(face)
            return faces ## 1 or 2 faces in list
    
    def landmarksDetection(self, img, results, shape, draw=False):
        img_height, img_width = shape
        if results.multi_face_landmarks:
            mesh_coord = [(int(point.x * img_width), int(point.y * img_height)) for point in results.multi_face_landmarks[0].landmark]
            if draw :
                [cv2.circle(img, p, 2, (0,255,0), -1) for p in mesh_coord]

        # returning the list of tuples for each landmarks 
            return mesh_coord
        else:
            return None
