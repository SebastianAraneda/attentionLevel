import time

class AttentionUnit():
    pass

    def __init__(self):
        # Current counters:
        self.lostFocusCount = 0
        self.yawnCount = 0
        self.faceNotPresentDuration = 0
        
        # Prev counters
        self.prev_lostfocus = 0
        self.prevYawn = 0
        self.prev_fnp = 0

        # Attention default
        self.attentionDefault = 50
        self.attention = 0
        pass

    def attention_level(self):
        if time.time() - cont_prev > 2:
            cont_prev = time.time()
            counter_attention = 0
            
            if self.prevYawn - self.yawnCount != 0:
                self.prevYawn = self.yawnCount
                counter_attention = counter_attention + 4*self.yawnCount
            else:
                pass
            if self.prev_lostfocus - self.lostFocusCount != 0:
                self.prev_lostfocus = self.lostFocusCount
                counter_attention = counter_attention + round(self.lostFocusCount*(self.lostFocusDuration))
            else:
                pass
            if self.prev_fnp - self.faceNotPresentDuration != 0:
                self.prev_fnp = self.faceNotPresentDuration
                counter_attention += round(self.faceNotPresentDuration)
            else: 
                pass

            self.attention = self.attentionDefault - counter_attention
            atencion = self.attention
            
        if time.time() - att_prev > 5:
            att_prev = time.time()
            if self.prevYawn - self.yawnCount == 0:
                atencion += 1
            if self.prev_lostfocus - self.lostFocusCount == 0:
                atencion += 1
            
        if atencion > 60:
            atencion = 60
        if atencion < 0:
            atencion = 0
        
        self.attention = atencion
        return atencion