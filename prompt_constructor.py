import json

class PromptConstructor:
    def __init__(self, heart_rate, song_genre, current_sonic_pi_code):
        self.our_idea = """
        Our concept, PulseLL, synchronizes music with your pace. As users exercise, 
        the system measures their vital parameters, such as heart rate, and allows them 
        to select additional preferences, like song genre. The music is then constantly 
        and dynamically generated to match the intensity and rhythm of their activities.
        """
        self.your_task = """
        Your task is to generate code in the Sonic Pi live coding environment. 
        It is essential that your generated code is runnable and compilable by Sonic Pi. 
        The music the user is currently listening to is defined in “current_sonic_pi_code”. 
        If this key is “no_code_yet” the user has just started his exercice, 
        no music has been generated yet, and you must generate it from new based on 
        the content in “measured_parameters”. If this key already holds Sonic Pi 
        code you must use it as a baseline and change up this existing code based on 
        “measured_parameters” Feel free to change up specific sections of the song for 
        a more dynamic experience, that could possible fit for a smooth transition 
        between the “current_sonic_pi_code” and the new one. Feel free to introduce 
        new instruments, new sample, new beats, or remove them. The user should 
        experience different songs during his activity. Your response must only 
        include your new generated Sonic Pi code. Refrain from responding with any 
        other sentences, words, characters.
        """
        self.heart_rate = heart_rate
        self.song_genre = song_genre
        self.current_sonic_pi_code = current_sonic_pi_code
        
    def set_sonic_pi_code(self, new_code):
        self.current_sonic_pi_code = new_code
    
    def get_sonic_pi_code(self):
        return self.current_sonic_pi_code
    
    def set_heart_rate(self, new_heart_rate):
        self.heart_rate = new_heart_rate
        
    def to_json(self):
        data = {
            "our_idea": self.our_idea.replace('\n', ' ').strip(),
            "your_task": self.your_task.replace('\n', ' ').strip(),
            "measured_parameters": {
                "heart_rate": self.heart_rate,
                "song_genre": self.song_genre
            },
            "current_sonic_pi_code": self.current_sonic_pi_code
        }
        return json.dumps(data, indent=2)  # dictionary to JSON string for pretty printing

