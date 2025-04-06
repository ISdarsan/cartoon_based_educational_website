from gtts import gTTS
import os

def text_to_audio(text, output_filename):
    tts = gTTS(text=text, lang='en')
    tts.save(output_filename)
    return output_filename
