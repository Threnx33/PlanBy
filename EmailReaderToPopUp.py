import email
import imaplib
import re

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
#            print("Found one")
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
  while True:
    typ, data = Account.search(None, 'unseen')
    Platform = None
    Hour = None
    rez = []
    last_email_num = b'-1'
    for num in reversed(data[0].split()):
      typ, data = Account.fetch(num, '(RFC822)')
      last_email_num = max(num, last_email_num)
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
      rez.append([Platform, Hour])
    if len(rez):
      return rez
    raise Exception("Nu am putut gasi un meeting!\n")


def Delogare(Account):
  Account.close()
  Account.logout()

if __name__ == "__main__":
  while True:
    cont = Logare()
    try:
      meetings = SearchPlatformAndHour(cont)
      print(meetings)
      for meet in meetings:
        print(meet[0] + " -> " + meet[1] + "\n")
      #meetings -> contine toate meetingurile din mailurile necitite
    except Exception as ex:
      continue
    Delogare(cont)
