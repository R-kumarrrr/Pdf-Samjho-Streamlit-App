import subprocess
subprocess.check_call(["pip", "install", "transformers"])
subprocess.check_call(["pip", "install", "transformers", "datasets"])
subprocess.check_call(["pip", "install", "PyMuPDF"])
subprocess.check_call(["pip", "install", "gTTS"])

from transformers import pipeline, set_seed
import pymupdf  

doc = pymupdf.open("India_Paragraph.pdf")  
for page in doc:  
    text = page.get_text() 

translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-hi")
translated = translator(text)
print(translated)

from gtts import gTTS
tts = gTTS(text=translated[0]['translation_text'], lang='hi')
tts.save("translated.mp3")

import os
os.system("afplay translated.mp3")