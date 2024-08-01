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

        If the key "current_sonic_pi_code" does not say "no_code_yet", and holds some Sonic-Pi code,
        the user is already listening to this song in "current_sonic_pi_code" and has started his workout.

        Your task then is to generate a new song that infinitely loops via generating
        the code for sonic-pi in the sonic-pi language that fits the "measured_parameters".

        Please refer to "example_explanation" and the provided examples in "example_techno_song_genre_and_running_activity",
        "example_rock_song_genre_and_hiking_activity", and "example_dubstep_song_genre_and_cycling_activity".

        We have a logic in our backend that defines, when the user has had a significant 
        change in pace. If that happend you will get a new request that will include the 
        song (i.e. the code) that the user is currenlty listening too as a value in the key
        "current_sonic_pi_code", so it will not say "no_code_yet" anymore. Your task is then
        to use this existing code as a baseline and adapt it to his newly "measured_parameters" that you see.

        Feel free to change up specific sections of the song for 
        a more dynamic experience, that could possible fit for a smooth transition 
        between the “current_sonic_pi_code” and the new one you are generating. Feel free to introduce 
        new instruments, new sample, new beats, or remove them. The user should 
        experience different songs during his activity.
        """
        self.your_task_intro = """
        The user has now just begun his exercise. Your task now is to generate a simple intro song that fits the "measured_parameters".
        Please refer to "example_explanation" and "example_intro" for a simple example of an intro song.
        It should not introduce notes or be too melodic. Rather drums and samples. Let it be simple and not too complex.
        """

        self.example_explanation = """
        Sonic-Pi itself will run this following code:

        use_osc "localhost", 4560
        live_loop :executor do
            use_real_time
            code = sync "/osc*/execute_code"
            eval(code[0])
        end

        With this, the Sonic-Pi server is ready to await for generated code and 
        interpret and play it in real time. The following example keys
        will show you example codes that is at least expected as your response
        in terms of complexity, and that is then (unfiltered) sent 
        to Sonic-Pi via OSC.

        Please make sure, that your newly generated code also adheres to such a format 
        as in those examples in terms of compilability. As mentioned, you are of course free to
        generate music how you like but must fit the "measured_parameters". Be very creative! The code must work with
        our setup! Ensure the code will run correctly in Sonic-Pi. Your response must be ready to copy and paste
        into Sonic-Pi and runable without any errors!

        IMPORTANT:
        Your response must only include your new generated Sonic-Pi code. Refrain from responding with any 
        other sentences, words, characters. Comments within the code must be omitted.
        """
        self.example_techno_song_genre_and_running_activity_130_heartrate = """
        use_debug false
        use_bpm 130

        master = (ramp *range(0, 1, 0.01))
        kick_volume = 1
        bass_volume = 1
        revbass_volume = 1
        snare_volume = 0.5
        hats_volume = 0.5
        open_hats_volume = 1
        synth_volume = 1
        pad_volume = 1
        beep_volume = 0.5

        kick_cutoffs = range(50, 80, 0.5).mirror
        live_loop :kick do
        if (spread 1, 4).tick then
            sample :bd_tek, amp: master.look * kick_volume,
            cutoff: kick_cutoffs.look
        end
        sleep 0.25
        end

        define :snare do |amp|
        sample :sn_dolf, amp: amp, start: 0.15, finish: 0.35, rate: 0.7
        end

        live_loop :snares do
        sleep 1
        snare 1 * master.tick * snare_volume
        sleep 1
        end

        live_loop :snare_break do
        sync :snares
        sleep 15.75
        with_fx :reverb, mix: 0.3, room: 0.8 do
            with_fx :echo, mix: 0.4, decay: 12, phase: 0.75 do
            snare 0.5 * master.tick * snare_volume
            end
        end
        sleep 0.25
        end

        live_loop :hats do
        sync :kick
        if (spread 3, 8).tick then
            with_fx :rhpf, cutoff: 125, res: 0.8 do
            with_synth :pnoise do
                play :d1, amp: hats_volume * master.tick,
                attack: 0.05, decay: 0.08, release: 0.1
            end
            end
        end
        sleep 0.25
        end

        live_loop :noise_hats do
        sync :kick
        with_fx :slicer, mix: 1, phase: 0.25, pulse_width: 0.1 do
            with_fx :hpf, cutoff: 130 do
            with_synth :noise do
                play :d1, decay: 1, amp: master.tick * hats_volume
            end
            end
        end
        sleep 1
        end

        open_hats_cutoffs = range(120, 130, 0.5).mirror
        live_loop :open_hats do
        sync :kick
        with_fx :echo, amp: open_hats_volume * master.look,
        mix: 0.4, decay: 4, phase: 0.75 do
            with_fx :hpf, cutoff: open_hats_cutoffs.tick do
            with_fx :reverb, mix: 0.4, room: 0.8 do
                sleep 0.5
                sample :drum_cymbal_open, start: 0.2, finish: 0.3, amp: 0.5
                sleep 0.5
            end
            end
        end
        end

        bassline_rhythm = (ring 1, 0, 0, 0, 1, 0, 0, 0,
                        1, 0, 0.5, 0, 1, 0, 0.5, 0)
        bassline_notes = (stretch [:d1] * 12 + [:f1, :f1, :a1, :f1], 8)
        live_loop :bassline do
        sync :kick
        with_synth :fm do
            play bassline_notes.look,
            amp: master.look * bassline_rhythm.tick * bass_volume,
            attack: 0.03, divisor: 1, depth: 2.5
        end
        sleep 0.25
        end

        live_loop :revbassline do
        sync :snares
        sleep 7.5
        with_fx :pan, pan: -0.5 do
            with_synth :fm do
            play :d1, amp: bass_volume * master.tick,
                attack: 0.5, divisor: 0.5, depth: 6
            end
        end
        sleep 0.5
        end

        dchord = chord(:d2, :minor, num_octaves: 3)
        synth_cutoffs = range(60, 100, 0.5).mirror
        synth_rhythm = (ring 1.5, 1.5, 1)
        synth_transpositions = (stretch 0, 36) + (stretch -12, 6) + (stretch 12, 6)
        synth_phases = (stretch 0.75, 15) + [0.25]
        synth_pans = (ring -0.5, 0.5)
        live_loop :synth do
        sync :kick
        ch = invert_chord(dchord, rand_i(3))
        sleep synth_rhythm.tick
        with_fx :echo, amp: synth_volume * master.look, mix: 0.3,
        decay: 8, phase: synth_phases.look do
            with_fx :pan, pan: synth_pans.look do
            with_fx :reverb, room: 0.7, damp: 0.8 do
                with_synth_defaults attack: 0.05, release: 0.3 do
                with_transpose synth_transpositions.look do
                    with_synth :sine do
                    play_chord ch
                    end
                    cutoff = synth_cutoffs.look
                    with_fx :ixi_techno, cutoff_min: cutoff,
                    cutoff_max: cutoff - 30, phase: 1, res: 0.3 do
                    with_synth :dsaw do
                        play_chord ch, attack: 0.1
                    end
                    end
                end
                end
            end
            end
        end
        end

        dubpad_cutoffs = range(70, 100, 5).mirror
        dubpad_phases = (ring 8, 8, 8, 0.5)
        dubpad_mixes = (ring 0.5, 0.5, 0.5, 0)
        define :dubpad do |ch, amp|
        with_fx :echo, amp: amp, mix: dubpad_mixes.look,
        phase: 1.5, decay: 2 do
            with_fx :reverb, room: 0.8 do
            with_fx :ixi_techno, phase: dubpad_phases.tick, cutoff_min: 70 do
                with_synth :tb303 do
                with_synth_defaults attack: 0.1, release: 8,
                cutoff: dubpad_cutoffs.look, res: 0.5 do
                    play_chord ch
                    play_chord ch.map { |n| n + 0.3 }
                end
                end
            end
            end
        end
        end

        live_loop :pad do
        sync :snares
        dubpad dchord, master.tick * pad_volume
        sleep 16
        end

        beep_notes = (ring :d2, :d2, :f2, :e2, :d3, :g2)
        live_loop :beeps do
        sync :kick
        sleep 0.5
        with_fx :distortion do
            with_synth :beep do
            play beep_notes.tick, amp: beep_volume * master.look,
                decay: 0.2, release: 0.1
            end
        end
        end
        """
        self.example_rock_song_genre_and_hiking_activity = """
        tick   = 1.0
        half   = 0.5*tick
        quart  = 0.25*tick
        length = 32*tick

        in_thread(name: :letsgetloud) do
        sync :frame
        sleep length
        loop do
            drums_please_get_loud
        end
        end

        define :permanent_drumset do
        length.to_i.times.each_with_index do |_, i|
            sample :drum_cymbal_closed
            sleep tick
        end
        end

        define :drums_please_get_loud do
        length.to_i.times.each_with_index do |_, i|
            with_fx :level, amp: 2.0 do
            sample :drum_bass_hard
            sleep half
            sample :drum_snare_hard
            sample :drum_cymbal_hard if i % 8 == 3
            sleep half
            end
        end
        end

        define :monolithic_pattern do
        4.times do
            [:a3, :cs4, :a4, :cs4].each do |note|
            play note
            sleep quart
            end
        end
        
        2.times do
            [:ab3, :cs4, :ab4, :cs4].each do |note|
            play note
            sleep quart
            end
        end
        
        1.times do
            [:ab3, :cs4, 66, :cs4].each do |note|
            play note
            sleep quart
            end
        end
        
        1.times do
            [56, :cs4, 65, :cs4].each do |note|
            play note
            sleep quart
            end
        end
        
        
        4.times do
            [57, :d3, 66, :d3].each do |note|
            play note
            sleep quart
            end
        end
        
        4.times do
            [54, :b2, 66, :b2].each do |note|
            play note
            sleep quart
            end
        end
        end

        in_thread(name: :the_red_line) do
        sync :frame
        loop do
            with_synth :sine do
            monolithic_pattern
            end
        end
        end

        in_thread(name: :groll) do
        sync :frame
        sleep 16*tick
        loop do
            sleep 12*tick
            with_fx :level, amp: 2.0 do
            with_synth(:fm) do
                with_fx(:distortion) do
                4.times do
                    play 54.0
                    sleep quart
                    
                    play :b2
                    sleep quart
                    
                    #play 66.0
                    sleep quart
                    
                    play :b2
                    sleep quart
                end
                end
            end
            end
        end
        end

        in_thread(name: :screaming_git) do
        sync :frame
        sleep 48*tick
        loop do
            with_fx :level, amp: 0.4 do
            with_synth(:pulse) do
                with_fx(:distortion) do
                monolithic_pattern
                end
            end
            end
        end
        end

        in_thread(name: :supportive) do
        sync :frame
        sleep 16*tick
        loop do
            with_synth(:fm) do
            monolithic_pattern
            end
        end
        end

        in_thread(name: :supportive_dist) do
        sync :frame
        sleep 64*tick
        loop do
            with_synth(:fm) do
            with_fx(:distortion) do
                monolithic_pattern
            end
            end
        end
        end

        in_thread(name: :frame) do
        cue :frame
        loop do
            permanent_drumset
        end
        end
        """
        self.example_dubstep_song_genre_and_cycling_activity_140_heartrate = """
        use_bpm 140
        use_debug false

        basari = :bd_klub
        virveli = :sn_dolf
        haitsu = :perc_snap
        haitsu2 = :drum_cymbal_pedal

        with_fx :distortion, mix: 0.08 do
        with_fx :nrhpf, mix: 0.05 do

            live_loop :drumloop do
            at [1, 2, 4] do
                sample basari, amp: rrand(1, 1.5), rate: rrand(0.95, 1.05)
            end
            at [2.5, 6.5] do
                sample virveli, amp: rrand(0.6, 1), rate: rrand(0.95, 1.05)
                sleep 0.1
                with_fx :gverb, amp: 0.6, mix: 1, spread: 1, delay: 10 do
                sample virveli, amp: rrand(0.3, 0.5), rate: rrand(0.95, 1.05)
                end
            end
            at [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5] do
                with_fx :flanger, mix: 0.5, depth: 40, delay: 20, decay: 5, feedback: rrand(0.1, 1.0) do
                sample haitsu, amp: rrand(0.3, 0.5), rate: rrand(2.1, 2.2), pan: rrand(-0.25, 0.25)
                if one_in(10)
                    sleep 0.5
                    sample haitsu2, amp: rrand(0.6, 0.9), rate: rrand(1.1, 1.2), pan: rrand(-0.25, 0.25)
                end
                end
            end
            sleep 8
            end

            live_loop :bassolinjaus do
            with_fx :distortion, mix: 0.5, amp: 0.95 do
                3.times do
                at [0.5, 2.5, 4.5] do
                    with_fx :panslicer, smooth_up: 0.1, smooth_down: 0.1 do
                    sample :bass_dnb_f, pitch: 0, finish: 0.6
                    end
                end
                at [6.5] do
                    with_fx :panslicer, smooth_up: 0.1, smooth_down: 0.1 do
                    sample :bass_dnb_f, pitch: 0, finish: 0.6
                    end
                end
                sleep 8
                end
                n = 1
                at [0.5, 2.5, 4.5, 6.5] do
                with_fx :panslicer, mix: 1, wave: 3 do
                    with_fx :reverb, mix: 0.6, room: 0.2, amp: 2 do
                    7.times do
                        sample :bass_dnb_f, rate: n, finish: 0.1
                        n += 0.15
                        sleep 0.25
                    end
                    sample :bass_voxy_hit_c, rate: n, amp: 1
                    end
                end
                end
                sleep 8
            end
            end

            live_loop :randoming_pädi do
            kesto = [8, 10, 12].choose
            nuku = kesto / 2.0
            use_synth :hollow
            with_fx :hpf, cutoff: 75 do
                with_fx :reverb, room: 0.8, mix: 0.8, amp: 1 do
                nuotit = [:F4, :B4, :D4, :F5, :B5, :D5].choose
                play nuotit, attack: kesto / 3.0, release: kesto
                end
            end
            sleep nuku
            end

        end
        end
        """
        self.example_intro = """
        use_bpm 90

        live_loop :intro_drums do
        sample :bd_tek, amp: 2
        sleep 1
        sample :elec_snare, rate: 0.75, amp: 1.5
        sleep 1
        sample :elec_cymbal, rate: 1.5, amp: 1.5, release: 1.5
        sleep 1
        sample :drum_tom_lo_hard, rate: 0.5, amp: 1.5
        sleep 1
        end

        live_loop :ambient_fx do
        sample :ambi_choir, rate: 0.25, amp: 2, attack: 1, release: 3
        sleep 8
        end
        """
        self.heart_rate = heart_rate
        self.song_genre = song_genre
        self.activity_type = activity_type
        self.current_sonic_pi_code = current_sonic_pi_code
        self.intro_code = ""
        
    def set_sonic_pi_code(self, new_code):
        self.current_sonic_pi_code = new_code

    def set_intro_code(self, new_intro_code):
        self.intro_code = new_intro_code
    
    def get_sonic_pi_code(self):
        return self.current_sonic_pi_code
    
    def get_intro_code(self):
        return self.intro_code
    
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
            "example_explanation": self.example_explanation.replace('\n', ' ').strip(),
            "example_techno_song_genre_and_running_activity_130_heartrate": self.example_techno_song_genre_and_running_activity_130_heartrate.replace('\n', ' ').strip(),
            "example_rock_song_genre_and_hiking_activity": self.example_rock_song_genre_and_hiking_activity.replace('\n', ' ').strip(),
            "example_dubstep_song_genre_and_cycling_activity_140_heartrate": self.example_dubstep_song_genre_and_cycling_activity_140_heartrate.replace('\n', ' ').strip(),
            "example_intro": self.example_intro.replace('\n', ' ').strip(),
            "measured_parameters": {
                "heart_rate": self.heart_rate,
                "song_genre": self.song_genre,
                "activity_type": self.activity_type
            },
            "current_sonic_pi_code": self.current_sonic_pi_code
        }
        return json.dumps(data, indent=2)  # dictionary to JSON string for pretty printing
    
    def to_json_only_intro(self):
        data = {
            "our_idea": self.our_idea.replace('\n', ' ').strip(),
            "your_task_intro": self.your_task_intro.replace('\n', ' ').strip(),
            "example_explanation": self.example_explanation.replace('\n', ' ').strip(),
            "example_intro": self.example_intro.replace('\n', ' ').strip(),
            "measured_parameters": {
                "heart_rate": self.heart_rate,
                "song_genre": self.song_genre,
                "activity_type": self.activity_type
            },
        }
        return json.dumps(data, indent=2)  # dictionary to JSON string for pretty printing
