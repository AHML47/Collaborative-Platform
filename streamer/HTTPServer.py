from flask import Flask, Response


class StreamerHTTP :
    def __init__(self,indexFile) :
        self.app = Flask(__name__)
        with open(indexFile,'r') as f:
            self.indexFile = f.read()

    def route(self, path, endpoint=None):
        # The decorator logic that wraps the function
        def decorator(func):
            # Use the provided endpoint name or the function's name
            endpoint_name = endpoint or func.__name__
            @self.app.route(path, endpoint=endpoint_name)
            def handler(*args, **kwargs):
                return func(*args, **kwargs)

            return handler

        return decorator


    def index(self) :
        return self.indexFile


    def video(self,provider) :
        return Response(provider(), mimetype='multipart/x-mixed-replace; boundary=frame')

    def define_routes(self, provider):
        # Use route directly here, as @route doesn't work due to the self requirement
        self.route('/')(self.index)
        self.route('/video_feed', endpoint='video_feed')(lambda: self.video(provider))


    def run(self,portNum,provider) :
        self.define_routes(provider)
        self.video(provider)
        self.app.run(host='0.0.0.0',port=portNum)




