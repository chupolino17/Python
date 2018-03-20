import sys
import os
import pickle


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



def save_obj(main_dict, N, name, MIN, path):
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
                with open(os.getcwd() + '\\obj\\' + name + '.pkl', 'wb') as f:
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
                os.mkdir(os.getcwd() + '\\obj\\')


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


a = sys.argv
lowercase = False
input_dir = [False]
main_dict = {}
model_name = 'primary_model'
model_path = None
N = 1
MIN_LEN_DICT = 1

for i in range(len(a)):
    if a[i] == '--input-dir':
        i += 1
        input_dir = a[i]
    elif a[i] == '--model':
        i += 1
        model_path = a[i]
    elif a[i] == '--min':
        i += 1
        MIN_LEN_DICT = int(a[i])
    elif a[i] == '--lc':
        lowercase = True
    elif a[i] == '--model-name':
        i += 1
        model_name = a[i]
    elif a[i] == '--last-model':
        i += 1
        try:
            with open(a[i], 'rb') as f:
                main_dict = pickle.load(f)
        except:
            sys.stderr = 'Неверно указан путь модели!'
            sys.exit()
    elif a[i] == '--n':
        i += 1
        N = int(a[i])
        #глубина точности не для потребителя (ВЕТА)
        #значение по умолчанию 1
    elif a[i] == '--help':
        print("Аргументы для генератора модели:")
        print("    --input-dir - путь к директории, в которой лежит коллекция документов.")
        print("    --model - путь к файлу, в который сохраняется модель. ПО УМОЛЧАНИЮ \obj\primary_model.pkl")
        print("    --model-name - имя файла модели, сохранится в \obj\ ")
        print("    --last-model - имя файла прошлой модели для пополнения")
        print("    --lc - привести текст к нижнему регистру.")
        print("    --help - справка")
        sys.exit()

for file in os.listdir(input_dir):
    print('Чтение файла текста', file, '... ', end='')
    sys.stdin = open(input_dir + '\\' + file, 'r')
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

if MIN_LEN_DICT > 1:
    main_dict = clear_dict(main_dict, MIN_LEN_DICT)
save_obj(main_dict, N, model_name, MIN_LEN_DICT, model_path)
