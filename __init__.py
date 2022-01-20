from mycroft import MycroftSkill, intent_file_handler


class ObsbbAutomater(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('automater.obsbb.intent')
    def handle_automater_obsbb(self, message):
        self.speak_dialog('automater.obsbb')


def create_skill():
    return ObsbbAutomater()

