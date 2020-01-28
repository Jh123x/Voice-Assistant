from gtts import gTTS
import speech_recognition as sr
import pygame
import time
import webbrowser
import random
import urllib
import re

class JHAssistant:
    def __init__(self,lang = "en-uk"):
        """Initializer for the voice assistant"""
        self.lang = lang

        #Initialise the mixer
        self.mixer = pygame.mixer
        self.mixer.init()

        #Initialise the voice recognizer
        self.recognizer = sr.Recognizer()

        #Error messages
        self.errmsg = ("Sorry, I didn't catch what you say","Can you repeat that?","What did you say?")

    def talk(self,message : str) -> None:
        """Conver text to speech for the voice command"""

        #Initialise the speech to None
        text_to_speech = None

        #Splitting up each of the 
        for line in message.splitlines():
            if not text_to_speech:
                text_to_speech = gTTS(text = line, lang= self.lang)
            else:
                text_to_speech += gTTS(text = line, lang= self.lang)
        
        #Saving the audio file 
        text_to_speech.save('audio.mp3')

        #Load the file
        self.mixer.music.load("audio.mp3")

        #Play the music file
        self.mixer.music.play(0)

        #Block the main thread while the mixer is playing
        while(self.mixer.music.get_busy()):
            time.sleep(0.1)

        #Unload the file
        self.mixer.music.unload()

    def listen(self) -> str:
        """The command for the virtual assistant to listen to the user"""

        #Listen to the microphone as source
        with sr.Microphone() as source:
            #Setting the Pause threshold
            self.recognizer.pause_threshold = 2

            #Get the command from the user
            while True:

                #Adjust the noise for the ambient sound
                self.recognizer.adjust_for_ambient_noise(source, duration = 1)

                #Listen to the user
                self.talk("Listening")

                #Listen to the audio
                audio = self.recognizer.listen(source)

                try:
                    #Recognizing the voice
                    command = self.recognizer.recognize_google(audio).lower()

                    #If recognition is successful return the command
                    return command
                except sr.UnknownValueError:
                    #Otherwise the loop continues
                    self.talk("Your last command cannot be heard! ")
        
        #If it reaches here it means that there is an error
        return None

    def parse_command(self,command) -> None:
        """Parse the command for the Virtual assistant"""
        print(f"Command: {command}")
        cmd = command.split(" ")
        if("quit" in cmd or "exit" in cmd):
            exit()
        elif("search" == cmd[0]):
            self.open_google(cmd[1:])
        elif("youtube" == cmd[0]):
            self.open_youtube(cmd[1:])

        #Add additional commands here
        else:
            self.talk(random.choice(self.errmsg))

    def open_youtube(self,queries):
        """Open youtube"""
        self.talk("Opening youtube")
        if len(queries):

            #Join the queries together
            domain = " ".join(queries)

            #Get the query string for the youtube vid
            query_string = urllib.parse.urlencode({"search_query" : domain})

            #Get the HTML result of the youtube search
            html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string) 

            #Look through the search results to get the id
            search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())

            #Open the result link in the web browser
            webbrowser.open(f"http://www.youtube.com/watch?v={search_results[0]}")
        else:
            webbrowser.open("http://www.youtube.com")

    def open_google(self,queries):
        """Open google in a new tab TODO: Add with search queries keyed in"""
        self.talk("I have opened google for you, please enter the search data")
        webbrowser.open("www.google.com/")

def main():
    """The main function for the virtual assistant"""
    assistant = JHAssistant()
    while(True):
        command = assistant.listen()
        assistant.parse_command(command)
        time.sleep(1)
        

if __name__ == "__main__":
    main()
