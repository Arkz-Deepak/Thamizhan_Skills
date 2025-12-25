import speech_recognition as sr

listener = sr.Recognizer()

def get_voice_command():
    try:
        with sr.Microphone() as source:
            print("Listening... (Speak now)")
            
            listener.adjust_for_ambient_noise(source, duration=1)
            
            voice = listener.listen(source)
            
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

while True:
    print("\n--- Voice Control Active ---")
    text = get_voice_command()
    
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