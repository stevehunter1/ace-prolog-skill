from mycroft import MycroftSkill, intent_file_handler, FileSystemAccess
from mycroft.util.log import LOG

import requests


def get_test(s):
    r = requests.get("https://www.felix-frank.com/")
    return r.text

def load_data_file(self, filename, mode="r"):
    file_system = FileSystemAccess(str(self.skill_id))
    file = file_system.open(filename, mode)
    data = file.read()
    file.close()
    return data

def save_data_file(self, filename, data, mode="w"):
    try:
        file_system = FileSystemAccess(str(self.skill_id))
        file = file_system.open(filename, mode)
        file.write(data)
        file.close()
        return True
    except Exception as e:
        LOG.warning("could not save skill file " + filename)
        LOG.error(e)
        return False

class AceProlog(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('remember.intent')
    def handle_remember(self, message):
        remember = message.data.get('text')
        save_data_file(self, "test.txt", "hallo")
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

