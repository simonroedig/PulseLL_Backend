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
        # but this does is not really useful actually
        silent_code = """
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
        # Send the OSC message to stop all sound and processes
        self.client.send_message("/execute_code", [silent_code])

    def stop_all(self):
        # this does not work yet
        sonic_pi_code = """
        # Stop all existing live loops by redefining them as stopped
        live_loop :heartbeat do
        stop
        end

        live_loop :synth_rhythm do
        stop
        end

        live_loop :ambient_effects do
        stop
        end
        """
        self.client.send_message("/execute_code", [sonic_pi_code])

    def stop_execution(self):
        # Send a stop command to Sonic Pi
        self.client.send_message("/stop_execution", [])

    @staticmethod
    def _clean_sonic_pi_code(code):
        # Remove the ```ruby and ``` at the start and end
        if code.startswith('```ruby'):
            code = code[len('```ruby'):].strip()
        if code.startswith('```sonic-pi'):
            code = code[len('```sonic-pi'):].strip()
        if code.startswith('```sonic_pi'):
            code = code[len('```sonic_pi'):].strip()
        if code.endswith('```'):
            code = code[:-len('```')].strip()
        return code
    
