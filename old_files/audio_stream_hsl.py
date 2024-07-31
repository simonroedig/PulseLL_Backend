import os
import subprocess
import threading
import logging
from http.server import SimpleHTTPRequestHandler, HTTPServer
import pyaudio

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

class AudioStreamServer:
    def __init__(self, host_ip, port):
        self.host_ip = host_ip
        self.port = port
        self.segment_duration = 4
        self.output_dir = "hls_stream"
        self.buffer_size = 4096
        self.ffmpeg_process = None
        self.ffmpeg_thread = None
        self.http_thread = None
        self.audio_thread = None

        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def start_server(self):
        try:
            self.ffmpeg_process = self.start_ffmpeg()
            self.audio_thread = threading.Thread(target=self.audio_capture)
            self.audio_thread.start()
            self.http_thread = threading.Thread(target=self.start_http_server)
            self.http_thread.start()
            print(f'Serving HLS stream on http://{self.host_ip}:{self.port}')
        except Exception as e:
            print(f"Error starting server: {e}")
            self.cleanup()

    def start_ffmpeg(self):
        ffmpeg_cmd = [
            'C:/ffmpeg/bin/ffmpeg',
            '-f', 's16le',  # Use raw audio format
            '-ar', '44100',  # Sampling rate
            '-ac', '2',  # Number of channels
            '-i', '-',  # Input from stdin
            '-acodec', 'aac',  # Encode to AAC
            '-b:a', '128k',  # Bitrate
            '-f', 'hls',  # Output format
            '-hls_time', str(self.segment_duration),  # Segment duration
            '-hls_list_size', '5',  # Number of segments to keep in the playlist
            '-hls_flags', 'delete_segments',  # Delete old segments
            '-hls_segment_filename', os.path.join(self.output_dir, 'segment_%03d.aac'),
            os.path.join(self.output_dir, 'playlist.m3u8')
        ]
        ffmpeg_process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)
        return ffmpeg_process

    def audio_capture(self):
        p = pyaudio.PyAudio()
        format = pyaudio.paInt16
        channels = 2
        rate = 44100

        stream = p.open(format=format,
                        channels=channels,
                        rate=rate,
                        input=True,
                        frames_per_buffer=self.buffer_size)

        try:
            while True:
                data = stream.read(self.buffer_size, exception_on_overflow=False)
                self.ffmpeg_process.stdin.write(data)
        except Exception as e:
            logging.error(f"Audio capture stopped due to: {e}")
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()
            self.ffmpeg_process.stdin.close()

    def start_http_server(self):
        os.chdir(self.output_dir)
        server_address = (self.host_ip, self.port)
        httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
        httpd.serve_forever()

    def start_server_in_thread(self):
        server_thread = threading.Thread(target=self.start_server)
        server_thread.start()

    def stop_server(self):
        self.cleanup()

    def cleanup(self):
        try:
            if self.ffmpeg_process:
                self.ffmpeg_process.terminate()
            if self.http_thread and self.http_thread.is_alive():
                # No direct method to stop HTTPServer, usually requires handling shutdown in the request handler
                logging.info("HTTP server stopped")
            if self.audio_thread and self.audio_thread.is_alive():
                self.audio_thread.join()
            logging.info("Cleanup complete")
        except Exception as e:
            logging.error(f"Error during cleanup: {e}")

    def start_ffmpeg_full_recording(self, user_id):
        folder = "full_recordings"
        if not os.path.exists(folder):
            os.makedirs(folder)
        full_recording_file = os.path.join(folder, str(user_id) + ".mp3")
        ffmpeg_cmd = [
            'C:/ffmpeg/bin/ffmpeg',
            '-f', 's16le',  # Use raw audio format
            '-ar', '44100',  # Sampling rate
            '-ac', '2',  # Number of channels
            '-i', '-',  # Input from stdin
            '-acodec', 'libmp3lame',  # Encode to MP3
            '-b:a', '192k',  # Bitrate
            full_recording_file
        ]
        ffmpeg_process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)
