from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "hello, Flask"

@app.route("/hello")
def hello():
    return "hello, World"