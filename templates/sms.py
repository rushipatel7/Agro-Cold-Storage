import urllib
import urllib.parse, urllib.request
import time
# Proovl SMS API settings www.proovl.com / Script for Python 2
user = "jyfFJWy"   # change ***** to your Proovl user ID
token = "mpqDB2sXlfvwX3MrsDpPQQb4dqJsAF95"   # change ***** to your Proovl token
from1 = "+919106016105"  # change ***** to your Proovl SMS number
text = "Hello World"   # text
# Add numbers: format "44755555555" / one per line
numbers = [
"+919737330332"
]
messagesSent = 0
host = "https://www.proovl.com/api/send.php?"
for x in numbers:
  messagesSent += 1
  params = {
  "user": user,       
  "token": token,
  "from": from1,
  "text": text,
  "to": x}
  query_string = urllib.parse.urlencode(params)   
  http_req = host + query_string
  f = urllib.request.urlopen(http_req)
  txt = (f.read().decode('utf-8'))
  z = txt.split(";")
  time.sleep(0.5)
  print("Progress: {}/{}") .format(messagesSent, len(numbers)), (x), (z[0])
if z[0] == "Error":
  print("== Error. Text messages not sent ==")
else:
  print("== Message has been sent! ==")