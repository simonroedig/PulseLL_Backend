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
        to any music yet. The key "current_sonic_pi_code" will therefore say "no_code_yet".
        Your task then is to generate a new song that infinitely loops via generating
        the code for sonic-pi in the sonic-pi language that fits the "measured_parameters".
        Our idea is, that the user is constantly listening to what Sonic-Pi streams.
        We have a logic in our backend that defines, when the user has had a significant 
        change in pace (i.e. different mean heart_rate). If that happend you will get a new request that will include the 
        song (i.e. the code) that the user is currenlty listening too as a value in the key
        "current_sonic_pi_code", so it will not say "no_code_yet" anymore. Your task is then
        to use this existing code as a baseline and adapt it to the newly "measured_parameters".
        This means to change up specific sections of the song for 
        a more dynamic experience, that could possible fit for a smooth transition 
        between the “current_sonic_pi_code” and the new one you are outputting. Feel free to introduce 
        new instruments, new samples, new beats, new loops etc. or remove them. If an instrument/beat/sample/loop
        should be removed simply reduce this instruments amplitude to 0 instead 
        of ommiting it from the code. You must use “current_sonic_pi_code” as baseline if it holds code
        and is not "no_code_yet".
        The user should fell like experiencing different song dynamic during his activity that
        fit his measured heart_rate.
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
        interpret and play it in real time. Example code for "current_sonic_pi_code"
        that is at least expected as your response, and that is then (unfiltered) sent 
        to Sonic-Pi via OSC are the following. 
        This example fits the techno genre and the activity running with a mean heart of 143:

        use_bpm 143

        live_loop :kick do
        sample :bd_haus, rate: 0.8, amp: 1.5
        sleep 1
        end

        live_loop :bassline do
        use_synth :tb303
        notes = (ring :e1, :e1, :g1, :a1)
        play notes.tick, release: 0.2, cutoff: rrand(70, 120), res: 0.7, amp: 0.8
        sleep 0.25
        end

        live_loop :hihat do
        sample :drum_cymbal_closed, rate: 1.5, amp: 0.6 if one_in(2)
          sleep 0.25
        end

        
        Please make sure, that your newly generated code also adheres to such a format. As mentioned, you are of course free to
        generate music how you like. Be very creative! But, the code must work with
        our setup as it does in our examples.
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
