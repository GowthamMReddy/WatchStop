from flask import Flask, url_for

def create_app():
    app=Flask(__name__)

    return app