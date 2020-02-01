from config.updateConfig import UpdateConfig


updateCofig = UpdateConfig()
CONF = updateCofig.getConfig()

spftCONF = {
    "task": {
        "name": "SpFT",
        "language": ["English", "German"][0],
        # in seconds
        "duration": {"versionMain": 10, "versionDemo": 10, "versionDebug": 2},
    },
    "instructions": {
        "text": "You will be presented with 20 tongue twisters, one at a time. Read the sentence, and when you're ready, press 'enter' to start. Read out loud the sentence as fast and accurately as you can in 10 seconds before the sentence disappears.",
        "startPrompt": "Press any key to continue. Press q to quit.",
        "continue": "Press enter to start.",
        "alarm": "horn.wav",
        "questionnaireReminder": "answerQuestionnaire.wav"
    },
    "pause": {
        "backgroundColor": "black",
        "duration": 2,
    },
    "stimuli": {
        "timeHeight": 1,
        "timeWidth": 10,
        "timeColor": "green",
        "timeBackgroundColor": "grey",
        "timePos": (0, -CONF["screen"]["size"][1]/2+3),
        "sentencePos": (0, 0),
        "sentenceHeight": 0.5,
        "exampleSentence": "How much wood could a woodchuck chuck if a woodchuck could chuck wood?"
    }
}

spftTriggers = {
    "StartRecording": 10,
    "EndTime": 11
}

# additional triggers
CONF["trigger"]["labels"]["StartRecording"] = 0x0A
CONF["trigger"]["labels"]["EndTime"] = 0x0B


updateCofig.addContent(spftCONF)
updateCofig.addTriggers(spftTriggers)
CONF = updateCofig.getConfig()
