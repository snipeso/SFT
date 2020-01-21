import os
from psychopy import core, event, microphone

microphone.switchOn()
Mic = microphone.AdvAudioCapture()
 # Mic = core.microphone.switchOn(sampleRate=48000)

filepath = os.path.join("output", "recordings")

if not os.path.exists(filepath):
    os.makedirs(filepath)

filename = os.path.join("filepath", "test1.wav")
f = Mic.record(3, filename)

core.wait(3)
Mic.reset()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
