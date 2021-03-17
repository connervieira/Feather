import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import os
import pickle
from pathlib import Path
from os.path import expanduser



if (str(Path.home()) == "/root"): # Terminate if the program is being run as root
    print("Feather can't be run as root. Please re-run Feather as a standard user.")
    sys.exit()
root = str(Path.home()) + "/.config/Feather"



class Feather(toga.App):

    def initialize_database(self):
        if os.path.isdir(str(Path.home()) + "/.config") == False:
            print("~/.config doesn't exist. This is the folder that Feather uses to store it's configuration information.")
            print("Create a folder called '.config' in your home folder and re-run Feather if you still want to attempt to use Feather")

        # Initialize Feather's configuration root directory
        if os.path.isdir(root + ""):
            print("Feather root directory already exists at " + root)
        else:
            os.mkdir(root + "")
            print("Created Feather root directory at " + root)


        if os.path.isfile(root + "/config.txt"):
            print("The configuration database already exists at " + root + "/config.txt")
            config_database = open(root + "/config.txt", "rb")
            self.configuration_array = pickle.loads(config_database.read())
            config_database.close()
        
        else:
            config_database = open(root + "/config.txt", "wb")
            print("Created Feather configuration database at " + root + "/config.txt")
            self.configuration_array = ["localhost:5050", "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"] # Create a placeholder database to be filled in later.
            config_database.write(pickle.dumps(self.configuration_array, protocol=0))
            print("Wrote to the configuration database at " + root + "/config.txt with a placeholder database") 
            config_database.close()

    mood = "" # Placeholder variable to be filled in when the user presses a button to select their mood.


    def startup(self):

        # Initialize Feather and its configuration database
        self.initialize_database()


        self.configuration_open = False # At launch, the configuration menu is closed, so this variable is set to false at launch to reflect that.

        self.main_box = toga.Box(style=Pack(direction=COLUMN)) # This is the box containing the main mood selection buttons. They are displayed top to bottom.
        submission_box = toga.Box(style=Pack(direction=ROW)) # This is the box that contains the Submit and Configuration buttons. They are displayed side by side.


        # Create the prompt element
        prompt_label = toga.Label(
            'What emotion is most prominent to you right now?',
            style=Pack(padding=(0, 0),text_align='center')
        )

        # Create all of the button elements
        happy_button = toga.Button(
            'Happy',
            on_press=self.mood_happy, style=Pack(padding=5)
        )
        sad_button = toga.Button(
            'Sad',
            on_press=self.mood_sad, style=Pack(padding=5)
        )
        stressed_button = toga.Button(
            'Stressed',
            on_press=self.mood_stressed, style=Pack(padding=5)
        )
        angry_button = toga.Button(
            'Angry',
            on_press=self.mood_angry, style=Pack(padding=5)
        )
        excited_button = toga.Button(
            'Excited',
            on_press=self.mood_excited, style=Pack(padding=5)
        )
        relaxed_button = toga.Button(
            'Relaxed',
            on_press=self.mood_relaxed, style=Pack(padding=5)
        )
        tired_button = toga.Button(
            'Tired',
            on_press=self.mood_tired, style=Pack(padding=5)
        )
        neutral_button = toga.Button(
            'Neutral',
            on_press=self.mood_neutral, style=Pack(padding=5)
        )


        submit = toga.Button(
            'Submit',
            on_press=self.submit, style=Pack(padding=5,padding_top=50,flex=1,padding_left=40)
        )
        configure = toga.Button(
            'Configure',
            on_press=self.configure, style=Pack(padding=5,padding_top=50,flex=1,padding_right=40)
        )

        # Display all of the elements on the interface
        self.main_box.add(prompt_label)

        self.main_box.add(happy_button)
        self.main_box.add(sad_button)
        self.main_box.add(stressed_button)
        self.main_box.add(angry_button)
        self.main_box.add(excited_button)
        self.main_box.add(relaxed_button)
        self.main_box.add(tired_button)
        self.main_box.add(neutral_button)

        submission_box.add(submit)
        submission_box.add(configure)

        self.main_box.add(submission_box)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box
        self.main_window.show()



    # Define the functions for all of the buttons.
    def mood_happy(self, widget):
        mood = "happy"

    def mood_sad(self, widget):
        mood = "sad"

    def mood_stressed(self, widget):
        mood = "stressed"

    def mood_angry(self, widget):
        mood = "angry"

    def mood_excited(self, widget):
        mood = "excited"

    def mood_relaxed(self, widget):
        mood = "relaxed"

    def mood_tired(self, widget):
        mood = "tired"

    def mood_neutral(self, widget):
        mood = "neutral"




    def submit(self, widget):
        pass

    def configure(self, widget):
        if (self.configuration_open == False):
            self.configuration_open = True # Indicate that the configuration section is now open.

            self.configuration_box = toga.Box(style=Pack(direction=COLUMN,padding_top=30))

            self.healthbox_server_box = toga.Box(style=Pack(direction=ROW,padding=5))
            self.healthbox_apikey_box = toga.Box(style=Pack(direction=ROW,padding=5))

            self.healthbox_server_label = toga.Label('HealthBox Server and Port:')
            self.healthbox_apikey_label = toga.Label('HealthBox API Key:')

            self.healthbox_server_input = toga.TextInput(style=Pack(flex=1,padding=10),placeholder="host:port",initial=self.configuration_array[0])
            self.healthbox_apikey_input = toga.TextInput(style=Pack(flex=1,padding=10),placeholder="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",initial=self.configuration_array[1])

            self.apply_configuration_button = toga.Button('Apply', on_press=self.apply_configuration, style=Pack(padding=10))

            self.healthbox_server_box.add(self.healthbox_server_label)
            self.healthbox_server_box.add(self.healthbox_server_input)

            self.healthbox_apikey_box.add(self.healthbox_apikey_label)
            self.healthbox_apikey_box.add(self.healthbox_apikey_input)

            self.configuration_box.add(self.healthbox_server_box)
            self.configuration_box.add(self.healthbox_apikey_box)

            self.main_box.add(self.configuration_box)
            self.main_box.add(self.apply_configuration_button)


        elif (self.configuration_open == True):
            self.configuration_open = False
            self.main_box.remove(self.configuration_box)
            self.main_box.remove(self.apply_configuration_button)

    def apply_configuration(self, widget):
        # Make changes to the configuration array
        self.configuration_array[0] = self.healthbox_server_input.value
        self.configuration_array[1] = self.healthbox_apikey_input.value
    
        # Save changes to the configuration array to disk
        config_database = open(root + "/config.txt", "wb") # Open configuration database
        config_database.write(pickle.dumps(self.configuration_array, protocol=0)) # Write configuration changes to disk
        config_database.close() # Close the configuration database


def main():
    return Feather()
