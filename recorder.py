import datetime
import os

from psychopy import microphone


class Recorder:
    def __init__(self, CONF):
        "Initialize microphone"
        path = os.path.join("output", "recordings",
                            CONF["participant"] + "_" + CONF["session"])
        if not os.path.exists(path):
            os.makedirs(path)
        self.path = path
        self.CONF = CONF

        microphone.switchOn()
        self.mic = microphone.AdvAudioCapture()

    def set_filename(self, trial):
        # Determines name for output file
        self.filename = "{}_{}_{}_{}_{}".format(
            self.CONF["participant"],
            self.CONF["session"],
            self.CONF["task"]["name"],
            trial,
            datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"))
        self.filepath = os.path.join(self.path, self.filename)

        return self.filename

    def play(self):
        self.mic.record(self.CONF["task"]["duration"], filename=self.filepath)
