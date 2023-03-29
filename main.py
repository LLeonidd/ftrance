from threading import Lock
from flask import Flask, render_template, session, request, \
    copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()


# def background_thread():
#     """Example of how to send server generated events to clients."""
#     count = 0
#     while True:
#         socketio.sleep(10)
#         count += 1
#         socketio.emit('socket_response',
#                       {'data': 'Server generated event', 'count': count})


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.event
def send_socket(message):
    emit('socket_response',
         {'data': message['data']})


@socketio.event
def send_broadcast_event(message):
    emit('socket_response',
         {'data': message['data']},
         broadcast=True)


@socketio.event
def join(message):
    join_room(message['room'])
    emit('socket_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),})


@socketio.event
def leave(message):
    leave_room(message['room'])
    emit('socket_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),})


@socketio.on('close_room')
def on_close_room(message):
    emit('socket_response', {'data': 'Room ' + message['room'] + ' is closing.',},
         to=message['room'])
    close_room(message['room'])


@socketio.event
def send_room(message):
    emit('socket_response',
         {'data': message['data']},
         to=message['room'])


@socketio.event
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()
    emit('socket_response',
         {'data': 'Disconnected!'},
         callback=can_disconnect)


# @socketio.event
# def connect():
#     global thread
#     with thread_lock:
#         if thread is None:
#             thread = socketio.start_background_task(background_thread)
#     emit('socket_response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    socketio.run(app)



# from flask import Flask, render_template
# from flask_sock import Sock
#
#
# app = Flask(__name__)
# sock = Sock(app)
#
#
#
# @app.route('/')
# def index():
#     return render_template('index.html')
#
#
# @sock.route('/receive/vending1')
# def receive(sock):
#     while True:
#         data = sock.receive()
#         sock.send(data)
