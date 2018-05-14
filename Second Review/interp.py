import difflib
import pickle
import datetime

name = 'SynonimDict.dict'

with open(name, 'rb') as f:
    variants_days = pickle.load(f)
    variants_commands = pickle.load(f)
print(variants_days)

def day_parse(a):
    maxim = 0
    for j in variants_days.keys():
            for i in variants_days[j]:
                temp = difflib.SequenceMatcher(None, a, i).ratio()
                if temp > maxim:
                    maxim = temp
                    if isinstance(j, str):
                        answer = (7 + datetime.datetime.now().weekday() + int(j)) % 7
                    else:
                        answer = j
    return (answer, maxim)


def command_parse(a):
    maxim = 0
    for j in variants_commands.keys():
        for i in variants_commands[j]:
            temp = difflib.SequenceMatcher(None, a, i).ratio()
            if temp > maxim:
                maxim = temp
                answer = j
    return (answer, maxim)


def message_parse(string):
    string = string.lower().split()
    days = []
    commands = []
    for i in string:
        try:
            commands.append(command_parse(i))
        except:
            pass
        try:
            days.append(day_parse(i))
        except:
            pass
    days.sort(key=lambda x: x[1], reverse=True)
    commands.sort(key=lambda x: x[1], reverse=True)
    print(days)
    print(commands)
    print([days[0][0], commands[0][0]])
    try:
        if days[0][1] < 0.6:
            return [None, commands[0][0]]
    except:
        return [None, commands[0][0]]
    return [days[0][0], commands[0][0]]
