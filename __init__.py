from enum import auto
from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_file_handler, intent_handler
import requests
import json

class ObsbbAutomater(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.API_HOST = self.settings.get('api_host', False)
        self.API_PORT = self.settings.get('api_port', False)

    @intent_file_handler('automations.available.intent')
    def handle_list_automations(self, message):
        if self.API_HOST and self.API_PORT:
            entries = []
            cached = []
            available_triggers = ""
            r = requests.get(f'http://{self.API_HOST}:{self.API_PORT}/api/automation/triggers')

            if r.status_code == 200:    
                for item in r.text.strip('"').split(','):
                    entries += [ item.split(":")[0] ]
                    cached += [ dict(
                        name=item.split(":")[0], 
                        endpoint=item.split(":")[1]
                        )]
                with open('./automation-cache', 'w') as f:
                    f.write(json.dumps(cached))
                for item in entries:
                    available_triggers += f"and {item}" if item == entries[-1] else f"{item}, "
                self.speak_dialog(f'The available automations are: {available_triggers}')
            else:
                self.speak_dialog("The A P I Call has failed. Please recheck that the A P I is running and the settings are correct.")                
        else:
            self.speak_dialog('Please sign in to yore mycroft dot hey eye account and set the variables for A P I Host and A P I Port in the Skills Setting.')

    @intent_handler(IntentBuilder('ExecBBAutomation')
                    .require('automations')
                    .require('activate')
    )
    def handle_automater_obsbb(self, message):
        endpoint = None
        pattern = ""
        translations = {
            "Start Stream": "stream",
            "Countdown for 1 Minute": "countdown for one minute",
            "Countdown for 2 Minutes": "countdown for two minutes",
            "Countdown for 5 Minutes": "countdown for five minutes. Get me a snack too.",
            "Countdown for 10 Minutes": "countdown for ten minutes. Someone has to hit the can.",
            "Go On Camera": "go on camera automation",
            "Outro": "outro",
        }
        target = message.data.get('automations')
        for key in translations.keys():
            if key.lower() == target:
                pattern = translations[key]
                break
        self.speak_dialog(f"I'm starting the damned {pattern}")
        r = requests.get(f'http://{self.API_HOST}:{self.API_PORT}/api/automation/triggers')
        if r.status_code == 200:    
            for item in r.text.strip('"').split(','):
                if item.split(':')[0].lower() == target:
                    endpoint = item.split(':')[1]
                    break
            if endpoint:
                r = requests.get(f'http://{self.API_HOST}:{self.API_PORT}/api/automation?trigger={endpoint}')
            else:
                self.speak_dialog('There was an error triggering the automation.')
        else:
            self.speak_dialog('There was an error retrieving automations.')

    @intent_file_handler('cheer.intent')
    def handle_cheer(self, message):
        self.speak_dialog('Hooray, you.')
        r = requests.get(f'http://{self.API_HOST}:{self.API_PORT}/api/sound?name=ES_Crowd Teens Cheer 7 -0')



def create_skill():
    return ObsbbAutomater()

