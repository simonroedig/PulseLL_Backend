import asyncio
from flask import Flask, app, jsonify, request, send_file
from icecream import ic
from dotenv import load_dotenv
import os
import json
import random
from pydub import AudioSegment

# python 3.9.(11)
# .venv\Scripts\activate
# "C:\Users\simon\AppData\Local\Programs\Python\Python39\python.exe"
# virtualenv -p C:\Users\simon\AppData\Local\Programs\Python\Python39\python.exe venv

from vital_threshold_logic import VitalThresholdLogic

load_dotenv()

vital_logic = VitalThresholdLogic(change_threshold=5, window_size=5) 

app = Flask(__name__)
root_working_dir = os.getcwd()

just_started_running = True
user_id = -1
workout_id = -1

all_song_array = []

# gets called as often as frontend sends us the vital parameters
@app.route('/vital_parameters', methods=['POST'])
def receive_vital_parameters():
    global just_started_running
    global user_id
    global workout_id
    global all_song_array
    
    data = request.get_json()
    ic(data)

    if not data:
        return jsonify({"error": "No data provided"}), 400
    if 'heart_rate' not in data:
        return jsonify({"error": "Missing heart_rate parameter"}), 400
    if 'unix_timestamp' not in data:
        return jsonify({"error": "Missing unix_timestamp parameter"}), 400
    if 'song_genre' not in data:
        return jsonify({"error": "Missing song_genre parameter"}), 400
    if 'user_id' not in data:
        return jsonify({"error": "Missing user_id parameter"}), 400
    if 'workout_id' not in data:
        return jsonify({"error": "Missing workout_id parameter"}), 400
    if 'activity_type' not in data:
        return jsonify({"error": "Missing activity_type parameter"}), 400

    heart_rate = data['heart_rate']
    ic(heart_rate)
    if heart_rate == "0" or heart_rate == 0:
        data = {
            "new_song": False,
            "error": "Heart rate is 0"
        }
        return jsonify(data), 200
    unix_timestamp = data['unix_timestamp']
    song_genre = data['song_genre']
    user_id = data['user_id']
    workout_id = data['workout_id']
    activity_type = data['activity_type']

    vital_logic.set_append_heart_rate_and_time(heart_rate, unix_timestamp)
    
    print("Just started running: ", just_started_running)
    
    if vital_logic.has_significant_change_occurred() or just_started_running:
        current_median_heart_rate = vital_logic.get_current_median_heartrate(check_last_x_heart_rates=3)
        ic(current_median_heart_rate)
        
        if current_median_heart_rate <= 80:
            song = 60
        elif 80 < current_median_heart_rate <= 110:
            song = 90
        elif 110 < current_median_heart_rate <= 130:
            song = 120
        elif 130 < current_median_heart_rate <= 150:
            song = 140
        else:  # current_median_heart_rate > 150
            song = 160
            
        ic(song)    
        song_filename = str(song) + ".wav"
        ic(song_filename)
        
        if just_started_running:
            just_started_running = False
        
            random_number = random.choice([1, 2])
            data = {
                "new_song": True,
                "folder": "intro",
                "subfolder": f"ran{random_number}",
                "song": song_filename
            }
            all_song_array.append(data)
            return jsonify(data), 200

        
        random_number = random.choice([1, 2])
        data = {
            "new_song": True,
            "folder": f"{song_genre.lower()}",
            "subfolder": f"ran{random_number}",
            "song": song_filename
        }
        all_song_array.append(data)
        return jsonify(data), 200

    data = {
            "new_song": False
        }
    return jsonify(data), 200

@app.route('/stop_workout', methods=['GET'])
def receive_stop_workout():
    global just_started_running
    global audio_server_started
    global user_id
    global workout_id

    if user_id == -1:
        return jsonify({"error": "Can't stop workout, cause you haven't started it yet. No user_id provided"}), 400

    just_started_running = True
    
    concatenate_songs(all_song_array, output_filename=f"{user_id}_{workout_id}.mp3")

    return jsonify({"message": "Success"}), 200

@app.route('/get_thumbnail_img', methods=['POST'])
def get_thumbnail_img():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400
    if 'user_id' not in data:
        return jsonify({"error": "Missing user_id parameter"}), 400
    if 'workout_id' not in data:
        return jsonify({"error": "Missing workout_id parameter"}), 400

    user_id = data['user_id']
    workout_id = data['workout_id']

    # Check the folder heart_rate_images and return the file that has the user_id and workout_id in its name
    # The file will be an .png file
    thumbnail_img_dir = os.path.join(root_working_dir, "thumbnail_img")
    files = os.listdir(thumbnail_img_dir)

    png_file = None
    for file in files:
        if (str(user_id) in file) and (str(workout_id) in file) and (file.endswith('.png')):
            png_file = os.path.join(thumbnail_img_dir, file)
            break

    if not png_file or not os.path.exists(png_file):
        return jsonify({"error": "File not found"}), 404

    return send_file(png_file, mimetype='image/png')

@app.route('/get_full_song', methods=['POST'])
def get_full_song():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400
    if 'workout_id' not in data:
        return jsonify({"error": "Missing workout_id parameter"}), 400

    workout_id = data['workout_id']

    # Check the folder full_recordings and return the file that has the workout_id in its name
    # The file will be an .mp3 file
    final_song_dir = os.path.join(root_working_dir, "final_song")
    files = os.listdir(final_song_dir)

    # Find the file with the workout_id in its name
    mp3_file = None
    for file in files:
        if str(workout_id) in file and file.endswith('.mp3'):
            mp3_file = os.path.join(final_song_dir, file)
            break

    if not mp3_file or not os.path.exists(mp3_file):
        return jsonify({"error": "File not found"}), 404

    return send_file(mp3_file, mimetype='audio/mpeg')

def concatenate_songs(all_song_array, root_folder='songdata', output_folder='final_song', output_filename='final_song.mp3'):
    # Ensure the output directory exists
    os.makedirs(output_folder, exist_ok=True)

    # Initialize an empty AudioSegment
    final_song = AudioSegment.empty()

    # Iterate over each song entry in the array
    for song_data in all_song_array:
        folder = song_data["folder"]
        subfolder = song_data["subfolder"]
        song_filename = song_data["song"]

        # Construct the full path to the song
        song_path = os.path.join(root_folder, folder, subfolder, song_filename)

        # Load the song and append it to the final song
        song = AudioSegment.from_wav(song_path)
        final_song += song

    # Export the final song as an MP3 file
    output_path = os.path.join(output_folder, output_filename)
    final_song.export(output_path, format="mp3")

    print(f"Final song created at: {output_path}")
    
if __name__ == "__main__":
    print("Starting Flask app...")
    app.run(debug=True, port=5000, host='0.0.0.0', use_reloader=False)
    print("!!!!! Flask app running !!!!!")