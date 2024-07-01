from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello, World!"

@app.route('/add')
def add():
    a = request.args.get("a")
    b = request.args.get("b")
    result = int(a) + int(b)
    return str(result)