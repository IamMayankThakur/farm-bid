from flask import Flask, request
from flask_socketio import SocketIO
import eventlet

eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!sdfjsjdhjsdw8w8e'
socketio = SocketIO(app, message_queue='redis://redis:6379')

@socketio.on('connect', namespace='/')
def test_connect():
    print('A client connected!')


@app.route('/', methods=['GET'])
def index():
    return 'Hello from Flask!'


@app.route('/con-test/')
def con_test():
    return 'Test succeeded!'


@app.route('/bid-placed/', methods=['POST'])
def bid_placed():
    message = request.form['message']
    socketio.emit('bid placed', {'message': message}, namespace='/')
    return ''


@app.route('/item-sold/', methods=['POST'])
def item_sold():
    message = request.form['message']
    socketio.emit('item sold', {'message': message}, namespace='/')
    return ''


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=9000)
