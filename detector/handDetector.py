import cv2
import mediapipe as mp
from queue import Queue
import math

class HandDetector:
    def __init__(self):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils

    def detect_raised_fingers(self,hand_landmarks,raised_fingers):
        """Detect raised fingers based on hand landmarks."""

        raised_fingers.queue.clear()
        fingers_tips = [8, 12, 16, 20]  # Index, Middle, Ring, Little finger tips
        fingers_joints = [6, 10, 14, 18]  # Corresponding joints
        thumb_tip = 4
        thumb_joint = 3

        for i, tip in enumerate(fingers_tips):
            joint = fingers_joints[i]
            if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[joint].y:
                raised_fingers.put(i + 1)


        if hand_landmarks.landmark[thumb_tip].x > hand_landmarks.landmark[thumb_joint].x:
            raised_fingers.put(0)

    def detect_capture(self, hand_landmarks,cap,x,y):
        """Detect the place of the capture based on hand landmarks."""




        fingers_tips = [8, 12, 16, 20]  # Index, Middle, Ring, Little finger tips

        thumb_tip = 4
        thumb_joint = 3
        Thumb = [hand_landmarks.landmark[thumb_tip].x , hand_landmarks.landmark[thumb_tip].y]

        for i, tip in enumerate(fingers_tips):

            Finger = [hand_landmarks.landmark[tip].x, hand_landmarks.landmark[tip].y]

            if math.dist(Thumb, Finger) < 0.08 :
                cap = True
                #print(f' {fingers_tips[i]} : {math.dist(Thumb, Finger)} | x : {hand_landmarks.landmark[tip].x} | y : {hand_landmarks.landmark[tip].y}' )
                x=hand_landmarks.landmark[tip].x
                y=hand_landmarks.landmark[tip].y
        return cap ,x,y






    def process_image(self,
                      frame,

                      cap,
                      x,
                      y,
                      raised_fingers=None
                      ):
        results = self.hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mpHands.HAND_CONNECTIONS
                )
                if raised_fingers is not None:
                    self.detect_raised_fingers(hand_landmarks,raised_fingers)
                cap ,x,y = self.detect_capture(hand_landmarks,cap,x,y)
        return frame ,cap,x,y

