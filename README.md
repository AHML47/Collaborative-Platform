this is a collaborative platform project for Raspberry Pi 5 ,PC 
the idea of this platform is to control components connected to esp cart using http-server to handle synchronization
for python development on Raspberry Pi you should create a python virtual environment and install required packages on it 
to create virtual environment : 
    ``````
    python3 -m venv <name_of_venv>
    ``````
to activate the venv:
    ```source <name_of_venv>/bin/activate```

required packages : 
for camera :
    ```
    sudo apt install -y python3-libcamera python3-kms++
    sudo apt install -y python3-prctl libatlas-base-dev ffmpeg python3-pip
    sudo apt install -y python3-pyqt5 python3-opengl # only if you want GUI features
    pip3 install numpy --upgrade
    pip install python-dotenv
    pip3 install picamera2
    pip install rpi-libcamera
    pip install kms
    pip install rpi-kms```

for the webServer :
    ``
    pip install Flask
    pip install requests``

for mediapipe:
    `
    pip install mediapipe`

for open-cv :
    ``
    pip install opencv-python``

in this repository there's server , esp , raspberry and pc code so before start working you should start the server and esp and change their ip address in the .env file