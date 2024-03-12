import cv2
import numpy as np

def remove_blackwindow(img):

    stitched = cv2.copyMakeBorder(img, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=(0, 0, 0))

    gray = cv2.cvtColor(stitched, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]
    mask = np.zeros(thresh.shape, dtype=np.uint8)

    if len(cnts) > 0:
        
        c = max(cnts, key=cv2.contourArea)
        
        x, y, w, h = cv2.boundingRect(c)
        
        cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)

    minRect = mask.copy()
    sub = mask.copy()

    while cv2.countNonZero(sub) > 0:
        minRect = cv2.erode(minRect, None)
        sub = cv2.subtract(minRect, thresh)

    edge_y, edge_x = np.where(minRect==255)
    bottom = min(edge_y)
    top = max(edge_y)
    height = top - bottom

    left = min(edge_x)
    right = max(edge_x)
    width = right - left

    result = cv2.bitwise_and(stitched, stitched, mask=minRect)
    result = result[bottom:bottom + height, left:left + width]
    return result
