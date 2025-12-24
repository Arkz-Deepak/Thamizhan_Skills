import cv2
import mediapipe as mp
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class TurtleController(Node):
    
    def __init__(self):
        super().__init__("my_node")
        self.publisher_ = self.create_publisher(Twist,"/cmd_vel",10)
        self.get_logger().info("Activating Turtle Controller.............")

    def sendCommands(self,action):
        msg = Twist()

        if action == "FORWARD":
            msg.linear.x = 0.5
            msg.angular.z = 0.0
        elif action == "REVERSE":
            msg.linear.x = -0.5
            msg.angular.z = 0.0
        elif action == "LEFT":
            msg.linear.x = 0.0
            msg.angular.z = 0.5
        elif action == "RIGHT":
            msg.linear.x = 0.0
            msg.angular.z = -0.5
        elif action == "STOP":
            msg.linear.x = 0.0
            msg.angular.z =0.0
            
        self.publisher_.publish(msg)

        
def count_finger(hand_landmarks):
    finger = []
    tip_ids = [8,12,16,20]
    for tip_id in tip_ids:
        if hand_landmarks.landmark[tip_id].y < hand_landmarks.landmark[tip_id-2].y:
            finger.append(1)
        else:
            finger.append(0)
    return(finger.count(1))

    
def main(args = None):
    rclpy.init(args=args)
    node = TurtleController()

    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    hands = mp_hands.Hands()
    cap = cv2.VideoCapture("/mnt/c/Projects/Video.mp4")
    try:
        while True:
            ret, frame = cap.read()
            if not ret: break
            frame = cv2.cvtColor(cv2.flip(frame,1),cv2.COLOR_BGR2RGB)
            results = hands.process(frame)

            command = "STOP"
        
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    count = count_finger(hand_landmarks)
                    if count == 1: command = "FORWARD"
                    elif count == 2: command = "REVERSE"
                    elif count == 3: command = "LEFT"
                    elif count == 4: command = "RIGHT"
                    else: command = "STOP"
            node.sendCommands(command)
    except KeyboardInterrupt:
        pass
    finally:
        node.sendCommands("STOP")
        cap.release()
        cv2.destroyAllWindows()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
