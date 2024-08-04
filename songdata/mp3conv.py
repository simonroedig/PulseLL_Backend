import os
from pydub import AudioSegment

def trim_and_convert_audio_files(root_folder, trim_ms=2000, bitrate="192k"):
    """
    Trims the first `trim_ms` milliseconds from each .wav file in the given directory and its subdirectories,
    and converts them to compressed .mp3 files.

    :param root_folder: The root directory containing the audio files.
    :param trim_ms: The duration in milliseconds to trim from the start of each audio file.
    :param bitrate: The bitrate for the output .mp3 files.
    """
    for genre in ['dubstep', 'intro', 'rock', 'techno']:
        genre_path = os.path.join(root_folder, genre)
        
        for run in ['ran1', 'ran2', 'ran3']:
            run_path = os.path.join(genre_path, run)
            
            for file_name in os.listdir(run_path):
                if file_name.endswith('.wav'):
                    file_path = os.path.join(run_path, file_name)
                    
                    # Load the audio file
                    audio = AudioSegment.from_wav(file_path)
                    
                    # Trim the first `trim_ms` milliseconds
                    trimmed_audio = audio[trim_ms:]
                    
                    # Export the trimmed audio as an MP3 file
                    mp3_file_path = os.path.splitext(file_path)[0] + ".mp3"
                    trimmed_audio.export(mp3_file_path, format="mp3", bitrate=bitrate)
                    print(f"Converted {file_path} to {mp3_file_path} with bitrate {bitrate}")

# Set the root directory where the 'songrater' folder is located
root_directory = r"C:\Users\simon\Desktop\songdata"
trim_and_convert_audio_files(root_directory)
