import os
import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import python_weather
from flask import Flask, request, jsonify

app = Flask(__name__)

# Initialize speech engine
engine = pyttsx3.init()
recognizer = sr.Recognizer()

# Configuration (use environment variables in Railway)
WEATHER_CITY = os.getenv("WEATHER_CITY", "New York")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Optional

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            return command
        except sr.UnknownValueError:
            return ""

def handle_command(command):
    if "play" in command:
        song = command.replace("play", "").strip()
        pywhatkit.playonyt(song)
        return f"Playing {song} on YouTube"
    
    elif "wikipedia" in command:
        query = command.replace("wikipedia", "").strip()
        summary = wikipedia.summary(query, sentences=2)
        return f"According to Wikipedia: {summary}"
    
    elif "weather" in command:
        client = python_weather.Client(format=python_weather.IMPERIAL)
        weather = client.find(WEATHER_CITY)
        return f"Weather in {WEATHER_CITY}: {weather.current.temperature}°F, {weather.current.sky_text}"
    
    elif "exit" in command:
        return "Goodbye!"
    
    else:
        return "I didn't understand that command."

@app.route('/assist', methods=['POST'])
def assist():
    command = request.json.get('command', '')
    response = handle_command(command)
    return jsonify({"response": response})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
