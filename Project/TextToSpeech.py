from gtts import gTTS
from playsound import playsound


class TextToSpeech:

    @staticmethod
    def read_text(text, lang="de"):

        tts = gTTS(text, lang=lang)
        file_name = 'chatbot.mp3'
        tts.save(file_name)
        playsound(file_name)
