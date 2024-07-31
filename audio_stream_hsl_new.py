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
                self.recording_data.append(data)
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

    def save_recording_as_mp3(self, user_id):
        # Ensure the full_recordings directory exists
        full_recordings_dir = "full_recordings"
        if not os.path.exists(full_recordings_dir):
            os.makedirs(full_recordings_dir)

        # Check if recording_data is not empty
        if not self.recording_data:
            logging.error("No audio data available to save.")
            return

        # Create the raw audio file and write the recorded data to it
        raw_audio_path = 'raw_audio.raw'
        try:
            with open(raw_audio_path, 'wb') as raw_audio_file:
                raw_audio_file.write(b''.join(self.recording_data))
            logging.info(f"Raw audio data written to {raw_audio_path}")
        except Exception as e:
            logging.error(f"Error writing raw audio data to file: {e}")
            return

        # Define the path for the mp3 file
        output_path = os.path.join(full_recordings_dir, f"{user_id}.mp3")

        # Use ffmpeg to convert raw audio data to mp3
        ffmpeg_cmd = [
            'C:/ffmpeg/bin/ffmpeg',
            '-f', 's16le',  # Raw audio format
            '-ar', '44100',  # Sampling rate
            '-ac', '2',  # Number of channels
            '-i', raw_audio_path,  # Input raw audio file
            '-codec:a', 'mp3',  # Encode to MP3
            '-b:a', '128k',  # Bitrate
            output_path  # Output file
        ]

        try:
            # Run the ffmpeg command to convert the raw audio file to MP3
            subprocess.run(ffmpeg_cmd, check=True)
            logging.info(f"Recording saved as {output_path}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error converting raw audio to MP3: {e}")
        finally:
            # Clean up the temporary raw audio file
            if os.path.exists(raw_audio_path):
                os.remove(raw_audio_path)
                logging.info(f"Temporary raw audio file {raw_audio_path} deleted")
            else:
                logging.error(f"Temporary raw audio file {raw_audio_path} not found for deletion")


    def start_server(self):
        self.recording_data = []
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
