import telebot
import config
import lib
import interp
from telebot import apihelper

apihelper.proxy = {'https': 'https://'+lib.get_git_proxy()}
bot = telebot.TeleBot(config.token)
last_actions = {}


@bot.message_handler(commands=['cancel'])
def cancel(message):
    last_actions[message.chat.id] = None
    bot.send_message(message.chat.id, "Забыли...")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    lib.add_user(message.chat.id)
    bot.send_message(message.chat.id, "Добро пожаловать! Для начала работы создайте расписания /create")


@bot.message_handler(commands=['stop'])
def delete_user(message):
    bot.send_message(message.chat.id, "До свидания, до новых встреч!")
    lib.del_user(message.chat.id)


def create(chatid):
    if not lib.is_user_started(chatid):
        bot.send_message(chatid, 'Для начала работы нажмите /start')
        return
    last_actions[chatid] = 'start_create'
    bot.send_message(chatid, 'Выберите день расписание для которго вы хотите заполнить?')

@bot.message_handler(commands=['create'])
def creation(message):
    create(message.chat.id)


@bot.message_handler(commands=['end'])
def end_create(message):
    if last_actions[message.chat.id][0] != 'creating':
        bot.send_message(message.chat.id, 'Неверная команда!')
        return
    for i in range(8 - len(last_actions[message.chat.id][2])):
        last_actions[message.chat.id][2].append(None)
    last_actions[message.chat.id][1] = 8
    bot.send_message(message.chat.id, 'Вы можете добавить дополнительные занятия или законичить /stop_create')


@bot.message_handler(commands=['stop_create'])
def stop_create(message):
    if last_actions[message.chat.id][0] != 'creating':
        bot.send_message(message.chat.id, 'Неверная команда!')
        return
    last_actions[message.chat.id][1] = 9
    last_actions[message.chat.id][2].append(None)
    lib.insertion_timetable(last_actions[message.chat.id][3], last_actions[message.chat.id][2], message.chat.id)
    bot.send_message(message.chat.id, 'Расписание на ' + lib.days_rus[last_actions[message.chat.id][3]] + ' заполнено')
    last_actions[message.chat.id] = None


def getting_of_timetable(chatid, day):
    a = 'Вот ваше расписание на ' + lib.days_rus[day] + ': \n'
    try:
        timetable = lib.get_timetable(day, chatid)
    except NameError:
        bot.send_message(chatid, 'У вас нет расписания на этот день, вы можете создать его по ключу /create')
        return
    print(timetable)
    for i in range(1, len(timetable) - 1):
        if not timetable[i] is None:
            temp = str(i) + '. ' + timetable[i][:1].upper() + timetable[i][1:] + '\n'
            a += temp
    if not timetable[len(timetable) - 1] is None:
        temp = 'Также у вас в этот день:\n' + timetable[len(timetable) - 1]
        a += temp
    bot.send_message(chatid, a)


@bot.message_handler(commands=['get_timetable'])
def get_timetable(message):
    try:
        day = interp.day_parse(message.text.split()[1])
        if day[1] < 0.8:
            bot.send_message(message.chat.id, 'Мы не совсем уверены и решили, что это - ' + lib.days_rus[
                day[0]] + '. Если мы ошиблись, то поробуйте по-другому, например: "/get_timetable ' + lib.days_rus[
                day[0]] + '"')
        day = day[0]
    except Exception:
        bot.send_message(message.chat.id, 'Попросите меня по-другому, например: "/get_timetable пн"')
        return
    getting_of_timetable(message.chat.id, day)


@bot.message_handler()
def usual_message(message):
    try:
        if last_actions[message.chat.id] == 'start_create':
            try:
                day = interp.day_parse(message.text)
                if day[1] < 0.8:
                    bot.send_message(message.chat.id, 'Мы не совсем уверены и решили, что это - ' + lib.days_rus[day[0]] + '. Если что, всегда можно начать заново /create')
                day = day[0]
                print('here')
                last_actions[message.chat.id] = ['creating', 0, [], day]
                bot.send_message(message.chat.id, 'Отправляйте ваши занятия по очереди (каждое в новом сообщении, не больше 8) после последнего отправьте /end')
            except:
                bot.send_message(message.chat.id, 'Сложный какой-то день я такое не парсю, повтори плиз')
        elif last_actions[message.chat.id][0] == 'creating':
            last_actions[message.chat.id][1] += 1
            last_actions[message.chat.id][2].append(message.text)
            if last_actions[message.chat.id][1] == 8:
                bot.send_message(message.chat.id, 'Вы можете добавить дополнительные занятия или законичить /stop_create')
            elif last_actions[message.chat.id][1] == 9:
                lib.insertion_timetable(last_actions[message.chat.id][3], last_actions[message.chat.id][2], message.chat.id)
                bot.send_message(message.chat.id, 'Расписание на ' + lib.days_rus[last_actions[message.chat.id][3]] + ' заполнено')
                last_actions[message.chat.id] = None
    except:
        try:
            day, command = interp.message_parse(message.text)
            print(day, command)
            if command == 'create':
                if day is None:
                    create(message.chat.id)
                else:
                    print('here')
                    last_actions[message.chat.id] = ['creating', 0, [], day]
                    bot.send_message(message.chat.id,
                                     'Отправляйте ваши занятия по очереди (каждое в новом сообщении, не больше 8) после последнего отправьте /end')
            elif command == 'get':
                getting_of_timetable(message.chat.id, day)
            elif command == 'cancel':
                last_actions[message.chat.id] = None
                bot.send_message(message.chat.id, "Забыли...")
        except:
            bot.send_message(message.chat.id, 'Либо что-то пошло не так, либо я слишком глупый, попробуйте еще раз..')


def polling_function():
    try:
        print('Bot running...')
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        apihelper.proxy = {'https': 'https://' + lib.get_git_proxy()}
        print('Proxy changed')
        polling_function()


polling_function()