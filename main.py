from flask import Flask, render_template
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)


@app.route('/')
def index():
    return render_template('index.html')


@sock.route('/receive/vending1')
def receive(sock):
    while True:
        data = sock.receive()
        sock.send(data)
