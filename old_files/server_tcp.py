AUDIO_1 = "711804__leonseptavaux__drone_1.wav"
AUDIO_2 = "711805__leonseptavaux__drone_2.wav"

# This is server code to send audio frames over TCP

import socket
import threading
import wave
import pickle
import struct

host_ip = '127.0.0.1'  # Localhost IP address
port = 9611

def audio_stream():
    server_socket = socket.socket()
    server_socket.bind((host_ip, port-1))  # Bind to port 9610
    server_socket.listen(5)
    
    wf = wave.open(AUDIO_1, 'rb')
    sample_width = wf.getsampwidth()
    channels = wf.getnchannels()
    rate = wf.getframerate()
    audio_params = (sample_width, channels, rate)
    
    client_socket, addr = server_socket.accept()
    print('Client connected:', addr)

    # Send audio parameters
    client_socket.sendall(pickle.dumps(audio_params))
    
    CHUNK = 1024
    while True:
        data = wf.readframes(CHUNK)
        if not data:
            break
        a = pickle.dumps(data)
        message = struct.pack("Q", len(a)) + a
        client_socket.sendall(message)
        
    client_socket.close()
    wf.close()
    server_socket.close()

print('server listening at', (host_ip, port-1))
t1 = threading.Thread(target=audio_stream, args=())
t1.start()
