import sys

import pyttsx3
import speech_recognition


class BaseCommands():
    exit_program = "EXIT PROGRAM"
    mute_program = "MUTE PROGRAM"
    unmute_program = "UNMUTE PROGRAM"
    show_commands = "SHOW COMMANDS"


class PYVC():
    def __init__(self, *args, **kwargs):
        self._listener = speech_recognition
        self._speaker = pyttsx3.init()
        for v in self._speaker.getProperty('voices'):
            for lang in v.languages:
                print(1, v, lang, lang.decode('utf8'))
        self.debug_state = False
        self._sleep_state = False
        self._commands = {
            BaseCommands.exit_program: {
                "function": self.exit,
                "description": "Exit the program."
            },
            BaseCommands.mute_program: {
                "function": self.sleep,
                "description": "The program will sleep until it hears the word 'UNMUTE PROGRAM'."
            },
            BaseCommands.show_commands: {
                "function": self.show_commands,
                "description": "Provide a list of available commands."
            },
        }
        return super().__init__(*args, **kwargs)

    def command(self, phrase: str, description: str = ""):
        def decorator(f):
            self.add_command(phrase.upper(), f, description)
        return decorator

    def add_command(self, phrase: str, function, description: str):
        if not isinstance(phrase, str):
            raise ValueError(f"Command: {phrase}, is not a str.")
        if phrase in self._commands:
            raise KeyError(f"Command: {phrase}, already exists.")
        if not callable(function):
            raise ValueError(f"Function: {function}, is not callable.")
        if description == None:
            raise ValueError(f"Description cannot be none.")
        if description == "":
            raise ValueError(f"Description cannot be an empty string.")
        self._commands.setdefault(
            phrase.upper(),
            {
                "function": function,
                "description": str(description)
            })

    def start(self, debug_state: bool = False):
        self.debug_state = debug_state
        intro = [
            "* The program has started listening.",
            "* Say {} for a list of commands.\n".format(
                BaseCommands.show_commands),
        ]
        print("\n".join(intro))
        while self._listener and self._speaker and self._commands:
            while True:
                command = self.listen().upper()
                if self.debug_state:
                    print("You said:", command)
                if command in self._commands:
                    if self.debug_state:
                        print("Found command:", command)
                    try:
                        self._commands[command]["function"]()
                    except Exception as e:
                        self.log_error(f"{command}: {e}")
                    break

    def listen(self) -> str:
        recognizer = self._listener.Recognizer()
        microphone = self._listener.Microphone()
        with microphone as source:
            audio = recognizer.listen(source)
            try:
                result = recognizer.recognize_google(audio)
                return str(result).upper()
            except Exception as e:
                self.log_error(f"LISTEN: {e}")
                return ""

    def speak(self, value: str):
        self._speaker.say(value)
        self._speaker.runAndWait()

    def set_speaker_properties(self, properties: dict):
        for k in properties:
            self._speaker.setProperty(k, properties[k])

    def exit(self):
        print("Goodbye.")
        self.speak("Goodbye.")
        sys.exit()

    def sleep(self):
        self.speak("I will sleep until you say the command 'UNMUTE PROGRAM'.")
        self._sleep_state = True
        while self._sleep_state:
            command = self.listen()
            if command == BaseCommands.unmute_program:
                self.speak("I am now listening.")
                self._sleep_state = False

    def show_commands(self):
        print("COMMANDS:")
        for command in self._commands:
            description = self._commands[command]["description"]
            print(f"> {command}: {description}")
        print()

    def log_error(self, e):
        if self.debug_state:
            with open("error_log.txt", "a+") as f:
                f.write(f"{str(e)}\n")


def main():
    bot = PYVC()

    @bot.command(phrase="Hello World", description="Say 'Hello World!'")
    def hello_world():
        bot.speak("Hello World!")

    @bot.command("Repeat after me", "Say what will be repeated back to you.")
    def hello_world():
        print("Say what I will repeat.")
        bot.speak(bot.listen())

    @bot.command("Read Gateway of the Mind", "Tell a story about an event in 1983.")
    def creepy_pasta():
        paragraphs = [
            "In 1983, a team of deeply pious scientists conducted a radical experiment in an undisclosed facility. The scientists had theorized that a human without access to any senses or ways to perceive stimuli would be able to perceive the presence of God. They believed that the five senses clouded our awareness of eternity, and without them, a human could actually establish contact with God by thought. An elderly man who claimed to have “nothing left to live for” was the only test subject to volunteer. To purge him of all his senses, the scientists performed a complex operation in which every sensory nerve connection to the brain was surgically severed. Although the test subject retained full muscular function, he could not see, hear, taste, smell, or feel. With no possible way to communicate with or even sense the outside world, he was alone with his thoughts.",
            "Scientists monitored him as he spoke aloud about his state of mind in jumbled, slurred sentences that he couldn’t even hear. After four days, the man claimed to be hearing hushed, unintelligible voices in his head. Assuming it was an onset of psychosis, the scientists paid little attention to the man’s concerns.",
            "Two days later, the man cried that he could hear his dead wife speaking with him, and even more, he could communicate back. The scientists were intrigued, but were not convinced until the subject started naming dead relatives of the scientists. He repeated personal information to the scientists that only their dead spouses and parents would have known. At this point, a sizable portion of scientists left the study.",
            "After a week of conversing with the deceased through his thoughts, the subject became distressed, saying the voices were overwhelming. In every waking moment, his consciousness was bombarded by hundreds of voices that refused to leave him alone. He frequently threw himself against the wall, trying to elicit a pain response. He begged the scientists for sedatives, so he could escape the voices by sleeping. This tactic worked for three days, until he started having severe night terrors. The subject repeatedly said that he could see and hear the deceased in his dreams.",
            "Only a day later, the subject began to scream and claw at his non-functional eyes, hoping to sense something in the physical world. The hysterical subject now said the voices of the dead were deafening and hostile, speaking of hell and the end of the world. At one point, he yelled “No heaven, no forgiveness” for five hours straight. He continually begged to be killed, but the scientists were convinced that he was close to establishing contact with God.",
            "After another day, the subject could no longer form coherent sentences. Seemingly mad, he started to bite off chunks of flesh from his arm. The scientists rushed into the test chamber and restrained him to a table so he could not kill himself. After a few hours of being tied down, the subject halted his struggling and screaming. He stared blankly at the ceiling as teardrops silently streaked across his face. For two weeks, the subject had to be manually rehydrated due to the constant crying. Eventually, he turned his head and, despite his blindness, made focused eye contact with a scientist for the first time in the study. He whispered “I have spoken with God, and he has abandoned us” and his vital signs stopped. There was no apparent cause of death."
        ]
        for p in paragraphs:
            bot.speak(p)

    bot.start(debug_state=True)


if __name__ == "__main__":
    main()
