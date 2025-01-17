from camera import CameraHelper
from streamer import StreamerHTTP
import numpy as np
import requests
import cv2
import os
from dotenv import load_dotenv, dotenv_values

streamer=StreamerHTTP('index.html')

cam=CameraHelper()
cam.start()

SERVER_URL = os.getenv("SERVER_API")

x=0
y=0
cap=False





def send_to_server_and_get (frame_bytes):

    files = {'video': frame_bytes}

    response = requests.post(SERVER_URL, files=files)

    # Yield the frame in multipart format for streaming
    # If the server returns the processed frame, replace the local frame with it
    if response.status_code == 200:
        # Decode the response content into an image
        nparr = np.frombuffer(response.content, np.uint8)
        processed_frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if processed_frame is not None:
            frame = processed_frame  # Replace the local frame with the processed one
        else:
            print("Warning: Received invalid processed frame from the server.")

    else:
        print(f"Error: Server returned status code {response.status_code}")

    return frame



def generate_frames():
    global cap, x, y

    while True:
        # Capture frame-by-frame
        frame = cam.capture_arrays()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)


        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        frame = send_to_server_and_get(frame_bytes)

        # Yield the processed frame for streaming
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
if __name__ == '__main__':
    try:
        #threading.Thread(target=turn_led_control, daemon=True).start()
        streamer.run(5000, generate_frames)
    finally:
        cam.strop()
        print('Closing video feed')


