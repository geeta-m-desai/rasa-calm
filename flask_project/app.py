import subprocess

from flask import Flask, render_template
from flask_cors import CORS
from flask_socketio import SocketIO

from actions.voice_handling import audio_chunk_send_to_rasa

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on('audio_data')
def handle_audio(data):
    audio_data = data["blob"]
    lang = data["language"]
    print("before emitting audio ...")

    # Assuming Opus input
    converted_audio = convert_opus_to_wav(audio_data)

    audio_response = audio_chunk_send_to_rasa(converted_audio, 44100, 2, lang)
    socketio.emit('bot_response', {'audio': audio_response})
    print("after emitting audio ...")


def convert_opus_to_wav(opus_data):
    process = subprocess.Popen(['ffmpeg', '-i', 'pipe:0', '-f', 'wav', 'pipe:1'],
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    wav_data, err = process.communicate(opus_data)
    if err:
        print("error while converting opus", err)
    else:
        print("converted opus")
    return wav_data


@socketio.on('connect')
def on_connect():
    print('Client connected!')


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    socketio.run(app, port=8080, debug=True)
