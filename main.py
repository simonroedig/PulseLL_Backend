import asyncio
from flask import Flask, app, jsonify, request, send_file
from icecream import ic
from dotenv import load_dotenv
import os

# python 3.9.(11)
# .venv\Scripts\activate
# "C:\Users\simon\AppData\Local\Programs\Python\Python39\python.exe"
# virtualenv -p C:\Users\simon\AppData\Local\Programs\Python\Python39\python.exe venv

# own libraries
from openai_client import OpenAIClient

# you need to install https://vb-audio.com/Cable/
# and use this as your audio output (microphone)
from audio_stream_hsl import AudioStreamServer
from sonic_pi import SonicPi
from vital_threshold_logic import VitalThresholdLogic
from prompt_constructor import PromptConstructor

load_dotenv()

vital_logic = VitalThresholdLogic(change_threshold=5, window_size=5) 
prompt_constructor = PromptConstructor(heart_rate="0", song_genre="techno", activity_type="running", current_sonic_pi_code="no_code_yet")
sonic_pi = SonicPi(port=4560, ip="127.0.0.1")
audio_server = AudioStreamServer(os.getenv("AUDIO_IPV4"), port = int(os.getenv("AUDIO_PORT")))
openai = OpenAIClient(model="gpt-3.5-turbo-1106", max_response_tokens=3000, temperature=0.7, top_p=0.8)

app = Flask(__name__)

root_working_dir = os.getcwd()

just_started_running = True
audio_server_started = False
user_id = -1
#workout_id is five digits long
workout_id = -1


# gets called as often as frontend sends us the vital parameters
@app.route('/vital_parameters', methods=['POST'])
def receive_vital_parameters():
    global just_started_running
    global audio_server_started
    global user_id
    global workout_id
    
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
    unix_timestamp = data['unix_timestamp']
    song_genre = data['song_genre']
    user_id = data['user_id']
    workout_id = data['workout_id']
    activity_type = data['activity_type']

    vital_logic.set_append_heart_rate_and_time(heart_rate, unix_timestamp)
    
    if vital_logic.has_significant_change_occurred() or just_started_running:
        # Start audio server here to enforce starting it once only
        if just_started_running and not audio_server_started:
            audio_server.start_server_in_thread()
            #audio_server.save_recording_as_mp3(user_id)
            audio_server_started = True
                
        current_median_heart_rate = vital_logic.get_current_median_heartrate(check_last_x_heart_rates=3)
        ic(current_median_heart_rate)
        
        prompt_constructor.set_heart_rate(current_median_heart_rate)
        prompt_constructor.set_song_genre(song_genre)
        prompt_constructor.set_activity_type(activity_type)
    
        if just_started_running:
            prompt = prompt_constructor.to_json_only_intro()
        else:
            prompt = prompt_constructor.to_json()

        ic(prompt)
        
        openAI_response = asyncio.run(fetch_openai_completion(prompt))
        ic(openAI_response)
        new_sonic_pi_code = openAI_response.choices[0].message.content
        ic(new_sonic_pi_code)
        
        if just_started_running:
            prompt_constructor.set_intro_code(new_sonic_pi_code)
        else:
            prompt_constructor.set_sonic_pi_code(new_sonic_pi_code)
        
        # get, send and play the new sonic pi code
        if just_started_running:
            current_sonic_pi_code = prompt_constructor.get_intro_code()
        else:
            current_sonic_pi_code = prompt_constructor.get_sonic_pi_code()

        sonic_pi.stop_all()
        sonic_pi.send_code(current_sonic_pi_code)

        just_started_running = False
            
    return jsonify({"message": "Success"}), 200

@app.route('/stop_workout', methods=['GET'])
def receive_stop_workout():
    global just_started_running
    global audio_server_started
    global user_id
    global workout_id

    if user_id == -1:
        return jsonify({"error": "Can't stop workout, cause you haven't started it yet. No user_id provided"}), 400

    just_started_running = True
    audio_server_started = False

    audio_server.stop_server()
    vital_logic.reset()
    sonic_pi.send_silent_code()

    # check if a file with this workout_id exists in the full_recordings folder
    full_recordings_dir = os.path.join(root_working_dir, "full_recordings")
    files = os.listdir(full_recordings_dir)
    for file in files:
        if str(workout_id) in file and file.endswith('.mp3'):
            return jsonify({"message": "A song for this workout_id exists already. No new song saved. Workout stopped anyways."}), 200

    audio_server.save_recording_as_mp3(user_id, workout_id)

    return jsonify({"message": "Success"}), 200

# is probably not needed as you can get it in the frontend
# @app.route('/get_heart_rate_img', methods=['POST'])

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
    full_recordings_dir = os.path.join(root_working_dir, "full_recordings")
    files = os.listdir(full_recordings_dir)

    # Find the file with the workout_id in its name
    mp3_file = None
    for file in files:
        if str(workout_id) in file and file.endswith('.mp3'):
            mp3_file = os.path.join(full_recordings_dir, file)
            break

    if not mp3_file or not os.path.exists(mp3_file):
        return jsonify({"error": "File not found"}), 404

    return send_file(mp3_file, mimetype='audio/mpeg')


async def fetch_openai_completion(prompt):
    return await openai.get_completion(system_message="", user_message=prompt)

if __name__ == "__main__":
    print("Starting Flask app...")
    app.run(debug=True, port=5000, host='0.0.0.0', use_reloader=False)
    print("!!!!! Flask app running !!!!!")