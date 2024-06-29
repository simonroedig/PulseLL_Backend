import asyncio
from flask import Flask, app, jsonify, request

# own libraries
from openai_client import OpenAIClient
from audio_stream_empty import AudioStreamEmpty
from sonic_pi_empty import SonicPiEmpty
from vital_threshold_logic import VitalThresholdLogic
from prompt_constructor import PromptConstructor

vital_logic = VitalThresholdLogic(change_threshold=10, window_size=5) 
prompt_constructor = PromptConstructor(heart_rate="0", song_genre="techno", current_sonic_pi_code="no_code_yet")

openai = OpenAIClient(model="gpt-3.5-turbo-1106", max_response_tokens=300, temperature=0.7, top_p=0.8)

app = Flask(__name__)

@app.route('/vital_parameters', methods=['POST'])
async def receive_vital_parameters():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    if 'heart_rate' not in data:
        return jsonify({"error": "Missing heart_rate parameter"}), 400

    heart_rate = data['heart_rate']
    vital_logic.set_append_heart_rate(heart_rate)
    
    if vital_logic.has_significant_change_occurred():
        current_median_heart_rate = vital_logic.get_current_median_heartrate(check_last_x_heart_rates=3)
        
        prompt_constructor.set_heart_rate(current_median_heart_rate)
        prompt = prompt_constructor.to_json()
        
        openAI_response = await openai.get_completion(system_message="", user_message=prompt)
        new_sonic_pi_code = openAI_response.choices[0].message.content
        
        prompt_constructor.set_sonic_pi_code(new_sonic_pi_code)
        
        
        current_sonic_pi_code = prompt_constructor.get_sonic_pi_code()
        # based on alex and mia.. send new code to sonic pi and audio stream
    
    
if __name__ == "__main__":
    app.run(debug=True, port=5000)