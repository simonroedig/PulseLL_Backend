from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import pyaudio

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

def stream_audio():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    while True:
        data = stream.read(1024)
        socketio.emit('audio', data, broadcast=True)

if __name__ == '__main__':
    socketio.start_background_task(target=stream_audio)
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
