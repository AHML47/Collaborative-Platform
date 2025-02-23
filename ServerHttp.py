from http.server import BaseHTTPRequestHandler, HTTPServer
import cv2
import numpy as np
import cgi
from object.Object_helper import ObjectHelper
#from Logger import Log
from detector.handDetector import HandDetector
from component.LED import LED

HOST = "0.0.0.0"
PORT = 8080
detector=HandDetector()

LED1 = LED(1,570,410,50)
LED2 = LED(2,500,410,50)
LED3 = LED(3,430,410,50)

shape = ObjectHelper(0,(0,255,0),'rectangle',50,100,100)
shape1 = ObjectHelper(0,(200,255,0),'rectangle',50,150,150)
shape2 = ObjectHelper(0,(20,255,200),'rectangle',50,200,200)
class MyHandler(BaseHTTPRequestHandler):
    def procces_the_frame(self, frame):
        cap=False
        x=0.0
        y=0.0
        frame, cap, x, y = detector.process_image(frame, cap, x, y)

        frame = LED1.detect(frame, x, y)
        frame = LED2.detect(frame, x, y)
        frame = LED3.detect(frame, x, y)
        frame = shape.draw(frame, x, y)
        frame = shape1.draw(frame, x, y)
        frame = shape2.draw(frame, x, y)
    def do_POST(self):

        content_type = self.headers['Content-Type']
        if not content_type.startswith('multipart/form-data'):
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid content type")
            return


        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})


        file_item = form['video']

        if file_item.filename:
            post_data = file_item.file.read()
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"No file received")
            return

        # Convert bytes to OpenCV image
        nparr = np.frombuffer(post_data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if frame is None:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid frame received")
            return



        self.procces_the_frame(frame)

        _, buffer = cv2.imencode('.jpg', frame)


        self.send_response(200)
        self.send_header('Content-type', 'image/jpeg')
        self.end_headers()
        self.wfile.write(buffer.tobytes())


def run():
    server_address = (HOST, PORT)
    httpd = HTTPServer(server_address, MyHandler)
    print(f"Server running on {HOST}:{PORT}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
