# This is client code to receive audio frames over TCP

import socket
import os
import threading
import wave
import pyaudio
import pickle
import struct
import signal
import sys

host_ip = '10.181.242.44'  # Localhost IP address
port = 9665
running = True

def audio_stream():
    global running
    p = pyaudio.PyAudio()
    CHUNK = 1024

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_address = (host_ip, port)  # Connect to port 9610
    print('server listening at', socket_address)
    client_socket.connect(socket_address)
    print("CLIENT CONNECTED TO", socket_address)

    # Receive audio parameters
    audio_params = pickle.loads(client_socket.recv(1024))
    sample_width, channels, rate = audio_params
    
    stream = p.open(format=p.get_format_from_width(sample_width),
                    channels=channels,
                    rate=rate,
                    output=True,
                    frames_per_buffer=CHUNK)

    data = b""
    payload_size = struct.calcsize("Q")
    
    while running:
        try:
            while len(data) < payload_size:
                packet = client_socket.recv(4*1024)  # 4K
                if not packet:
                    running = False
                    break
                data += packet
            if not running:
                break
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            while len(data) < msg_size:
                data += client_socket.recv(4*1024)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)
            stream.write(frame)
        except:
            break

    stream.close()
    client_socket.close()
    print('Audio closed')
    os._exit(1)

t1 = threading.Thread(target=audio_stream, args=())
t1.start()
