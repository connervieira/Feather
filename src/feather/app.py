import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import os
import pickle
from pathlib import Path
from os.path import expanduser
import time
import datetime 
from datetime import timezone
import traceback
import urllib.parse

# Attempt to import the 'requests' module
try:
    import requests
except ModuleNotFoundError as error:
    if traceback.format_exception_only (ModuleNotFoundError, error) != ["ModuleNotFoundError: No module named 'requests'\n"]: # Make sure the error we're catching is the right one
        raise # If not, raise the error
    raise utils.MissingLibraryError ("making web server requests", "requests")

 
# Define the function required to make network requests to HealthBox
class APICallError (Exception): pass # This will be used when returning errors.

def make_request (*, server, api_key, submission = None, print_url = False):
    endpoint = "metrics/b7/submit".split ('/') # Define the method and metric that this request will use on HealthBox.
    url = f"http://{server}/api/source/{'/'.join (endpoint)}?api_key={urllib.parse.quote (api_key)}" # Form the URL that will be used to communicate with HealthBox
    if submission is not None:
        url += f"&submission={urllib.parse.quote (submission)}" # Attach the JSON submission data to the URL formed above.
    if print_url: print (f"Making a request to {url}")
    response = requests.get (url) # Send the network request.
    response_data = response.json () # Save the response of the network request to the response_data variable.
    if not response_data ["success"]: # If something goes wrong, return an error.
        raise APICallError (response_data ["error"])
    del response_data ["success"]
    del response_data ["error"]
    return response_data



if (str(Path.home()) == "/root"): # Terminate if the program is being run as root
    print("Feather can't be run as root. Please re-run Feather as a standard user.")
    sys.exit()
root = str(Path.home()) + "/.config/Feather"



class Feather(toga.App):
    error_label = toga.Label("") # Placeholder for later

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
        prompt_label = toga.Label('What emotion is most prominent to you right now?', style=Pack(padding=(0, 0),text_align='center'))

        # Create all of the button elements
        happy_button = toga.Button('Happy', on_press=self.mood_happy, style=Pack(padding=5))
        sad_button = toga.Button('Sad', on_press=self.mood_sad, style=Pack(padding=5))
        stressed_button = toga.Button('Stressed', on_press=self.mood_stressed, style=Pack(padding=5))
        angry_button = toga.Button('Angry', on_press=self.mood_angry, style=Pack(padding=5))
        excited_button = toga.Button('Excited', on_press=self.mood_excited, style=Pack(padding=5))
        relaxed_button = toga.Button('Relaxed', on_press=self.mood_relaxed, style=Pack(padding=5))
        tired_button = toga.Button('Tired', on_press=self.mood_tired, style=Pack(padding=5))
        neutral_button = toga.Button('Neutral', on_press=self.mood_neutral, style=Pack(padding=5))

        submit = toga.Button('Submit', on_press=self.submit, style=Pack(padding=5,padding_top=50,flex=1,padding_left=40))
        configure = toga.Button('Configure', on_press=self.configure, style=Pack(padding=5,padding_top=50,flex=1,padding_right=40))


        # Add all of the UI elements to the interface
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


        # Show all of the UI elements
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box
        self.main_window.show()



    # Define the functions for all of the buttons.
    def mood_happy(self, widget):
        self.mood = "happy"

    def mood_sad(self, widget):
        self.mood = "sad"

    def mood_stressed(self, widget):
        self.mood = "stressed"

    def mood_angry(self, widget):
        self.mood = "angry"

    def mood_excited(self, widget):
        self.mood = "excited"

    def mood_relaxed(self, widget):
        self.mood = "relaxed"

    def mood_tired(self, widget):
        self.mood = "tired"

    def mood_neutral(self, widget):
        self.mood = "neutral"


    def submit(self, widget):
        self.main_box.remove(self.error_label)
        if (self.configuration_array[1] == "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" or len(self.configuration_array[1]) != 32):
            self.error_label = toga.Label('Error: You need to configure the HealthBox API key!', style=Pack(padding=(0, 0),text_align='center'))
            self.main_box.add(self.error_label)
        elif (self.mood == ""):
            self.error_label = toga.Label('Error: You need to select a mood first!', style=Pack(padding=(0, 0),text_align='center'))
            self.main_box.add(self.error_label)
        else:
            print("GOTHERE")
            timestamp = int(time.time())
            # Generate the submission data as plain text JSON data.
            submission = '{"timestamp": ' + str(timestamp) + ', "data": {"mood": "' + str(self.mood) + '", "time": ' + str(timestamp) + '}}'
            print(submission)
            response = make_request (server = self.configuration_array[0], submission = submission, api_key = self.configuration_array[1], print_url = True)


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
