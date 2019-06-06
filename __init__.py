from mycroft import MycroftSkill, intent_file_handler


class AceProlog(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('remember.intent')
    def handle_prolog_ace(self, message):
        text = message.data.get('text')
        self.speak_dialog('answer', data={'result': text})


def create_skill():
    return AceProlog()

