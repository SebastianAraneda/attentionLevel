import numpy as np
import cv2


class HeadUnit():
    def __init__(self):
        pass

    def head_tilting(self, results, img, d_landmarks = False, d_line = False):
        if results.multi_face_landmarks:
            text = None
            face3D = []
            face2D = []
            ih, iw, ic = img.shape
            for face_landmarks in results.multi_face_landmarks: #recorre cada rostro
                for idx, faceLm in enumerate(face_landmarks.landmark): #recorre cada lm de un rostro
                    if idx==33 or idx==263 or idx==1 or idx==61 or idx==291 or idx==199:
                        if idx==1:
                            nose2D = faceLm.x * iw, faceLm.y * ih
                            nose3D = faceLm.x * iw, faceLm.y * ih, faceLm.z * ic
                        x, y = int(faceLm.x * iw), int(faceLm.y * ih)
                        face2D.append([x,y])
                        face3D.append([x,y, faceLm.z * ic])
                # Convert to np array
                face_2D = np.array(face2D, dtype=np.float64)
                face_3D = np.array(face3D, dtype=np.float64)
                # camera matrix
                focal_length = 1 * iw

                #size = img.shape
                #center = (size[1]/2, size[0]/2)
                
                cam_matrix = np.array([ 
                                [focal_length,              0,      ih/2],
                                [           0,  focal_length ,      iw/2],
                                [           0,              0,         1]   ])
                # distortion parameters
                dist_matrix = np.zeros((4,1), dtype=np.float64)
                # solve PnP
                success, rot_vector, trans_vector =  cv2.solvePnP(face_3D, face_2D, cam_matrix , dist_matrix)
                
                # rotational matrix
                rmat, jac = cv2.Rodrigues(rot_vector)
                # get Angles
                angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)       
                # y rotation degree:
                x = angles[0] * 360
                y = angles[1] * 360
                z = angles[2] * 360
                # Head tilting:
                
                if y < -20:
                    text = 'tilting left'
                elif y > 20:
                    text = 'tilting right'
                elif x < -20:
                    text = 'tilting down'
                elif x > 20:
                    text = 'tilting up'
                else:
                    text = 'forward tilting'
                
                # Draw nose direction:
                if d_line: 
                    nose_3D_projection, jacobian = cv2.projectPoints(nose3D, rot_vector, trans_vector, cam_matrix, dist_matrix)
                    p1 = int(nose2D[0]), int(nose2D[1])
                    p2 = int(nose2D[0] + y*5),int(nose2D[1] - x*5)
                    cv2.line(img, p1, p2, (255,0,0), 3)
            return text, x, y, z
