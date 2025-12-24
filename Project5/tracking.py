import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture("video.mp4")

size = (640,384)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out =cv2.VideoWriter("media.mp4",fourcc, 60.0, size)

while True:
    ret, frame = cap.read()
    if not ret: break
    frame = cv2.resize(frame,(640,384))
    results = model.track(frame, persist = True, device = 0, classes = [0], conf = 0.3)
    if results[0].boxes.id is not None:  
        track_ids = results[0].boxes.id.cpu().numpy().astype(int)
        for box,track_id in zip(results[0].boxes,track_ids):
        
            x1, y1, x2, y2 = box.xyxy[0]
            cls = "P"
        
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, f"{cls} : {track_id} ", (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    cv2.imshow("Human Tracking",frame)
    out.write(frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
out.release()
cap.release()
cv2.destroyAllWindows()
