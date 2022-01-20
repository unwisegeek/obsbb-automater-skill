from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_file_handler, intent_handler

class ObsbbAutomater(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('automations.available.intent')
    def handle_list_automations(self, message):
        self.speak_dialog('automations.available')

    # @intent_file_handler('automater.obsbb.intent')
    @intent_handler(IntentBuilder('ExecBBAutomation')
                    .require('Automation'))
    def handle_automater_obsbb(self, message):
        self.speak_dialog('automater.obsbb')


def create_skill():
    return ObsbbAutomater()

