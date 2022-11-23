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

