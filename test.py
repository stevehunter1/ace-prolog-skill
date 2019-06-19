import requests
from lxml import etree

url = "http://attempto.ifi.uzh.ch/ws/race/racews.perl"
headers = {"content-type":"text/xml"}

ns = {"env":"http://schemas.xmlsoap.org/soap/envelope/", "race":"http://attempto.ifi.uzh.ch/race"}

print("\n\n")

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
  response = requests.post(url, data = body, headers = headers)
  root = etree.fromstring(response.content)
  # etree.dump(root)
  good = True
  for el in root.iterfind(".//race:Proof", ns):
    if el is not None:
      good = False
  print(good)
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
  response = requests.post(url, data = body, headers = headers)
  root = etree.fromstring(response.content)
  etree.dump(root)
  good = False
  for el in root.iterfind(".//race:Proof", ns):
    if el is not None:
      good = True
  print(good)
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
  response = requests.post(url, data = body, headers = headers)
  root = etree.fromstring(response.content)
  etree.dump(root)
  good = False
  for el in root.iterfind(".//race:Proof", ns):
    if el is not None:
      good = True
  print(good)
  return good

def get_knowledge(filename):
  file = open(filename, "r")
  data = []
  for line in file:
    data.append(line.rstrip('\n'))
  knowledge = ".".join(data)
  return knowledge

check_consistency("John is a man. Mary is a woman. Every man is a human.")
prove_with_answer("John is a man. Mary is a woman. Every man is a human.", "John is a human.")
ask_with_answer("John is a man. Mary is a woman. Every man is a human.", "Is John a human?")



print("\n\n")