from mycroft import MycroftSkill, intent_file_handler
from mycroft.filesystem import FileSystemAccess
from mycroft.util.log import LOG

import requests
# from lxml import etree
import xml.etree.ElementTree as EL


url = "http://attempto.ifi.uzh.ch/ws/race/racews.perl"
headers = {"content-type": "text/xml"}

ns = {"env": "http://schemas.xmlsoap.org/soap/envelope/",
      "race": "http://attempto.ifi.uzh.ch/race"}


def check_consistency(knowledge):
    body = """<?xml version="1.0" encoding="UTF-8"?>
  <env:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
      <env:Body>
          <race:Request xmlns:race="http://attempto.ifi.uzh.ch/race">
              <race:Axioms>"""+knowledge+"""</race:Axioms>
              <race:Mode>check_consistency</race:Mode>
          </race:Request>
      </env:Body>
  </env:Envelope>"""
    response = requests.post(url, data=body, headers=headers)
    root = EL.fromstring(response.content)
    # etree.dump(root)
    good = True
    for el in root.iterfind(".//race:Proof", ns):
        if el is not None:
            good = False
    # print(good)
    return good


def prove_with_answer(knowledge, theorem):
    body = """<?xml version="1.0" encoding="UTF-8"?>
  <env:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
      <env:Body>
          <race:Request xmlns:race="http://attempto.ifi.uzh.ch/race">
              <race:Axioms>"""+knowledge+"""</race:Axioms>
              <race:Theorems>"""+theorem+"""</race:Theorems>
              <race:Mode>prove</race:Mode>
          </race:Request>
      </env:Body>
  </env:Envelope>"""
    response = requests.post(url, data=body, headers=headers)
    root = EL.fromstring(response.content)
    # etree.dump(root)
    good = False
    for el in root.iterfind(".//race:Proof", ns):
        if el is not None:
            good = True
    # print(good)
    return good


def ask_with_answer(knowledge, question):
    body = """<?xml version="1.0" encoding="UTF-8"?>
  <env:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
      <env:Body>
          <race:Request xmlns:race="http://attempto.ifi.uzh.ch/race">
              <race:Axioms>"""+knowledge+"""</race:Axioms>
              <race:Theorems>"""+question+"""</race:Theorems>
              <race:Mode>answer_query</race:Mode>
          </race:Request>
      </env:Body>
  </env:Envelope>"""
    response = requests.post(url, data=body, headers=headers)
    root = EL.fromstring(response.content)
    # etree.dump(root)
    good = False
    for el in root.iterfind(".//race:Proof", ns):
        if el is not None:
            good = True
    # print(good)
    return good


def get_knowledge(self, filename):
    file_system = FileSystemAccess(str(self.skill_id))
    file = file_system.open(filename, "r")
    data = []
    for line in file:
        data.append(line.rstrip('\n'))
    knowledge = ".".join(data)
    return knowledge


def save_knowledge(self, filename, knowledge, mode="w"):
    data = knowledge.split(".")
    data = "\n".join(data)
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

def check_dot(input):
  string = input.rstrip()
  if string[-1] != '.':
    string += '.'
  return string

# def load_data_file(self, filename, mode="r"):
#     file_system = FileSystemAccess(str(self.skill_id))
#     file = file_system.open(filename, mode)
#     data = file.read()
#     file.close()
#     return data


# def save_data_file(self, filename, data, mode="w"):
#     try:
#         file_system = FileSystemAccess(str(self.skill_id))
#         file = file_system.open(filename, mode)
#         file.write(data)
#         file.close()
#         return True
#     except Exception as e:
#         LOG.warning("could not save skill file " + filename)
#         LOG.error(e)
#         return False


class AceProlog(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('remember.intent')
    def handle_remember(self, message):
        remember = message.data.get('text')
        remember = check_dot(remember)
        check = check_consistency(remember)
        if check:
          knowledge = get_knowledge(self, "test.txt")
          knowledge += remember
          check = check_consistency(knowledge)
          if check:
            self.speak_dialog('answer', data={'result': remember})
          else:
            self.speak_dialog('fail')
        else:
          self.speak_dialog('fail')
        # save_data_file(self, "test.txt", remember, "a")
        # self.speak_dialog('answer', data={'result': remember})

    @intent_file_handler('prove.intent')
    def handle_prove(self, message):
        prove = message.data.get('text')
        # p = get_test(prove)
        self.speak_dialog('answer', data={'result': prove})

    @intent_file_handler('question.intent')
    def handle_question(self, message):
        question = message.data.get('text')
        # data = load_data_file(self, "test.txt")
        self.speak_dialog('answer', data={'result': question})


def create_skill():
    return AceProlog()
