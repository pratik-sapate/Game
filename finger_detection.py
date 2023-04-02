import cv2
import mediapipe as mp


class HandDetection:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5)

    def get_point_finger_coordinate(self, image):
        width, height, _ = image.shape
        results = self.hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)).multi_hand_landmarks
        left_x, left_y, right_x, right_y = None, None, None, None

        if results:
            if len(results) == 1:
                pinky_finger_mcp_x = results[0].landmark[self.mp_hands.HandLandmark.PINKY_MCP].x
                point_finger_mcp_x = results[0].landmark[self.mp_hands.HandLandmark.INDEX_FINGER_MCP].x
                if pinky_finger_mcp_x < point_finger_mcp_x:
                    left_x = results[0].landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].x * width
                    left_y = results[0].landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP
                             ].y * height
                else:
                    right_x = results[0].landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].x * width
                    right_y = results[0].landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].y * height
            elif len(results) == 2:
                pinky_finger_wrist1 = results[0].landmark[self.mp_hands.HandLandmark.WRIST].x
                point_finger_wrist2 = results[1].landmark[self.mp_hands.HandLandmark.WRIST].x
                if pinky_finger_wrist1 < point_finger_wrist2:
                    left_x = results[0].landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].x * width
                    left_y = results[0].landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].y * height
                    right_x = results[1].landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].x * width
                    right_y = results[1].landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].y * height
                else:
                    left_x = results[1].landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].x * width
                    left_y = results[1].landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].y * height
                    right_x = results[0].landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].x * width
                    right_y = results[0].landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].y * height

            self.mp_drawing.draw_landmarks(
                image,
                results[0],
                self.mp_hands.HAND_CONNECTIONS,
                self.mp_drawing_styles.get_default_hand_landmarks_style(),
                self.mp_drawing_styles.get_default_hand_connections_style())
            # print(len(results))
        if left_x != None and right_x == None:
            # left hand detected
            return (int(left_x), int(left_y)), None
        if left_x == None and right_x != None:
            # left hand detected
            return None, (int(right_x), int(right_y))
        elif left_x != None and right_x != None:
            # both hand detected
            return (int(left_x), int(left_y)), (int(right_x), int(right_y))
        else:
            # No hand detected
            return None, None

if __name__=="__main__":
    cam = cv2.VideoCapture(0)
    hand_capture = HandDetection()
    while True:
        ret, image = cam.read()
        left, right = hand_capture.get_point_finger_coordinate(image)
        print(left, right)
        cv2.imshow('image', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break