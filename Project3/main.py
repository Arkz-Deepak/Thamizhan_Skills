import cv2
import numpy as np
import tensorflow as tf

# 1. Load Model
print("Loading Brain...")
model = tf.keras.models.load_model('traffic_signal.h5')
classes = {0: 'GREEN', 1: 'RED', 2: 'YELLOW'}

cap = cv2.VideoCapture("Video.mp4") # Or use 0 for webcam

while True:
    ret, frame = cap.read()
    if not ret: break
    frame = cv2.resize(frame, (640, 480))

    height, width, _ = frame.shape
    
    # FILTER 1: IGNORE THE GROUND
    # We only look at the top 60% of the screen
    # ROI = Region of Interest
    roi_height = int(height * 0.6)
    frame_roi = frame[0:roi_height, 0:width]
    
    # Convert ROI to HSV
    hsv = cv2.cvtColor(frame_roi, cv2.COLOR_BGR2HSV)
    
    # FILTER 2: STRICTER COLOR RANGES
    # We increase 'S' and 'V' (last two numbers) to 100+
    # This means "Only look at COLORFUL and BRIGHT things"
    
    # RED (0-10) and (170-180)
    mask1 = cv2.inRange(hsv, (0, 120, 120), (10, 255, 255))
    mask2 = cv2.inRange(hsv, (170, 120, 120), (180, 255, 255))
    mask_r = mask1 | mask2
    
    # GREEN (Shifted to 60-90 to avoid trees)
    mask_g = cv2.inRange(hsv, (50, 100, 100), (90, 255, 255))
    
    # YELLOW (Strict Orange-Yellow)
    mask_y = cv2.inRange(hsv, (20, 100, 100), (35, 255, 255))
    
    # Combine
    mask = mask_r | mask_g | mask_y
    
    # Clean up noise
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=2)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        area = cv2.contourArea(contour)
        
        # FILTER 3: SIZE CHECK
        if area > 200: 
            x, y, w, h = cv2.boundingRect(contour)
            
            # FILTER 4: SHAPE CHECK
            # We are detecting the BULB, which is roughly square/circle (1:1 ratio)
            # Not a long rectangle.
            aspect_ratio = float(w)/h
            if 0.6 < aspect_ratio < 1.4:
                
                # Cut out the bulb
                bulb_img = frame_roi[y:y+h, x:x+w]
                
                try:
                    # Preprocess for Brain
                    bulb_input = cv2.resize(bulb_img, (30, 30))
                    bulb_input = np.expand_dims(bulb_input, axis=0) / 255.0
                    
                    # Ask Brain
                    pred = model.predict(bulb_input, verbose=0)
                    idx = np.argmax(pred)
                    conf = np.max(pred)
                    
                    # High Confidence Only
                    if conf > 0.80:
                        txt = classes[idx]
                        
                        # Draw on original frame
                        color = (0, 255, 0)
                        if txt == 'RED': color = (0, 0, 255)
                        if txt == 'YELLOW': color = (0, 255, 255)
                        
                        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                        cv2.putText(frame, f"{txt} {int(conf*100)}%", (x, y-10), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                except:
                    pass

    cv2.imshow('Strict Detector', frame)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()