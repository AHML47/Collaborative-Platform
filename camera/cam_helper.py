from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder, Quality
from picamera2.outputs import CircularOutput
from typing import Optional


class CameraHelper() :
    global output
    global cam
    output = CircularOutput()
    def __init__(self,cam_config : Optional[dict] = None):
        try:
            self.cam = Picamera2()
            if not cam_config:
                self.cam.configure(self.cam.create_preview_configuration(main={"size": (640, 480)}))
            else:
                self.cam.configure(cam_config)

        except Exception as e :
            print (f"Error creating Camera Helper : {e}")
    
    def start_preview(self,lite):
        if not lite :
            self.cam.start_preview(Preview.QTGL)
        self.cam.start()


    def conf (self,cam_config) :
        self.cam.configure(cam_config)


    def take_picture(self,name):
        self.cam.capture_file(name + ".jpg")

    def start(self):
        self.cam.start()

    def capture_arrays(self):
        return self.cam.capture_array()

    def set_control(self, param):
        self.cam.set_controls(param)

    def start_recording(self, filename):

        try:
            self.cam.stop()
            self.cam.configure(self.cam.create_video_configuration())
            self.cam.start()
            output.fileoutput = filename
            output.start()
            print(f"Recording started: {filename}")
        except Exception as e:
            print(f"Error starting recording: {e}")
    def strop(self):
        self.cam.stop()
    def stop_recording(self):

        try:
            output.stop()
            print("Recording stopped.")
        except Exception as e:
            print(f"Error stopping recording: {e}")


