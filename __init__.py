from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_file_handler, intent_handler
import requests

class ObsbbAutomater(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.API_HOST = self.settings.get('api_host', False)
        self.API_PORT = self.settings.get('api_port', False)

    @intent_file_handler('automations.available.intent')
    def handle_list_automations(self, message):
        if self.API_HOST and self.API_PORT:
            entries = []
            available_triggers = ""
            r = requests.get(f'http://{self.API_HOST}:{self.API_PORT}/api/automation/triggers')

            if r.status_code == 200:    
                for item in r.text.strip('"').split(','):
                    entries += [ item.split(":")[0] ]
                for item in entries:
                    available_triggers += f"and {item}" if item == entries[-1] else f"{item}, "
            else:
                self.speak_dialog("The A P I Call has failed. Please recheck that the A P I is running and the settings are correct.")                
            self.speak_dialog(f'The available automations are: {available_triggers}')
        else:
            self.speak_dialog('Please sign in to yore mycroft dot hey eye account and set the variables for A P I Host and A P I Port in the Skills Setting.')

    @intent_handler(IntentBuilder('ExecBBAutomation')
                    .require('Automation'))
    def handle_automater_obsbb(self, message):
        self.speak_dialog('automater.obsbb')


def create_skill():
    return ObsbbAutomater()

