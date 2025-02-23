import cv2
import requests
import numpy as np
from dotenv import load_dotenv, dotenv_values
import os
from streamer.HTTPServer import StreamerHTTP

# Initialize the HTTP streamer
streamer = StreamerHTTP('index.html')

load_dotenv()
SERVER_URL = os.getenv("Server_UP_API")
print(f"SERVER_URL is: {SERVER_URL}")



# Initialize the webcam (use 0 for default laptop camera)
camera = cv2.VideoCapture(0)  # 0 is typically the default webcam; change to 1 if you have a second camera

if not camera.isOpened():
    raise Exception("Could not open the webcam.")

def send_to_server_and_get_frame (frame_bytes):

    files = {'video': frame_bytes}
    frame=None

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


    while True:
        # Capture frame-by-frame from the webcam
        ret, frame = camera.read()
        if not ret:
            print("Failed to capture frame from the camera.")
            break

        # Process the frame using the detector


        # Encode the frame to JPEG format
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        # Send the frame and additional data to the server
        frame =  send_to_server_and_get_frame(frame_bytes)

        # Yield the processed frame for streaming
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

if __name__ == '__main__':
    try:
        # Start the HTTP streamer
        streamer.run(5000, generate_frames)
    finally:
        # Release the camera resource
        camera.release()
        print('Closing video feed')
