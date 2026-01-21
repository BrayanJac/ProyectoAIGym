import numpy as np

def angle(a, b, c):
    a, b, c = map(np.array, (a, b, c))
    ba = a - b
    bc = c - b
    cosang = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    return np.degrees(np.arccos(np.clip(cosang, -1, 1)))
