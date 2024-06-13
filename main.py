import os
import openai
from dotenv import load_dotenv
import time
import speech_recognition as sr
import pyttsx3
import numpy as np
from gtts import gTTS

# Load environment variables from .env file
load_dotenv('/home/thalamus/configs/.env')

# Set up OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Text-to-Speech settings
language = 'en'
model = 'gpt-4'

# Initialize speech recognition and text-to-speech engines
r = sr.Recognizer()
engine = pyttsx3.init()
voice = engine.getProperty('voices')[0]  # Adjust index based on your preferred voice
engine.setProperty('voice', voice.id)

# List all available microphones and find the index of the USB microphone
mic_list = sr.Microphone.list_microphone_names()
print("Available microphones:")
for index, name in enumerate(mic_list):
    print(f"{index}: {name}")

# Find the index of your USB microphone
mic_index = None
for index, name in enumerate(mic_list):
    if "USB PnP Sound Device" in name:  # Adjust this string to match your USB microphone name
        mic_index = index
        break

if mic_index is not None:
    print(f"Using microphone: {mic_list[mic_index]} (index: {mic_index})")
else:
    print("USB Microphone not found. Please check the connection.")
    exit(1)

greetings = [f"whats up",
             "yeah?",
             "Well, hello there",
             f"Ahoy there",
             f"Bonjour, Monsieur" ]

def listen_for_wake_word(source):
    print("Listening for 'Hey'...")
    while True:
        try:
            audio = r.listen(source)
            text = r.recognize_google(audio)
            if "hey" in text.lower():
                print("Wake word detected.")
                engine.say(np.random.choice(greetings))
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
            print(f"Error with the speech recognition service: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

with sr.Microphone(device_index=mic_index) as source:
    print("Adjusting for ambient noise, please wait...")
    r.adjust_for_ambient_noise(source)
    listen_for_wake_word(source)
    listen_and_respond(source)
