import speech_recognition as sr


class CouldNotRecognizeError(Exception):
    def __init__(self, message):
        self.message = message


class ServerRequestError(Exception):
    def __init__(self, message):
        self.message = message


class SRModule:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 0.5
        self.microphone = sr.Microphone()
        self.audio = None
        self.recognized_text = None
        self.strategies = {
            'spinx': self._recognize_spinx,
            'google': self._recognize_google,
            'houndify': self._recognize_houndify
        }

    def adjust_mic(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=5)

    def obtain_audio(self):
        with self.microphone as source:
            self.audio = self.recognizer.listen(source, timeout=3)

    def _recognize_spinx(self, id, key):
        try:
            recognized_text = self.recognizer.recognize_sphinx(self.audio)
        except sr.UnknownValueError:
            raise CouldNotRecognizeError("Sphinx could not understand audio")
        except sr.RequestError as e:
            raise ServerRequestError("Sphinx error; {0}".format(e))
        return recognized_text

    def _recognize_google(self, id, key):
        try:
            recognized_text = self.recognizer.recognize_google(self.audio)
        except sr.UnknownValueError:
            raise CouldNotRecognizeError("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            raise ServerRequestError("Could not request results from Google Speech Recognition service; {0}".format(e))
        return recognized_text

    def _recognize_houndify(self, id, key):
        HOUNDIFY_CLIENT_ID = id  # "dVdGP0yoHHRo7tWi2dJ-CQ=="  # Houndify client IDs are Base64-encoded strings
        HOUNDIFY_CLIENT_KEY = key  # "p2XmAMsymEhyqvJq0W4Irv21RGB6O1xppyV4PL7-WeR-gPIUZBETvxkgJtIx1SA0SuAHK7x2YmI0AWF-5UUiHA=="  # Houndify client keys are Base64-encoded strings
        try:
            recognized_text = self.recognizer.recognize_houndify(self.audio, client_id=HOUNDIFY_CLIENT_ID,
                                                                 client_key=HOUNDIFY_CLIENT_KEY)
        except sr.UnknownValueError:
            raise CouldNotRecognizeError("Houndify could not understand audio")
        except sr.RequestError as e:
            raise ServerRequestError("Could not request results from Houndify service; {0}".format(e))
        return recognized_text

    def recognize(self, engine='google', id=None, key=None):
        if self.audio is None:
            raise ValueError("No audio given yet")
        self.recognized_text = self.strategies[engine](id, key)


if __name__ == '__main__':
    srec = SRModule()
    srec.obtain_audio()
    srec.recognize('houndify', 'dVdGP0yoHHRo7tWi2dJ-MQ==',
                   'p2XmAMsymEhyqvJq0W4Irv21RGB6O1xppyV4PL7-WeR-gPIUZBETvxkgJtIx1SA0SuAHK7x2YmI0AWF-5UUiHA==')
