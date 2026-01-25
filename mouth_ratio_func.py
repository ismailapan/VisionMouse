import math

#78: Sol Köşe
#308: Sağ Köşe
#13: Üst Dudak
#14: Alt Dudak

MOUTH_ID = [78, 308, 13, 14]

def mouth_ratio(landmarks):
    p_left = landmarks[78]
    p_right = landmarks[308]
    h_dist = math.hypot(p_left.x - p_right.x, p_left.y - p_right.y)

    p_top = landmarks[13]
    p_bottom = landmarks[14]
    v_dist = math.hypot(p_top.x - p_bottom.x, p_top.y - p_bottom.y)

    if h_dist == 0:
        return 0
    
    return v_dist / h_dist