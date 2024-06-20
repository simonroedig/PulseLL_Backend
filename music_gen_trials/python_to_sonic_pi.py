from pythonosc import udp_client


"""
In Sonic-Pi one must run the following code first:

use_osc "localhost", 4560

live_loop :executor do
  use_real_time
  code = sync "/osc*/execute_code"
  eval(code[0])
end
"""

# Simply read the code from the file
file_path = r"current_sonic_pi_code.txt"
with open(file_path, 'r') as file:
    sonic_pi_code = file.read()
    print(file)
    
ip = "127.0.0.1"
port = 4560
# Send the code to Sonic Pi
client = udp_client.SimpleUDPClient(ip, port)
client.send_message("/execute_code", [sonic_pi_code])

