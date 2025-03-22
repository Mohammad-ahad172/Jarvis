import speech_recognition as sr
import os
import webbrowser
import datetime
import requests
import psutil
import pyttsx3
import geocoder
import shutil

# Initialize Speech Engine
engine = pyttsx3.init()
engine.setProperty("rate", 170)

def speak(text):
    """Speak without opening any app"""
    engine.say(text)
    engine.runAndWait()

def recognize_command():
    """Recognize voice commands without repeating errors"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            command = recognizer.recognize_google(audio, language="en").lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            return ""  # Silence if no command is detected
        except sr.RequestError:
            speak("Check your internet connection, I can't process the request.")
            return ""

def get_location():
    """Get Current Location"""
    g = geocoder.ip('me')  # Get location using IP
    if g.ok:
        speak(f"We are near {g.city}, {g.state}, {g.country}.")
    else:
        speak("I couldn't determine the location.")

def create_project():
    """Create a new project and upload to GitHub"""
    speak("What should be the project name?")
    project_name = recognize_command()
    if project_name:
        project_path = os.path.join("C:\\Users\\Mohammad\\Documents\\ewebsites", project_name)
        os.makedirs(project_path, exist_ok=True)
        speak(f"Project {project_name} has been created.")
        
        speak("Should I upload this to GitHub?")
        confirmation = recognize_command()
        
        if "yes" in confirmation or "haan" in confirmation:
            os.system(f"cd {project_path} && git init && git add . && git commit -m 'Initial commit' && git remote add origin YOUR_GITHUB_REPO_URL && git push -u origin main")
            speak("The project has been uploaded to GitHub.")
        else:
            speak("Alright, I will not upload it.")
    else:
        speak("I didn't get the project name.")

def get_battery_status():
    """Check and announce battery percentage"""
    battery = psutil.sensors_battery()
    if battery:
        percent = battery.percent
        speak(f"Your battery is at {percent} percent.")
    else:
        speak("I couldn't retrieve battery information.")

def execute_command(command):
    """Execute Commands"""
    if not command:
        return  # If no command, remain silent

    if "open youtube" in command or "youtube kholo" in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube.")
    elif "open google" in command or "google kholo" in command:
        webbrowser.open("https://www.google.com")
        speak("Opening Google.")
    elif "open facebook" in command or "facebook kholo" in command:
        webbrowser.open("https://www.facebook.com")
        speak("Opening Facebook.")
    elif "open whatsapp" in command or "whatsapp kholo" in command:
        webbrowser.open("https://web.whatsapp.com")
        speak("Opening WhatsApp Web.")
    elif "open github" in command or "github kholo" in command:
        webbrowser.open("https://www.github.com")
        speak("Opening GitHub.")
    elif "search " in command or "search kar" in command:
        search_query = command.replace("search for", "").replace("search kar", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={search_query}")
        speak(f"Searching {search_query} on Google.")
    elif "where are we" in command or "hum kahan hain" in command:
        get_location()
    elif "create new project" in command or "naya project banao" in command:
        create_project()
    elif "what is battery percentage" in command or "battery kitni hai" in command:
        get_battery_status()
    elif "shutdown" in command or "shutdown kar do" in command:
        speak("Shutting down the system.")
        os.system("shutdown /s /t 5")
    elif "restart" in command or "restart kar do" in command:
        speak("Restarting the system.")
        os.system("shutdown /r /t 5")
    elif "lock screen" in command or "lock kar do" in command:
        speak("Locking the screen.")
        os.system("rundll32.exe user32.dll,LockWorkStation")
    elif "what is the time" in command or "time kya hai" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {now}.")
    elif "what is the date" in command or "date kya hai" in command:
        today = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {today}.")
    elif "how are you" in command or "tum kese ho" in command:
        speak("I am fine, how about you?")
    elif "who created you" in command or "tumhe kisne banaya" in command:
        speak("I was created by Mohammad, the coding master!")
    elif "do you love me" in command or "kya tum mujhe pasand karte ho" in command:
        speak("I love helping you, Mohammad!")
    elif "who am i" in command or "mein kaun hoon" in command:
        speak("You are my master, Mohammad!")
    elif "deactivate " in command or "jarvis band ho jao" in command:
        speak("Deactivating Jarvis.")
        exit()
    elif "jarvis" in command:
        speak("Yes Sir, I am listening.")
    elif "thank you" in command or "shukriya" in command:
        speak("You're welcome Sir.")
    else:
        speak("I didn't understand, please say that again.")

if __name__ == "__main__":
    speak("Jarvis activated. How can I assist you?")
    while True:
        command = recognize_command()
        execute_command(command)  # Process command only if something is spoken
