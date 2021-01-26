import pyttsx3
import keyboard


class TTSModule:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 140)
        self.engine.runAndWait()

    def say(self, line):
        self.engine.connect('started-word', self.onWord)
        self.engine.say(line)
        self.engine.runAndWait()

    def set_speech_rate(self, rate):
        self.engine.setProperty('rate', rate)

    def onWord(self, name, location, length):
        if keyboard.is_pressed("esc"):
            self.engine.stop()

