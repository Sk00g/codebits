from templating import Templater

temp = Templater()

resp = temp.parse_input("My name is Scott ")

print(resp)

resp = temp.parse_input("My name is Scott")

print(resp)

resp = temp.parse_input("My name is Scot")

print(resp)