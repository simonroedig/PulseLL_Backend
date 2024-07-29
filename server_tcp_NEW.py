import socket
import threading
import pyaudio
import pickle
import struct

host_ip = '10.181.216.240'  # Localhost IP address
port = 9610

def audio_stream():
    server_socket = socket.socket()
    server_socket.bind((host_ip, port))  # Bind to port 9610
    server_socket.listen(5)
    
    client_socket, addr = server_socket.accept()
    print('Client connected:', addr)
    
    # PyAudio setup
    p = pyaudio.PyAudio()
    format = pyaudio.paInt16
    channels = 2
    rate = 44100

    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=1024)

    # Send audio parameters
    audio_params = (pyaudio.paInt16, channels, rate)
    client_socket.sendall(pickle.dumps(audio_params))
    
    while True:
        data = stream.read(1024)
        a = pickle.dumps(data)
        message = struct.pack("Q", len(a)) + a
        client_socket.sendall(message)
        
    client_socket.close()
    stream.stop_stream()
    stream.close()
    p.terminate()
    server_socket.close()

print('server listening at', (host_ip, port))
t1 = threading.Thread(target=audio_stream, args=())
t1.start()