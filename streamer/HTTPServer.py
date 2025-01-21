from flask import Flask, Response , request, jsonify
from pip._vendor import requests
import os


class StreamerHTTP :
    def __init__(self,indexFile) :
        self.app = Flask(__name__)
        self.SERVER_URL = os.getenv("Server_API")
        with open(indexFile,'r') as f:
            self.indexFile = f.read()

    def route(self, path, endpoint=None ,methods=None):
        # The decorator logic that wraps the function
        def decorator(func):
            # Use the provided endpoint name or the function's name
            endpoint_name = endpoint or func.__name__
            if methods is None:
                @self.app.route(path, endpoint=endpoint_name,)
                def handler(*args, **kwargs):
                    return func(*args, **kwargs)
            else :
                @self.app.route(path, endpoint=endpoint_name,methods=methods )
                def handler(*args, **kwargs):
                    return func(*args, **kwargs)
            return handler

        return decorator


    def index(self) :
        return self.indexFile
    def login(self) :
        with open('Login.html','r') as f:
            return f.read()


    def VerifLogin(self):
        try:
            # Parse JSON data from the request
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            response = requests.post(self.SERVER_URL+'/login', json={'username':username, 'password':password})

            # Dummy logic for demonstration (replace with real authentication logic)
            if request.status_code == 200 :
                return jsonify({"message": "Login successful!"}), 200
            else:
                return jsonify({"message": "Invalid username or password"}), 401
        except Exception as e:
            return jsonify({"message": f"An error occurred: {str(e)}"}), 500

    def video(self,provider) :
        return Response(provider(), mimetype='multipart/x-mixed-replace; boundary=frame')

    def define_routes(self, provider):
        # Use route directly here, as @route doesn't work due to the self requirement
        self.route('/')(self.index)
        self.route('/login')(self.login)
        self.route('/video_feed', endpoint='video_feed')(lambda: self.video(provider))
        self.route('/Verif', methods=['POST'])(self.VerifLogin)


    def run(self,portNum,provider) :
        self.define_routes(provider)
        self.video(provider)
        self.app.run(host='0.0.0.0',port=portNum)




