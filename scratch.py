# from templating import Templater
#
# temp = Templater()
#
# resp = temp.parse_input("My name is Scott ")
#
# print(resp)
#
# resp = temp.parse_input("My name is Scott")
#
# print(resp)
#
# resp = temp.parse_input("My name is Scot")
#
# print(resp)
import re


data = "Heroku/seomthing else To Tom Tomo Heroku-baby Heroku_Kemperman Heroku=Kemperman"


# result = re.sub("[ \t]", "", data)
result = [w.rstrip(" /=-_") for w in re.findall("[A-Z][A-Za-z0-9]{3,}[ /=\-_]|[A-Z][A-Za-z0-9]*$", data)]
first_word = re.findall("^\w*", data)
last_word = re.findall("\w*", data)

print(result)
print(first_word)
print(last_word)