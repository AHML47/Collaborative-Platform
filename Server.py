from flask import Flask, Response, request ,jsonify
import cv2
import threading
import numpy as np
from object import ObjectHelper
#from Logger import Log
from detector import HandDetector
from component import LED
app = Flask(__name__)

detector=HandDetector()

LED1 = LED(1,570,410,50)
LED2 = LED(2,500,410,50)
LED3 = LED(3,430,410,50)

shape = ObjectHelper(0,(0,255,0),'rectangle',50,100,100)
shape1 = ObjectHelper(0,(200,255,0),'rectangle',50,150,150)
shape2 = ObjectHelper(0,(20,255,200),'rectangle',50,200,200)

# Global variable to hold the video frame
video_frame = None
lock = threading.Lock()

def generate_frames():
    """Yield video frames for clients (MJPEG stream)."""
    global video_frame
    while True:
        with lock:
            if video_frame is None:
                continue
            # Encode the frame to JPEG
            _, buffer = cv2.imencode('.jpg', video_frame)
            frame = buffer.tobytes()
        # Yield the frame as a multipart response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/upload_stream', methods=['POST'])
def upload_stream():
    """Endpoint to receive video stream from the source server."""
    global video_frame
    if 'video' not in request.files:
        return "No video file provided", 400

    file = request.files['video']
    x=0
    y=0
    cap=False
    # Read the file into a NumPy array
    file_data = file.read()
    nparr = np.frombuffer(file_data, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # Decode image from buffer
    frame, cap, x, y = detector.process_image(frame,
                                              cap,
                                              x,
                                              y
                                              )
    frame = LED1.detect(frame,x,y)
    frame = LED2.detect(frame, x, y)
    frame = LED3.detect(frame, x, y)
    frame = shape.draw(frame, x, y)
    frame = shape1.draw(frame, x, y)
    frame = shape2.draw(frame, x, y)

    if frame is None:
        return "Invalid frame data", 400

    # Update the global video_frame
    with lock:
        video_frame = frame
    _,data = cv2.imencode('.jpg', video_frame)

    return Response(data.tobytes(), mimetype='image/jpeg'),200
@app.route('/loginVerfi', methods=['POST'])
def loginVerfi():
    """Endpoint to verify login status."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if username == "admin" and password == "password123":
        return jsonify({"message": "Login successful!"}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401


@app.route('/stream', methods=['GET'])
def stream():
    """Endpoint to serve the relayed stream."""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
