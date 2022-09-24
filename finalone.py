######## IMPORTS ##########
import sounddevice as sd
from scipy.io.wavfile import write
import librosa
import numpy as np
from tensorflow.keras.models import load_model
import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import os
import pywhatkit
import pyjokes
import ctypes



engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning Sir !")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon Sir !")

    else:
        speak("Good Evening Sir !")

        # assname =("TRAVIS")
    speak("I am your assistant cloudy!")
    # speak(assname)
    speak("How can i Help you, Sir")


def takeCommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:

        print("Listening...")
        # r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        print(e)
        print("Unable to Recognize your voice.")
        return "none"

    return query

def bot():
 #while True:
    
    query = takeCommand().lower()

    if 'play' in query:
        song = query.replace('play', '')
        speak('playing' + song)
        pywhatkit.playonyt(song)
    elif 'the time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"sir, the time is {strTime}")

    elif 'open youtube' in query or 'go to youtube' in query:
        speak("opening youtube")
        webbrowser.open("youtube.com")
    elif 'open chrome' in query or 'open google chrome ' in query:
        speak("opening google chrome")
        app_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        os.startfile(app_path)

    elif 'open spotify' in query:
        speak("opening spotify")
        os.system("spotify")

    #elif 'open whatsapp' in query:
     #   speak("opening whatsapp")
      #s  os.system("whatsapp")

    elif 'how are you' in query:
        speak("I am fine, Thank you")
        speak("How are you, Sir")
        speak("It's good to know that you're fine")

    elif "change my name to" in query:
        query = query.replace("change my name to", "")
        uname = query
        speak("your name is changed to {assname}")

    elif "what's your name" in query or "What is your name" in query:
        speak("My friends call me")
        speak(uname)
        print("My friends call me", uname)

    elif 'thank you' in query or 'thanks' in query or 'exit' in query:
        speak("Thanks for giving me your time")
        exit()
    elif 'search' in query:
        query = query.replace("search", "")
        webbrowser.open(query)
    elif 'lock' in query:
        speak("locking your device")
        ctypes.windll.user32.LockWorkStation()


    elif "how are you" in query:
        speak("I'm fine, how are you ")
        speak()
        if 'not' in query:
            speak("your day is going to be great")
        else:
            speak("very happy to know that you are doing good")


    elif 'joke' in query:
        joke = pyjokes.get_joke(language='en', category='neutral')
        speak(joke)
    elif 'hi ' in query:
        speak("hello ")
    elif 'stop' in query:
        speak("stopping")
        bot()
        exit()
    else:
        speak("I CAN'T DO THAT!! ")


####### ALL CONSTANTS #####
fs = 44100
seconds = 2
filename = "prediction.wav"
class_names = ["Wake Word NOT Detected", "Wake Word Detected"]

##### LOADING OUR SAVED MODEL and PREDICTING ###
model = load_model("saved_model/WWD2.h5")

print("Prediction Started: ")
i = 0
while True:
    print("Say Now: ")
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    write(filename, fs, myrecording)

    audio, sample_rate = librosa.load(filename)
    mfcc = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
    mfcc_processed = np.mean(mfcc.T, axis=0)

    prediction = model.predict(np.expand_dims(mfcc_processed, axis=0))
    if prediction[:, 1] > 0.97:
        print(f"Wake Word Detected for ({i})")
        print("Confidence:", prediction[:, 1])
        i += 1
        wishMe()
        bot()
        
    
    else:
        print("Wake Word NOT Detected")
        print("Confidence:", prediction[:, 0])
