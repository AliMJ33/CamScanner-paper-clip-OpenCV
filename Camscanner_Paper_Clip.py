import cv2
import numpy as np

def get_points(event, x, y, flags, param):
    global pts, clone
    if event == cv2.EVENT_LBUTTONDBLCLK:
        pts.append([x, y])
        cv2.circle(clone, (x,y), 10, (255, 0, 0), -1)

def perspective(image, points):
    (tl, tr, br, bl) = points
    width = np.sqrt(((tl[1] - tr[1])**2) + ((tl[0] - tr[0])**2))
    height = np.sqrt(((tl[1] - bl[1])**2) + ((tl[0] - tl[0])**2))

    dts = np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype= "float32")
    src = np.array([points], dtype= "float32")
    M = cv2.getPerspectiveTransform(src, dts)
    warped = cv2.warpPerspective(image, M, (int(width), int(height)))
    return warped


pts = []
clone = []
paper = cv2.imread("Paper.jpg")
clone = paper.copy()
cv2.namedWindow("Paper")

# Specify the corners of the paper in this order: 1) Top left corner. 2) Top right corner. 3) Bottom right corner. 4) Bottom left corner.
# You have to double click!
cv2.setMouseCallback("Paper", get_points)

while(1):
    cv2.imshow("Paper", clone)
    key = cv2.waitKey(1)
    if key == 27:
        break

    # Click "p" after specifying the corners to proceed.
    elif key == ord("p"):
        if len(pts) == 4:
            warped = perspective(paper, pts)
            cv2.imshow("Correct", warped)

cv2.destroyAllWindows()
