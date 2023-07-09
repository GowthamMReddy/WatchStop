from flask import Flask, url_for

def create_app():
    app=Flask(__name__)

    @app.route('/')
    def helloworld():
        return "<p>Hello, World!</p>"

    return app