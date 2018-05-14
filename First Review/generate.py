import sys
import pickle
import random
import argparse
sys.setrecursionlimit(50000)


def progress(progress, total):
    print('\r[{0}] {1}%'.format('#'*(round(progress/total*50)) + '-'*(50-round(progress/total*50)), ((progress/total + 0.001)//0.001)/10), end = '')


def load_obj(name):
    global N
    try:
        with open(name, 'rb') as f:
            N = pickle.load(f)
            if N > 1:
                print("Внимание, вы работаете со словарем с точностью больше 1!")
                print("Вы делаете это на свой cтрах и риск, стабильная работа не гарантируется.\n")
            MIN = pickle.load(f)
            if MIN > 1:
                print("Внимание, вы работаете со словарем где минимальное число возможных продолжений больше 1!")
                print("Вы делаете это на свой cтрах и риск, стабильная работа не гарантируется.\n")
            L = pickle.load(f)
            main_dict = {}
            print("Считывания файла модели:")
            for i in range(L // 100):
                progress(i, L // 100)
                main_dict.update(pickle.load(f))
            print()
            if L % 100 > 0:
                main_dict.update(pickle.load(f))
            return main_dict
    except:
        print('Неверный путь файла словаря')
        sys.exit()


def rand_line(length, inword, time):
    global LENGTH
    progress(LENGTH - length - 1, LENGTH)
    try:
        if length < 0:
            return ''
        tempdict = []
        indict = main_dict[inword]
        for key, value in indict.items():
            for i in range(value):
                tempdict.append(key)
        word = random.choice(tempdict)
        a = rand_line(length - 1, word, 0)
        #print(a, length)
        if a == "False":
            if time <= 10:
                return rand_line(length, inword, time+1)
            else:
                return "False"
        else:
            # + "(" + str(dict[word])+ ") "
            #print(main_dict[inword])
            return word.split()[0] + " " + a
    except:
        if time > 10:
            return "False"
        return rand_line(length, inword, time+1)


def parse():
    parser = argparse.ArgumentParser(description='Гененратор моделей из текстов 1.2')
    parser.add_argument('--model', action='store', required=True, help='Путь к файлу модели')
    parser.add_argument('--length', action='store', default=50, type=int, help='Длина сроки (по умолчанию - 50).')
    parser.add_argument('--output', action='store', default=None, help='Файл вывода строки (опционально.')
    parser.add_argument('--seed', action='store', default=None, help='Певрое слово строки (опционально).')
    args = parser.parse_args()
    return args


args = parse()
result = []
a = sys.argv
main_dict = {}
N = 1
LENGTH = args.length
first = args.seed
main_dict = load_obj(args.model)
final_line = "False"
i = 0
print("Генерация строки:")
mother = []

if first != None:
    flag = False
    for j in main_dict.keys():
        for l in main_dict[j]:
            if first.lower() == l.lower().split()[0]:
                mother.append(l)
    random.shuffle(mother)
    #print(mother)
    if len(mother) < 1:
        print('Не удалось найти слово в тексте, выберите другое начальное слово!')
        sys.exit()
used_keys = []
while final_line == "False" and not len(used_keys) == len(main_dict.keys()):
    i += 1
    if first == None:
        flag = True
        key = ''
        while key in used_keys:
            key = random.choice(list(main_dict.keys()))
        used_keys.append(key)
        final_line = rand_line(LENGTH-1, key, 0)
    else:
        for l in mother:
            final_line = rand_line(LENGTH - 1, l, 0)
            if final_line != "False":
                break
    if i > 100:
        print('Не удалось выполнить генерацию строки, измените начальное слово или длину')
        sys.exit()
if first != None:
    final_line = first + " " + final_line
print('\n\n', final_line)
