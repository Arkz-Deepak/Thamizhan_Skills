import speech_recognition as sr

# 1. Initialize the Recognizer (The Brain)
listener = sr.Recognizer()

def get_voice_command():
    try:
        with sr.Microphone() as source:
            print("Listening... (Speak now)")
            
            # Adjust for background noise (Wait 1 sec to measure silence)
            listener.adjust_for_ambient_noise(source, duration=1)
            
            # Listen to the audio
            voice = listener.listen(source)
            
            # Convert audio to text using Google's API
            command = listener.recognize_google(voice)
            command = command.lower()
            
            print(f"You said: {command}")
            return command
            
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        print("Network error. Google API is down.")
        return ""
    except Exception as e:
        print(f"Error: {e}")
        return ""

# 2. Main Control Loop
while True:
    print("\n--- Voice Control Active ---")
    text = get_voice_command()
    
    # 3. Map Words to Actions
    if "forward" in text or "go" in text:
        print("🤖 ROBOT ACTION: Moving Forward ⬆️")
    elif "back" in text or "reverse" in text:
        print("🤖 ROBOT ACTION: Moving Backward ⬇️")
    elif "left" in text:
        print("🤖 ROBOT ACTION: Turning Left ⬅️")
    elif "right" in text:
        print("🤖 ROBOT ACTION: Turning Right ➡️")
    elif "stop" in text:
        print("🛑 ROBOT ACTION: Stopping")
    elif "exit" in text or "quit" in text:
        print("Shutting down system.")
        break