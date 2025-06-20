"""
PDF Translator & Audio Generator

A Streamlit app to extract text from a PDF, translate it from English to Hindi, and generate audio from the translated text.
"""
import streamlit as st
import pymupdf
from transformers import pipeline
from gtts import gTTS
import os
import base64
import re

# Helper function to split text into chunks
def split_text(text, max_length=400):
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_length:
            current_chunk += (" " if current_chunk else "") + sentence
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = sentence
    if current_chunk:
        chunks.append(current_chunk)
    return chunks

st.set_page_config(page_title="PDF Translator & Audio Generator", layout="centered")
st.title("PDF Translator & Audio Generator")
st.markdown("""
Welcome to the PDF Translator & Audio Generator! 
Upload a PDF file, and I will extract the text, translate it to Hindi, and generate an audio file of the translated text.
""")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    with open("uploaded_file.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("PDF uploaded successfully!")
    st.subheader("1. Extracting Text from PDF")
    text = ""
    try:
        doc = pymupdf.open("uploaded_file.pdf")
        for page in doc:
            text += page.get_text()
        st.write("Text extracted:")
        st.info(text[:500] + "...")
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        text = ""
    if text:
        st.subheader("2. Translating Text to Hindi")
        try:
            translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-hi")
            lines = text.splitlines()
            translated_lines = []
            for line in lines:
                if line.strip() == "":
                    translated_lines.append("")
                else:
                    chunks = split_text(line, max_length=400)
                    translated_chunks = []
                    for chunk in chunks:
                        translated = translator(chunk)[0]['translation_text']
                        translated_chunks.append(translated)
                    translated_lines.append(" ".join(translated_chunks))
            translated_text = "\n".join(translated_lines)
            st.write("Translated text (Hindi):")
            st.success(translated_text)
        except Exception as e:
            st.error(f"Error translating text: {e}")
            translated_text = ""
        if translated_text:
            st.subheader("3. Generating Audio from Translated Text")
            audio_file_path = "translated_audio.mp3"
            try:
                tts = gTTS(text=translated_text, lang='hi')
                tts.save(audio_file_path)
                st.success("Audio generated successfully!")
                with open(audio_file_path, "rb") as audio_file:
                    audio_bytes = audio_file.read()
                    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
                st.markdown(f"""<audio controls src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3"></audio>""", unsafe_allow_html=True)
                st.write("If the audio does not play automatically, you can download it:")
                with open(audio_file_path, "rb") as file:
                    st.download_button(
                        label="Download Audio",
                        data=file,
                        file_name="translated_audio.mp3",
                        mime="audio/mp3"
                    )
            except Exception as e:
                st.error(f"Error generating or playing audio: {e}")
        else:
            st.warning("Translation failed, cannot generate audio.")
    else:
        st.warning("Text extraction failed, cannot proceed with translation.")
else:
    st.info("Please upload a PDF file to get started.")
if os.path.exists("uploaded_file.pdf"):
    os.remove("uploaded_file.pdf")
if os.path.exists("translated_audio.mp3"):
    os.remove("translated_audio.mp3") 