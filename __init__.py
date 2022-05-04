from enum import auto
from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_file_handler, intent_handler
import requests
import json
from time import time_ns
import os

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
            phrase = []
            available_triggers = ""
            r = requests.get(f'http://{self.API_HOST}:{self.API_PORT}/api/automation/triggers')

            if r.status_code == 200:
                cached += [ time_ns() ]
                for item in r.text.strip('"').split(','):
                    entries += [ item.split(":")[2] ]
                    cached += [ dict(
                        name=item.split(":")[0], 
                        endpoint=item.split(":")[1],
                        phrase=item.split(":")[2],
                        )]
                with open('./automation-cache', 'w') as f:
                    f.write(json.dumps(cached))
                f.close()
                if os.path.exists('./skills/obsbb-automater-skill/locale/en-us/automations.voc'):
                    self.log.info("removing automations.voc....")
                    os.remove('./skills/obsbb-automater-skill/locale/en-us/automations.voc')
                with open('./skills/obsbb-automater-skill/locale/en-us/automations.voc', 'w') as f:
                    for item in entries:
                        f.write(f"{item}\n")
                        available_triggers += f"and {item}" if item == entries[-1] else f"{item}, "
                f.close()
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
        current_time = time_ns()
        endpoint = None
        phrase = ""
        target = message.data.get('automations')
        with open('./automation-cache', 'r') as f:
            entries = json.loads(f.read())
            self.log.info(entries)
        for i in range(1, len(entries)):
            self.log.info(f"Comparing {entries[i]['phrase'].lower()} to {target.lower()}")
            if entries[i]["phrase"].lower() == target.lower():
                endpoint = entries[i]["endpoint"]
                phrase = entries[i]["phrase"]
                break
        if endpoint:
            self.speak_dialog(f"I'm starting the {phrase}")
            r = requests.get(f'http://{self.API_HOST}:{self.API_PORT}/api/automation?trigger={endpoint}')
        else:
            self.speak_dialog('There was an error triggering the automation.')

    @intent_file_handler('cheer.intent')
    def handle_cheer(self, message):
        self.speak_dialog('Hooray, you.')
        r = requests.get(f'http://{self.API_HOST}:{self.API_PORT}/api/sound?name=ES_Crowd Teens Cheer 7 -0')

def create_skill():
    return ObsbbAutomater()

