import json

class PromptConstructor:
    def __init__(self, heart_rate, song_genre, activity_type, current_sonic_pi_code):
        self.our_idea = """
        Our idea is PulseLL: The user is doing an exercice, e.g. running. We measure
        his vital parameters (e.g. heart_rate) constantly. Based on this vital parameters
        we want to generate music. We want to do this, by leveraging ChatGPT as an LLM
        that generates us code applicable for Sonic-Pi that is then live played and
        streamed to the user. 
        """
        self.your_task = """
        When the user is just beginning his exercise, he is not listening
        to any music yet. The key "current_sonic_pi_code" will therefore say no_code_yet.
        Your task then is to generate a new song that infinitely loops via generating
        the code for sonic-pi in the sonic-pi language that fits the "measured_parameters".
        Our idea is, that the user is constantly listening to what Sonic-Pi streams.
        We have a logic in our backend that defines, when the user has had a significant 
        change in pace. If that happend you will get a new request that will include the 
        song (i.e. the code) that the user is currenlty listening too as a value in the key
        "current_sonic_pi_code", so it will not say no_code_yet anymore. Your task is then
        to use this existing code as a baseline and adapt it to his newly "measured_parameters".
        Feel free to change up specific sections of the song for 
        a more dynamic experience, that could possible fit for a smooth transition 
        between the “current_sonic_pi_code” and the new one. Feel free to introduce 
        new instruments, new sample, new beats, or remove them. The user should 
        experience different songs during his activity.
        """
        self.example = """
        Sonic-Pi itself will run this following code:

            use_osc "localhost", 4560
            live_loop :executor do
                use_real_time
                code = sync "/osc*/execute_code"
                eval(code[0])
            end

            With this, the Sonic-Pi server is ready to await for generated code and 
            interpret and play it in real time. An example code for "current_sonic_pi_code"
            that is at least expected as your response, and that is then (unfiltered) sent 
            to Sonic-Pi via OSC is the following:

            use_bpm 116 

            live_loop :heartbeat do
                sample :bd_tek, rate: 1
                sleep 0.5
                sample :bd_tek, rate: 0.75
                sleep 0.5
            end

            live_loop :synth_rhythm do
                use_synth :tb303
                play :c3, release: 0.25, cutoff: rrand(70, 130) 
                sleep 0.25
                play :e3, release: 0.25, cutoff: rrand(70, 130)
                sleep 0.25
                play :g3, release: 0.25, cutoff: rrand(70, 130)
                sleep 0.25
                play :b3, release: 0.25, cutoff: rrand(70, 130)
                sleep 0.25
            end

            live_loop :ambient_effects do
                use_synth :prophet 
                play choose([:c2, :e2, :g2]), release: 3, cutoff: rrand(60, 120)
                sleep 8
            end

            Please make sure, that your newly generated code also adheres to such a format 
            as in the example "current_sonic_pi_code". As mentioned, you are of course free to
            generate music how you like. Be very creative! But, the code must work with
            our setup as it does in our example.
            IMPORTANT:
            Your response must only include your new generated Sonic-Pi code. Refrain from responding with any 
            other sentences, words, characters. Comments within the code must be omitted.
        """
        self.heart_rate = heart_rate
        self.song_genre = song_genre
        self.activity_type = activity_type
        self.current_sonic_pi_code = current_sonic_pi_code
        
    def set_sonic_pi_code(self, new_code):
        self.current_sonic_pi_code = new_code
    
    def get_sonic_pi_code(self):
        return self.current_sonic_pi_code
    
    def set_heart_rate(self, new_heart_rate):
        self.heart_rate = new_heart_rate

    def set_song_genre(self, new_song_genre):
        self.song_genre = new_song_genre

    def set_activity_type(self, new_activity_type):
        self.activity_type = new_activity_type
        
    def to_json(self):
        data = {
            "our_idea": self.our_idea.replace('\n', ' ').strip(),
            "your_task": self.your_task.replace('\n', ' ').strip(),
            "example": self.example.replace('\n', ' ').strip(),
            "measured_parameters": {
                "heart_rate": self.heart_rate,
                "song_genre": self.song_genre,
                "activity_type": self.activity_type
            },
            "current_sonic_pi_code": self.current_sonic_pi_code
        }
        return json.dumps(data, indent=2)  # dictionary to JSON string for pretty printing

