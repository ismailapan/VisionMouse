import math

LEFT_EYE = [33, 133, 160, 159, 144, 145]
RIGHT_EYE = [362, 263, 387, 386, 373, 374]

def eye_ratio(landmarks, indices):
    # Yatay Çizgi İçin
    p_left = landmarks[indices[0]]
    p_right = landmarks[indices[1]]

    #dikey-1 çizgi için 
    p_top1 = landmarks[indices[2]]
    p_bottom1 = landmarks[indices[4]]

    #dikey-2 çizgi için
    p_top2 = landmarks[indices[3]]
    p_bottom2 = landmarks[indices[5]]

    #öklid mesafeleri için
    h_dist = math.hypot(p_left.x - p_right.x, p_left.y - p_right.y)
    v_dist1 = math.hypot(p_top1.x - p_bottom1.x, p_top1.y - p_bottom1.y)
    v_dist2 = math.hypot(p_top2.x - p_bottom2.x, p_top2.y - p_bottom2.y)

    ratio = (v_dist1 + v_dist2) / (2*h_dist)

    return ratio