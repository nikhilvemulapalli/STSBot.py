import sys
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit

recognizer = sr.Recognizer()
engine = pyttsx3.init()

genai.configure(api_key="AIzaSyBpwxmiM-wxqgYJY1AkYcubw_kMZJqhqrw")
model = genai.GenerativeModel("gemini-1.5-flash")

def speak(text):
    engine.say(text)
    engine.runAndWait()

def recognize_speech(output_text):
    with sr.Microphone() as source:
        print("Listening...")
        speak("Listening...")
        try:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=3)
            text = recognizer.recognize_google(audio)

            if text in ['exit', 'leave']:
                speak("Exiting")
                print("Exiting")
                sys.exit(0)

            print(f"You said: {text}")
            response = f"You said: {text}"
            speak(response)

            responsem = model.generate_content(text)
            print(responsem.text)
            output_text.setText(responsem.text)
            speak(responsem.text)

            

        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            speak("Sorry, I could not understand the audio.")
            output_text.setText("Sorry, I could not understand the audio.")
        except sr.RequestError:
            print("Could not request results; please check your internet connection.")
            speak("Could not request results; please check your internet connection.")
            output_text.setText("Could not request results; please check your internet connection.")

class SpeechBotApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Speech-to-Speech Bot')
        self.setGeometry(100, 100, 400, 400)

        layout = QVBoxLayout()

        self.label = QLabel("Click 'Start' to talk to the bot", self)
        layout.addWidget(self.label)

        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)
        layout.addWidget(self.output_text)

        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.start_recognition)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton('Stop', self)
        self.stop_button.clicked.connect(self.stop_recognition)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)

    def start_recognition(self):
        recognize_speech(self.output_text)

    def stop_recognition(self):
        speak("Exiting...")
        print("Exiting...")
        sys.exit(0)

app = QApplication(sys.argv)
window = SpeechBotApp()
window.show()
sys.exit(app.exec_())
