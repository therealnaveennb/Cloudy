import sounddevice as sd
from scipy.io.wavfile import write
from tensorflow.keras.models import load_model
import speech_recognition as sr
import numpy as np
import librosa
#import pyttsx3
import speech_recognition as sr
from gtts import gTTS
import os
import time
import playsound
import datetime
import pywhatkit
import webbrowser
import subprocess 

global assname
assname ="Cloudy"

def speak(audio):
    tts = gTTS(text=audio, lang='en', slow=False)
    filename = r'voice.mp3'
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if( hour >= 0 and hour < 12):
        speak("Good Morning Sir !")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon Sir !")

    else:
        speak("Good Evening Sir !")

    
    speak("I am your assistant!")
    speak(assname)
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
        print(f"you said: {query}\n")

    except Exception as e:
        print(e)
        print("Unable to Recognize your voice.")
        return "none"

    return query

def bot():
 #while True:
    
    #query = takeCommand().lower()
    query="play song"
    speak("you said "+query)
    if 'play' in query:
        song = query.replace('play', '')
        speak('playing' + song)
        pywhatkit.playonyt(song)

    elif 'the time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"sir, the time is {strTime}")

    elif "my name" in query:
        if UName == " ":
         speak("you did'nt tell me about your name")
         speak("can you please tellme your name")
         name=takeCommand().lower()

         if "my name is" or "i am" in name :
            UName =name("my name is"+ UName or "I am" +UName)
            speak(f"your name is {UName}, it's a nice name") 
        else:
         speak(f"I know, your name is {UName}")
        

    elif "change my name to" in query:
        query = query.replace("change my name to", "")
        uname = query
        speak("your name is changed to {UName}")

    elif "what's your name" in query or "What is your name" in query:
        speak("My friends call me")
        speak(uname)
        print("My friends call me", uname)

    elif 'thank you' in query or 'thanks' in query or 'exit' in query:
        speak("Thanks for giving me your time")
        exit()
    elif "how are you" in query:
        speak("I'm fine, how are you ")
        
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
        subprocess.call("taskkill /IM chrome.exe") 

        bot()
        exit()
    else:
        speak("Sorry, I CAN'T DO THAT!! ")



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
    if prediction[:, 1] >0.20:
        print(f"Wake Word Detected for ({i})")
        print("Confidence:", prediction[:, 1])
        i += 1
        #wishMe()
        bot()
        
        
    
    else:
        print("Wake Word NOT Detected")
        print("Confidence:", prediction[:, 0])
