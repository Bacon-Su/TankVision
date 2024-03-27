import cv2
import numpy as np
import setting

f = 254.8
baseboardh = 250
setting.targeth//2
h1 = baseboardh*f/(setting.targeth//2-baseboardh)
patternsize = 21 #cm
pc_ratio = h1/patternsize #pixel : cm

if __name__ == "__main__":
    print(pc_ratio) 