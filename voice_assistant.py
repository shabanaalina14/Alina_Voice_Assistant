import speech_recognition as sr
import pyttsx3 as pt
import pywhatkit as pk
import sys


class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pt.init()
        self.wake_word = "alina"
        self.configure_voice()

    def configure_voice(self):
        """Configure female voice with cross-platform support"""
        voices = self.engine.getProperty('voices')

        # Platform-specific voice selection
        if sys.platform == 'win32':  # Windows
            # Try to get Zira (Microsoft's female voice)
            for voice in voices:
                if 'zira' in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    break
        elif sys.platform == 'darwin':  # macOS
            # Try to get default female voice
            for voice in voices:
                if 'samantha' in voice.name.lower():  # Common macOS female voice
                    self.engine.setProperty('voice', voice.id)
                    break
        else:  # Linux and other systems
            # Try to find any female voice
            for voice in voices:
                if 'female' in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    break

        # Fallback to first available voice if no female found
        if not self.engine.getProperty('voice'):
            self.engine.setProperty('voice', voices[0].id)

        # Optimize voice parameters
        self.engine.setProperty('rate', 160)  # Slightly faster than normal
        self.engine.setProperty('volume', 0.9)  # 90% volume
        self.engine.setProperty('pitch', 110)  # Slightly higher pitch

    def speak(self, text):
        """Convert text to speech with natural pauses"""
        print(f"Assistant: {text}")
        # Add natural pauses for punctuation
        for phrase in text.split(','):
            self.engine.say(phrase.strip())
            self.engine.runAndWait()

    def listen(self):
        """Listen for voice commands with improved noise handling"""
        try:
            with sr.Microphone() as source:
                print("Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.8)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=8)

                command = self.recognizer.recognize_google(audio).lower()
                if self.wake_word in command:
                    return command.replace(self.wake_word, '').strip()
                return None

        except sr.WaitTimeoutError:
            self.speak("I didn't hear anything. Are you there?")
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't catch that")
        except sr.RequestError as e:
            self.speak("My speech service is having trouble")
            print(f"API Error: {e}")
        except Exception as e:
            self.speak("Something went wrong")
            print(f"Error: {e}")
        return None

    def process_command(self, command):
        """Enhanced command processing"""
        if not command:
            return

        print(f"Processing: {command}")

        if 'play' in command:
            song = command.replace('play', '').strip()
            self.speak(f"Playing {song} on YouTube")
            pk.playonyt(song)
        elif 'close' in command or 'quit' in command:
            self.speak("It was lovely assisting you. Have a beautiful day ahead!")
            sys.exit()
        elif 'hello' in command:
            self.speak("Hello there! How can I help you?")
        else:
            self.speak("I'm still learning that command, but I can play music if you say 'play [song name]'")

    def run(self):
        """Main assistant loop with friendly interactions"""
        self.speak(
            f"Hello! I'm {self.wake_word.capitalize()}, your voice assistant. Say '{self.wake_word}' followed by your command.")
        while True:
            command = self.listen()
            self.process_command(command)


if __name__ == "__main__":
    assistant = VoiceAssistant()
    try:
        assistant.run()
    except KeyboardInterrupt:
        assistant.speak("Shutting down")
        sys.exit(0)