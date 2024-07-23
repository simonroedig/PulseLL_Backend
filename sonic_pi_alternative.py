from pythonosc import udp_client
from icecream import ic

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

class SonicPiAlternative:
    def __init__(self, port=4560, ip="127.0.0.1"):
        self.port = port
        self.ip = ip
        # initialize the client
        self.client = udp_client.SimpleUDPClient(self.ip, self.port)
        
    def send_code(self, code):
        clean_code = self._clean_sonic_pi_code(code)
        ic(clean_code)
        self.client.send_message("/execute_code", [clean_code])
        
    @staticmethod
    def _clean_sonic_pi_code(code):
        # Remove the ```ruby and ``` at the start and end
        if code.startswith('```ruby'):
            code = code[len('```ruby'):].strip()
        if code.endswith('```'):
            code = code[:-len('```')].strip()
        return code
