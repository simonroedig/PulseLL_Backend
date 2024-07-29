import asyncio
from flask import Flask, app, jsonify, request
from icecream import ic

# python 3.9.(11)
# myenv\Scripts\activate
# "C:\Users\simon\AppData\Local\Programs\Python\Python39\python.exe"
# virtualenv -p C:\Users\simon\AppData\Local\Programs\Python\Python39\python.exe venv

# own libraries
from openai_client import OpenAIClient
#from audio_stream_empty import AudioStreamEmpty
#from sonic_pi_empty import SonicPiEmpty
from sonic_pi_alternative import SonicPiAlternative
from vital_threshold_logic import VitalThresholdLogic
from prompt_constructor import PromptConstructor

vital_logic = VitalThresholdLogic(change_threshold=5, window_size=5) 
prompt_constructor = PromptConstructor(heart_rate="0", song_genre="techno", current_sonic_pi_code="no_code_yet")
sonic_pi_alternative = SonicPiAlternative(port=4560, ip="127.0.0.1")

openai = OpenAIClient(model="gpt-3.5-turbo-1106", max_response_tokens=300, temperature=0.7, top_p=0.8)

app = Flask(__name__)

just_started_running = True

# gets called as often as frontend sends us the vital parameters
@app.route('/vital_parameters', methods=['POST'])
def receive_vital_parameters():
    global just_started_running
    
    data = request.get_json()
    print(data)
    if not data:
        return jsonify({"error": "No data provided"}), 400
    if 'heart_rate' not in data:
        return jsonify({"error": "Missing heart_rate parameter"}), 400

    heart_rate = data['heart_rate']
    vital_logic.set_append_heart_rate(heart_rate)
    
    if vital_logic.has_significant_change_occurred() or just_started_running:
        just_started_running = False
        print("Significant change detected")
        
        current_median_heart_rate = vital_logic.get_current_median_heartrate(check_last_x_heart_rates=3)
        ic(current_median_heart_rate)
        
        prompt_constructor.set_heart_rate(current_median_heart_rate)
        prompt = prompt_constructor.to_json()
        ic(prompt)
        
        openAI_response = asyncio.run(fetch_openai_completion(prompt))
        ic(openAI_response)
        new_sonic_pi_code = openAI_response.choices[0].message.content
        
        prompt_constructor.set_sonic_pi_code(new_sonic_pi_code)
        
        # get, send and play the new sonic pi code
        current_sonic_pi_code = prompt_constructor.get_sonic_pi_code()
        sonic_pi_alternative.send_code(current_sonic_pi_code)
        
        
    return jsonify({"message": "Success"}), 200


async def fetch_openai_completion(prompt):
    return await openai.get_completion(system_message="", user_message=prompt)

if __name__ == "__main__":
    app.run(debug=True, port=5000)