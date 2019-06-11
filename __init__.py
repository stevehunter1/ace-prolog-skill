from mycroft import MycroftSkill, intent_file_handler

import requests


def get_test(s):
    r = requests.get("https://www.felix-frank.com/")
    return r.text

class AceProlog(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('remember.intent')
    def handle_remember(self, message):
        remember = message.data.get('text')
        self.speak_dialog('answer', data={'result': remember})

    @intent_file_handler('prove.intent')
    def handle_prove(self, message):
        prove = message.data.get('text')
        p = get_test(prove)
        self.speak_dialog('answer', data={'result': p})

    @intent_file_handler('question.intent')
    def handle_question(self, message):
        question = message.data.get('text')
        self.speak_dialog('answer', data={'result': question})


def create_skill():
    return AceProlog()

