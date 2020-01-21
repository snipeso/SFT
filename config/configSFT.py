import os
from config.configSession import CONF


CONF.update({
    "task": {
        "name": "SFT",
        # TODO: make this setable with terminal
        "language": ["English", "German"][0],
        "duration": 10,  # in seconds
    },
    "instructions": {
        "text": "You will be presented with 20 tongue twisters, one at a time. Read the sentence, and when you're ready, press 'enter' to start. Read out loud the sentence as many times as you can in 10 seconds before the sentence disappears.",
        "startPrompt": "Press any key to continue. Press q to quit.",
        "continue": "Press enter to start."
    },
    "pause": {
        "backgroundColor": "black",
        "duration": 2,
    },
    "sounds": {
        "alarm": "horn.wav",
    },
    "stimuli": {
        "timeHeight": 1,
        "timeWidth": 10,
        "timeColor": "green",
        "timeBackgroundColor": "grey",
        "timePos": (0, -CONF["screen"]["size"][1]/2+3)
    }
})


# additional triggers
CONF["trigger"]["labels"]["StartRecording"] = 0x0A
CONF["trigger"]["labels"]["EndTime"] = 0x0B
