import cv2
import numpy as np

def region_of_interest(img, vertices):
    # 1. Create a black mask (same size as image)
    mask = np.zeros_like(img)
    
    # 2. Fill the "triangle" area with white (255)
    match_mask_color = 255
    cv2.fillPoly(mask, vertices, match_mask_color)
    
    # 3. Keep only the edges inside that triangle
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

def draw_lines(img, lines, color=[255, 0, 0], thickness=5):
    # Create a blank image to draw lines on
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_img, (x1, y1), (x2, y2), color, thickness)
    
    # Merge the line image with the original image
    return cv2.addWeighted(img, 0.8, line_img, 1.0, 0.0)

# Load Video
cap = cv2.VideoCapture("solidWhiteRight.mp4")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
    
    height = frame.shape[0]
    width = frame.shape[1]

    # A. PRE-PROCESSING
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    
    # B. MASKING (The Triangle)
    # These coordinates define the "Road Area"
    # (Bottom-Left, Top-Middle, Bottom-Right)
    region_vertices = [
        (0, height), 
        (width / 2, height / 1.75), 
        (width, height)
    ]
    
    # We need integer points for OpenCV
    region_vertices = np.array([region_vertices], np.int32)
    
    cropped_edges = region_of_interest(edges, region_vertices)
    
    # C. HOUGH TRANSFORM (Connect the dots!)
    # rho=2 (precision), theta=pi/180 (1 degree), threshold=50 (min votes)
    # min_line_len=40 (ignore short specs), max_line_gap=100 (connect dashed lines)
    lines = cv2.HoughLinesP(cropped_edges, 
                            rho=2, 
                            theta=np.pi/180, 
                            threshold=50, 
                            lines=np.array([]), 
                            minLineLength=40, 
                            maxLineGap=100)
    
    # D. DRAW RESULT
    image_with_lines = draw_lines(frame, lines)
    
    cv2.imshow("Lane Detector", image_with_lines)
    
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
