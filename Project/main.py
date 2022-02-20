import pyttsx3

from Project.TextToSpeech import TextToSpeech

if __name__ == '__main__':
    text = 'Hallo Sabine!'

    voice_fr = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_FR-FR_HORTENSE_11.0"
    voice_en = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
    voice_de = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_DE-DE_HEDDA_11.0"

    converter = pyttsx3.init()

    # Sets speed percent
    # Can be more than 100
    converter.setProperty('rate', 150)
    # Set volume 0-1
    converter.setProperty('volume', 0.7)
    converter.setProperty('voice', voice_de)
    converter.say(text)
    converter.runAndWait()

    voices = converter.getProperty('voices')

