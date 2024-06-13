from FoxDot import *

# Setting the tempo
Clock.bpm = 130

# Defining the bass line
b1 >> sawbass(var([0, 2, 3, 4], 4), dur=1/4, oct=4, cutoff=400, pan=(-0.5, 0.5))

# Adding a rhythmic drum pattern
d1 >> play('X-o-', sample=2)

# Adding hi-hats
h1 >> play('----[---]', sample=3)

# Lead synth line
p1 >> pluck([0, 1, 2, 3], dur=1/2, oct=6, room=1, mix=0.3).every(8, "jump", cycle=4)

# Adding some effects to the lead line every 8 cycles
p1.every(8, "offadd", 4, dur=3)

# Adding a secondary melody with some echo
p2 >> blip([1, 2, 3, 5, 4], dur=3/4, sus=2, room=1, mix=0.2, echo=0.5, echotime=3)

# Additional percussion elements
d2 >> play('(X )( X)O ', rate=0.5)

# Overlay snappy noises
sn >> play('I', dur=1, sample=2, pan=1)

# Create dynamics by gradually introducing instruments
Group(b1, d1, h1, p1, p2, d2, sn).spread()

# Schedule changes in parameters or patterns
def change_music():
    b1.cutoff = var([300, 500], 8)
    d2.rate = var([0.5, 1], 16)
    p1.mix = var([0.1, 0.4], 12)

# Applying changes every 10 seconds
Clock.future(10, change_music)

# Start the session
Clock.start()
