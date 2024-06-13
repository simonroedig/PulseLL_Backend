import os
from pythonosc.udp_client import SimpleUDPClient
import sounddevice as sd
import numpy as np

# Configuration
sonic_pi_host = '127.0.0.1'  # Localhost
sonic_pi_port = 4560         # Default OSC port for Sonic Pi
audio_file_path = "output.wav"
mp3_file_path = "output.mp3"

# Initialize OSC client
client = SimpleUDPClient(sonic_pi_host, sonic_pi_port)

# Function to send Sonic Pi code
def send_code_to_sonic_pi(code):
    client.send_message('/trigger/prophet', [70, 100, 8])

# Function to record audio
def record_audio(duration, fs=44100):
    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='float64')
    sd.wait()
    return recording

# Function to save the recording to a WAV file
def save_recording(recording, filename):
    from scipy.io.wavfile import write
    write(filename, 44100, np.int16(recording * 32767))
    print(f"Saved recording to {filename}")

# Read Sonic Pi code from a file
with open("sonic_pi_code.txt", "r") as file:
    sonic_pi_code = file.read()

# Send the Sonic Pi code
send_code_to_sonic_pi(sonic_pi_code)

# Record for a specific duration (e.g., 10 seconds)
recording = record_audio(10)

# Save the recording
save_recording(recording, audio_file_path)
