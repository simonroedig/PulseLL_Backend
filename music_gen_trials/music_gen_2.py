from psonic import *
import time

set_server_parameter('127.0.0.1', 4560)  

send_message('/trigger/prophet', 70, 100, 8)

'''
live_loop :foo do
  use_real_time
  a, b, c = sync "/osc*/trigger/prophet"
  synth :prophet, note: a, cutoff: b, sustain: c
end
'''