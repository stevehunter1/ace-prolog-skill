from mycroft import MycroftSkill, intent_file_handler


class AceProlog(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('prolog.ace.intent')
    def handle_prolog_ace(self, message):
        self.speak_dialog('prolog.ace')


def create_skill():
    return AceProlog()

