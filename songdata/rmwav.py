import os

def remove_wav_files(root_folder):
    """
    Removes all .wav files from the given directory and its subdirectories.

    :param root_folder: The root directory containing the audio files.
    """
    for genre in ['dubstep', 'intro', 'rock', 'techno']:
        genre_path = os.path.join(root_folder, genre)
        
        for run in ['ran1', 'ran2', 'ran3']:
            run_path = os.path.join(genre_path, run)
            
            for file_name in os.listdir(run_path):
                if file_name.endswith('.wav'):
                    file_path = os.path.join(run_path, file_name)
                    
                    # Remove the .wav file
                    os.remove(file_path)
                    print(f"Removed {file_path}")

# Set the root directory where the 'songrater' folder is located
root_directory = r"C:\Users\simon\Desktop\songdata"
remove_wav_files(root_directory)
