"""
In Sonic-Pi one must run the following code first:

use_osc "localhost", 4560

live_loop :executor do
  use_real_time
  code = sync "/osc*/execute_code"
  eval(code[0])
end
"""

import os
from pythonosc import udp_client
from icecream import ic

class SonicPi:
    def __init__(self, port=4560, ip="127.0.0.1"):
        self.port = port
        self.ip = ip
        # initialize the client
        self.client = udp_client.SimpleUDPClient(self.ip, self.port)
        
    def send_code(self, code):
        clean_code = self._clean_sonic_pi_code(code)
        ic(clean_code)
        self.client.send_message("/execute_code", [clean_code])

    def send_silent_code(self):
        # i just send some normal sonic pi code with amplitude 0
        # with this sonic pi keeps running but will not play any sound
        silent_code = """
        use_bpm 116

        live_loop :heartbeat do
        sample :bd_tek, rate: 1, amp: 0
        sleep 0.5
        sample :bd_tek, rate: 0.75, amp: 0
        sleep 0.5
        end

        live_loop :synth_rhythm do
        use_synth :tb303
        play :c3, release: 0.25, cutoff: rrand(70, 130), amp: 0
        sleep 0.25
        play :e3, release: 0.25, cutoff: rrand(70, 130), amp: 0
        sleep 0.25
        play :g3, release: 0.25, cutoff: rrand(70, 130), amp: 0
        sleep 0.25
        play :b3, release: 0.25, cutoff: rrand(70, 130), amp: 0
        sleep 0.25
        end

        live_loop :ambient_effects do
        use_synth :prophet
        play choose([:c2, :e2, :g2]), release: 3, cutoff: rrand(60, 120), amp: 0
        sleep 8
        end
        """
        # Send the OSC message to stop all sound and processes
        self.client.send_message("/execute_code", [silent_code])

    def stop_all(self):
        self.client.send_message("/execute_code", "stop_me_pls")

        
    @staticmethod
    def _clean_sonic_pi_code(code):
        # Remove the ```ruby and ``` at the start and end
        if code.startswith('```ruby'):
            code = code[len('```ruby'):].strip()
        if code.startswith('```sonic-pi'):
            code = code[len('```sonic-pi'):].strip()
        if code.endswith('```'):
            code = code[:-len('```')].strip()
        return code
    
#SonicPi().stop_all()


