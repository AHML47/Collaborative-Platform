import os
from stat import filemode
import threading
from dotenv import load_dotenv, dotenv_values
import requests
import logging
import cv2


class LED() :
    def __init__(self, id,x,y,size):
        self.id = id
        self.x = x
        self.y = y
        self.color=(0,0,255)
        self.work=False
        load_dotenv()
        self.NODEMCU_URL = os.getenv("Node_API")

        self.log=logging.getLogger(__name__)
        file_h=logging.FileHandler(filename="LOGS/esp.log" )
        format_h=logging.Formatter('%(asctime)s - %(name) - %(levelname)s - %(message)s')
        file_h.setFormatter(format_h)
        self.log.addHandler(file_h)

        self.size = size
        self.status=False
        self.isIN=False
        self.off()


    def on(self):
        try:
            print("LED START ON")
            self.work=True
            response = requests.get(f"{self.NODEMCU_URL}/led?led{self.id}=on")
            if response.status_code == 200:
                print(f"LED {self.id} turned on: {response.text}")
                self.log.info(f"LED {self.id} turned on: {response.text}")
            else:
                self.log.error(f"Failed to turn on LED {self.id}: {response.status_code}")
            print("LED ON")
            self.work=False
        except Exception as e:
            self.log.error(f"Error while turning on LED {self.id}: {e}")

    def off(self):
        print("LED START OFF")
        try:
            self.work=True
            response = requests.get(f"{self.NODEMCU_URL}/led?led{self.id}=off")
            if response.status_code == 200:
                print(f"LED {self.id} turned off: {response.text}")
                self.log.info(f"LED {self.id} turned off: {response.text}")
            else:
                self.log.error(f"Failed to turn off LED {self.id}: {response.status_code}")
            print("LED OFF")
            self.work=False

        except Exception as e:
            self.log.error(f"Error while turning off LED {self.id}: {e}")

    def calculateXY(self):
        return (self.x-self.size//2,self.y-self.size//2),(self.x+self.size//2,self.y+self.size//2)

    def detect(self,frame,Nx,Ny):
        frame_height, frame_width, _ = frame.shape

        center_x = int(Nx * frame_width)
        center_y = int(Ny * frame_height)



        top_left, bottom_right = self.calculateXY()
        frame = self.draw(frame, "LED " + str(self.id))
        if top_left[0]<center_x<bottom_right[0] and top_left[1]<center_y<bottom_right[1] and not self.isIN:

            self.isIN=True
            print(
                f"x: {center_x}, y: {center_y} xA: {top_left[0]}, xB: {bottom_right[0]} yA: {top_left[1]}, yB: {bottom_right[1]}"
            )
            if not self.work :
                if self.status:
                    threading.Thread(target=self.off,daemon=True).start()
                    self.status = False
                    self.color=(0,0,255)


                else:
                    threading.Thread(target=self.on, daemon=True).start()
                    self.status = True
                    self.color=(0,255,0)

        else:
            self.isIN=False
        return frame


    def draw (self,frame,text):
        top_left, bottom_right = self.calculateXY()
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        color = (255, 255, 255)
        thickness = 2

        center_x, center_y = self.x,self.y

        (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)

        text_x = center_x - (text_width // 2)
        text_y = center_y + (text_height // 2)


        cv2.rectangle(frame, top_left, bottom_right, self.color, -1)
        cv2.putText(frame, text, (text_x, text_y), font, font_scale, color, thickness)
        return frame



