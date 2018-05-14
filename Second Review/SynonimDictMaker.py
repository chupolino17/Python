import pickle
import lib
days = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], '+1': [], '+2': [], '-1': [], '-2': [], '0': []}
commands = {'create': [], 'update': [], 'delete': [], 'get': [], 'cancel': []}
name = 'SynonimDict.dict'
try:
    with open(name, 'rb') as f:
        temp_days = pickle.load(f)
        temp_commands = pickle.load(f)
    for i in temp_commands.keys():
        commands[i] = temp_commands[i]
    for i in temp_days.keys():
        days[i] = temp_days[i]
    print(commands)
except:
    pass

for i in commands.keys():
    try:
        print('Синонимы для ', i, ':')
    except:
        print(i)
    a = input().strip().lower()
    while a != '/':
        commands[i].append(a)
        a = input().strip().lower()

with open('SynonimDict.dict', 'wb') as f:
    pickle.dump(days, f, pickle.HIGHEST_PROTOCOL)
    pickle.dump(commands, f, pickle.HIGHEST_PROTOCOL)