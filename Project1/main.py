import cv2
import numpy as np

def region_of_interest(img, vertices):

    mask = np.zeros_like(img)
    
    match_mask_color = 255
    cv2.fillPoly(mask, vertices, match_mask_color)
    
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

def draw_lines(img, lines, color=[255, 0, 0], thickness=5):
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_img, (x1, y1), (x2, y2), color, thickness)
    
    return cv2.addWeighted(img, 0.8, line_img, 1.0, 0.0)

cap = cv2.VideoCapture("solidWhiteRight.mp4")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
    
    height = frame.shape[0]
    width = frame.shape[1]

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    
    region_vertices = [
        (0, height), 
        (width / 2, height / 1.75), 
        (width, height)
    ]
    
    region_vertices = np.array([region_vertices], np.int32)
    
    cropped_edges = region_of_interest(edges, region_vertices)
    
    lines = cv2.HoughLinesP(cropped_edges, rho=2, theta=np.pi/180, threshold=50, lines=np.array([]), minLineLength=40, maxLineGap=100)
    
    image_with_lines = draw_lines(frame, lines)
    
    cv2.imshow("Lane Detector", image_with_lines)
    
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
