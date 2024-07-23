from pythonosc import udp_client
import os


"""
In Sonic-Pi one must run the following code first:

use_osc "localhost", 4560

live_loop :executor do
  use_real_time
  code = sync "/osc*/execute_code"
  eval(code[0])
end
"""

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'current_sonic_pi_code.txt')

# Simply read the code from the file
with open(file_path, 'r') as file:
    sonic_pi_code = file.read()
    print(sonic_pi_code)
    
ip = "127.0.0.1"
port = 4560
# Send the code to Sonic Pi
client = udp_client.SimpleUDPClient(ip, port)
client.send_message("/execute_code", [sonic_pi_code])

