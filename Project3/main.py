import cv2
import numpy as np
import tensorflow as tf

model = tf.keras.models.load_model('traffic_signal.h5')
classes = {0: 'GREEN', 1: 'RED', 2: 'YELLOW'}

cap = cv2.VideoCapture("Video.mp4") 

while True:
    ret, frame = cap.read()
    if not ret: break
    frame = cv2.resize(frame, (640, 480))

    height, width, _ = frame.shape
    
    roi_height = int(height * 0.6)
    frame_roi = frame[0:roi_height, 0:width]
    
    hsv = cv2.cvtColor(frame_roi, cv2.COLOR_BGR2HSV)
    
    mask1 = cv2.inRange(hsv, (0, 120, 120), (10, 255, 255))
    mask2 = cv2.inRange(hsv, (170, 120, 120), (180, 255, 255))
    mask_r = mask1 | mask2
    
    mask_g = cv2.inRange(hsv, (50, 100, 100), (90, 255, 255))
    
    mask_y = cv2.inRange(hsv, (20, 100, 100), (35, 255, 255))
    
    mask = mask_r | mask_g | mask_y
    
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=2)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        area = cv2.contourArea(contour)
        
        if area > 200: 
            x, y, w, h = cv2.boundingRect(contour)
            
            aspect_ratio = float(w)/h
            if 0.6 < aspect_ratio < 1.4:
                
                bulb_img = frame_roi[y:y+h, x:x+w]
                
                try:
                    bulb_input = cv2.resize(bulb_img, (30, 30))
                    bulb_input = np.expand_dims(bulb_input, axis=0) / 255.0
                    
                    pred = model.predict(bulb_input, verbose=0)
                    idx = np.argmax(pred)
                    conf = np.max(pred)
                    
                    if conf > 0.80:
                        txt = classes[idx]
                        
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