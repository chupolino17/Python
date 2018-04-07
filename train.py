import sys
import os
import pickle
import argparse


def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '#' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()


def clear_dict(main, min):
    result = {}
    for i in main.keys():
        if len(main[i].keys()) >= min:
            result.update({i: main[i]})
    return result


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


def save_obj(main_dict, N, MIN, path):
    print("Создание файла модели...", end='')
    while True:
        try:
            with open(path, 'wb') as f:
                pickle.dump(N, f, pickle.HIGHEST_PROTOCOL)
                pickle.dump(MIN, f, pickle.HIGHEST_PROTOCOL)
                keys = list(main_dict.keys())
                pickle.dump((len(keys)), f, pickle.HIGHEST_PROTOCOL)
                for j in range(len(keys) // 100):
                    newdict = {}
                    for i in range(100):
                        newdict.update({keys[i + j * 100]: main_dict[keys[i + j * 100]]})
                    pickle.dump(newdict, f, pickle.HIGHEST_PROTOCOL)
                newdict = {}
                for i in range(len(keys) % 100):
                    newdict.update(
                        {keys[i + (j + 1) * 100]: main_dict[keys[i + (j + 1) * 100]]})
                pickle.dump(newdict, f, pickle.HIGHEST_PROTOCOL)
                print('ГОТОВО!')
                break
        except:
            try:
                os.mkdir(os.getcwd() + '\\obj\\')
            except:
                print('Не найден путь', name, '. Проверьте правильность имени папки и повторите попытку. ')
                sys.exit()


def wordgood(input_word):
    word = input_word.lower()
    result = ""
    for i in word:
        if (ord(i) >= ord('a') and ord(i) <= ord('z')) \
                or (ord(i) >= ord('а') and ord(i) <= ord('я')) \
                or (ord(i) >= ord('A') and ord(i) <= ord('Z')) \
                or (ord(i) >= ord('А') and ord(i) <= ord('Я'))\
                or (i == '-' and len(word) > 1 and word[0] != '-'):
            result += i
    if len(result) == 0:
        result = '#@'
    return result


def parse():
    parser = argparse.ArgumentParser(description='Гененратор моделей из текстов 1.2')
    parser.add_argument('--input_dir', action='store', default=None, required=True, help='Аргумент вывобра папки с текстами для анализа.')
    parser.add_argument('--model', action='store', default=os.getcwd() + '\\obj\\primary_model.pkl', help='Путь создания фалйа модели.')
    parser.add_argument('--lc', action='store_true', default=False, help='Приводить к нижнему регистру (опционально).')
    parser.add_argument('--min', action='store', default=1, help='Разнообразность словаря (БЕТА) (опционально)')
    parser.add_argument('--last_model', action='store', default=None, help='Файл словаря для дополнения. (опционально)')
    parser.add_argument('--n', action='store', default=1, help='Глубина точности словаря (БЕТА) (опционально)')
    args = parser.parse_args()
    return args


args = parse()
if args.last_model != None:
    try:
        main_dict = load_obj(args.last_model)
    except:
        sys.stderr = 'Неверно указан путь старой модели!'
        sys.exit()

lowercase = args.lc
main_dict = {}
N = args.n

if args.input_dir == None:
    print('Вставьте сюда текст, после окончания ввода на отдельной строке вставьте ключ --end')
    while True:
        try:
            line = input().strip().split()
        except:
            break
        if '--end' in line:
            break
        for word in range(len(line) - N):
            flag = False
            for i in range(word, word + N + 1):
                if wordgood(line[i]) == '#@':
                    flag = True
                    break
            if flag:
               continue
            key = ' '.join([wordgood(line[i]) for i in range(word, word + N)])
            next_key = ' '.join([wordgood(line[i]) for i in range(word + 1, word + N + 1)])
            if (key in main_dict):
                if next_key in main_dict[key]:
                    main_dict[key][next_key] += 1
                else:
                    main_dict[key][next_key] = 1
            else:
                main_dict[key] = {next_key: 1}
            first_word = next_key
else:
    for file in os.listdir(args.input_dir):
        print('Чтение файла текста', file, '... ', end='')
        sys.stdin = open(args.input_dir + '\\' + file, 'r')
        while True:
            try:
                line = input().strip().split()
            except:
                break
            for word in range(len(line) - N):
                flag = False
                for i in range(word, word + N + 1):
                    if wordgood(line[i]) == '#@':
                        flag = True
                        break
                if flag:
                    continue
                key = ' '.join([wordgood(line[i]) for i in range(word, word + N)])
                next_key = ' '.join([wordgood(line[i]) for i in range(word + 1, word + N + 1)])
                if (key in main_dict):
                    if next_key in main_dict[key]:
                        main_dict[key][next_key] += 1
                    else:
                        main_dict[key][next_key] = 1
                else:
                    main_dict[key] = {next_key: 1}
                first_word = next_key
        print('ГОТОВО!')

if args.min > 1:
    main_dict = clear_dict(main_dict, args.min)
save_obj(main_dict, args.n, args.min, args.model)
