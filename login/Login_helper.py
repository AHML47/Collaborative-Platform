from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify

class Login:
    def __init__(self, loginPage):
        self.loginFile=loginPage


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
