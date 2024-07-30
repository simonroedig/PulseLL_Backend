import socket
import threading
import pyaudio
import pickle
import struct
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

class AudioStreamServer:
    def __init__(self, host_ip, port):
        self.host_ip = host_ip
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.client_socket = None
        self.audio_thread = None

    def start_server(self):
        try:
            self.server_socket.bind((self.host_ip, self.port))
            self.server_socket.listen(5)
            logging.info(f'Server listening at {self.host_ip}:{self.port}')

            self.client_socket, addr = self.server_socket.accept()
            logging.info(f'Client connected: {addr}')

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

            self.audio_thread = threading.Thread(target=self.audio_stream)
            self.audio_thread.start()

        except Exception as e:
            logging.error(f"Error starting server: {e}")
            self.cleanup()

    def audio_stream(self):
        try:
            while True:
                data = self.stream.read(1024)
                a = pickle.dumps(data)
                message = struct.pack("Q", len(a)) + a
                self.client_socket.sendall(message)
        except socket.error as e:
            logging.error(f"Socket error: {e}")
        except Exception as e:
            logging.error(f"Error: {e}")
        finally:
            self.cleanup()

    def cleanup(self):
        try:
            if self.client_socket:
                self.client_socket.close()
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
            self.p.terminate()
            self.server_socket.close()
        except Exception as e:
            logging.error(f"Error during cleanup: {e}")

    def start_server_in_thread(self):
        server_thread = threading.Thread(target=self.start_server)
        server_thread.start()

    def stop_server(self):
        self.cleanup()
