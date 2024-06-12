import os
import openai
from dotenv import load_dotenv
import time
import speech_recognition as sr
import pyttsx3
import numpy as np
from gtts import gTTS

load_dotenv('/home/thalamus/configs/.env')

openai.api_key = os.getenv('OPENAI_API_KEY')
language = 'en'
model = 'gpt-4'

r = sr.Recognizer()
engine = pyttsx3.init()
voice = engine.getProperty('voices')[0]  
engine.setProperty('voice', voice.id)

def listen_for_wake_word(source):
    print("Listening for 'Hey'...")
    while True:
        try:
            audio = r.listen(source)
            text = r.recognize_google(audio)
            if "hey" in text.lower():
                print("Wake word detected.")
                engine.say(np.random.choice(["Hello", "Hi there"]))
                engine.runAndWait()
                break
        except sr.UnknownValueError:
            print("Could not understand audio, listening again...")
            time.sleep(2)

def listen_and_respond(source):
    print("Listening for a command...")
    while True:
        try:
            audio = r.listen(source)
            text = r.recognize_google(audio)
            if text:
                print(f"You said: {text}")
                response = openai.ChatCompletion.create(
                    model=model, messages=[{"role": "user", "content": text}]
                )
                response_text = response.choices[0].message.content
                print("Response:", response_text)
                engine.say(response_text)
                engine.runAndWait()
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Error: {e}")

with sr.Microphone() as source:
    listen_for_wake_word(source)
    listen_and_respond(source)
