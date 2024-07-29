import os
from dotenv import load_dotenv
from audio_stream import AudioStreamServer
audio_server = AudioStreamServer(os.getenv("AUDIO_IPV4"), port = int(os.getenv("AUDIO_PORT")))
audio_server.stop_server