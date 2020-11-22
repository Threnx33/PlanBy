import email
import imaplib
import re
from flask import Flask, render_template, request, jsonify
import requests
from flask_cors import CORS
import json
from datetime import date

from Errors import PlatformError, HourError


def get_body(msg):
  if msg.is_multipart():
    return get_body(msg.get_payload(0))
  else:
    return msg.get_payload(None, True)

def ConvertMessageToString(raw):
  string_message = str(get_body(raw))
  string_message = string_message.replace("\\r", "")
  string_message = string_message.replace("\\n", "")
  return string_message

def FindPlatform(message):
  platforms = {"Discord": ["discord"], "Zoom": ["zoom"], "Microsoft Teams": ["ms teams", "msteams", "teams", "microfost teams"], "Google meet":["google meet", "meet"], "Messenger": ["messenger", "facebook"]}

  temp = message.lower()
  for elem in platforms:
    for platform in platforms[elem]:
      if platform in temp:  
        return elem
  raise PlatformError("Nu am gasit nici o platforma!\n")

def FindDay(message):
  days = []
  months = []
  separators = ["/", "."]
  for i in range (1, 31):
    days.append(str(i))
  for i in range(1, 13):
    months.append(str(i))
  for i in reversed(days):
    day = i
    occurrences = [m.start() for m in re.finditer(day, message)]
    for j in occurrences:
      try:
        month = int(message[j + 3 : j + 5])
      except ValueError:
        try:
          month = int(message[j + 3])
        except ValueError:
          continue
        except IndexError:
          break
      except IndexError:
        try:
          month = int(message[j + 3])
        except ValueError:
          continue
        except IndexError:
          break
        print(day)
      if (str(month) in months) and (message[j + 2] in separators):
        print(day, str(month))
        return day + " " + str(month)
  raise HourError("Nu am gasit nici o data calendaristica in email!\n")

def FindHour(message):
  hours = []
  separator = [" ", ":", ";", "-"]
  rez = ""
  for i in range(0, 25):
    i = str(i)
    if len(i) < 2:
      i = "0" + i
    hours.append(i)

  for i in range(0, 10):
    hours.append(str(i))

  for i in hours:
    hour = i
    occurrences = [m.start() for m in re.finditer(hour, message)]
    for j in occurrences:
      try:
        minutes = int(message[j + 3 : j + 5])
      except ValueError:
        continue
      else:
        if minutes % 10 == 0 and minutes >= 0 and minutes <= 50:
          if len(hour) == 1:
            j -= 1
          if message[j + 3 : j + 5].isdigit() and (message[j + 2] in separator):
            return hour + " " + message[j + 3 : j + 5]
  raise HourError("Nu am gasit nici o ora in email!\n")



def Logare():
  user = "rachetaalbastra8@gmail.com"
  password = "functiifarateste"
  imap_url = "imap.gmail.com"

  M = imaplib.IMAP4_SSL(imap_url)
  M.login(user, password)
  M.select('INBOX')
  M.select()
  return M

def SearchPlatformAndHour(Account):
  typ, data = Account.search(None, 'unseen')
  Platform = None
  Hour = None
  for num in reversed(data[0].split()):
    typ, data = Account.fetch(num, '(RFC822)')
    raw = email.message_from_bytes(data[0][1])
    TheMessage = ConvertMessageToString(raw)
    try:
      Platform = FindPlatform(TheMessage)
    except PlatformError:
      continue
    try:
      Hour = FindHour(TheMessage)
    except HourError:
      continue
    try:
      DataCalendaristica = FindDay(TheMessage)
    except HourError as re:
      print(re)
    return [Platform, Hour, DataCalendaristica]
    raise Exception("Nu am putut gasi un meeting!\n")


def Delogare(Account):
  Account.close()
  Account.logout()


app = Flask(__name__)
CORS(app) # cross origin

@app.route("/cerere.html", methods=['GET', 'POST', 'PUT'])
def run():

  data = request.json
  x = json.loads(data)
  k = 0
  while True:
    cont = Logare()
    k += 1
    print("Cautarea nr: " + str(k))
    try:
      Platforma, Hour, DataCalendaristica = SearchPlatformAndHour(cont)
      dictionar = {}
      dictionar["platforma"] = Platforma
      dictionar["ora"] = Hour
      lista = DataCalendaristica.split()
      dictionar["zi"] = lista[0]
      dictionar["luna"] = lista[1]
      Delogare(cont)
      return dictionar
      #meetings -> contine toate meetingurile din mailurile necitite
    except Exception as ex:
      continue
    Delogare(cont)

app.run(debug = True)