import socket
import threading
import pyaudio
import pickle
import struct
import os
from dotenv import load_dotenv

class AudioStreamServer:
    def __init__(self, host_ip, port):
        self.host_ip = host_ip
        self.port = port
        self.server_socket = socket.socket()
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.client_socket = None
        self.thread = None

    def start_server(self):
        self.server_socket.bind((self.host_ip, self.port))
        self.server_socket.listen(5)
        print('Server listening at', (self.host_ip, self.port))
        
        self.client_socket, addr = self.server_socket.accept()
        print('Client connected:', addr)

        # PyAudio setup
        format = pyaudio.paInt16
        channels = 2
        rate = 44100

        self.stream = self.p.open(format=format,
                                  channels=channels,
                                  rate=rate,
                                  input=True,
                                  frames_per_buffer=1024)

        # Send audio parameters
        audio_params = (format, channels, rate)
        self.client_socket.sendall(pickle.dumps(audio_params))

        self.thread = threading.Thread(target=self.audio_stream)
        self.thread.start()

    def audio_stream(self):
        try:
            while True:
                data = self.stream.read(1024)
                a = pickle.dumps(data)
                message = struct.pack("Q", len(a)) + a
                self.client_socket.sendall(message)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.stop_server()

    def stop_server(self):
        if self.client_socket:
            self.client_socket.close()
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()
        self.server_socket.close()

    def start_server_in_thread(self):
        server_thread = threading.Thread(target=self.start_server)
        server_thread.start()

    def stop_server_in_thread(self):
        if self.thread:
            self.thread.join()