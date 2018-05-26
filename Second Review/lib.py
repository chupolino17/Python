import pyodbc
import requests
import json
import interp
import random
import config
import datetime
days = ['[dbo].[monday]', '[dbo].[tuesday]', '[dbo].[wednesday]', '[dbo].[thursday]', '[dbo].[friday]', '[dbo].[saturday]', '[dbo].[sunday]']
days_rus = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=pyBot;UID=python;PWD=python')
cursor = cnxn.cursor()
print("Connected to DataBase localhost/pyBot")
git_html = requests.get(config.proxy_list).text.split('\n')[4:]


def get_git_proxy():
    a = random.randint(4, len(git_html)-3)
    print(git_html[a].split()[0])
    return git_html[a].split()[0]


def get_proxy():
    html = requests.get('http://pubproxy.com/api/proxy?not_country=RU&https=true')
    html = json.loads(html.text)
    print(html['data'][0]['ipPort'])
    return html['data'][0]['ipPort']


def get_proxy_second():
    html = requests.get('https://api.getproxylist.com/proxy?notCountry[]=RU&allowsHtts=1')
    html = json.loads(html.text)
    print(html['ip']+':'+str(html['port']))
    return html['ip']+':'+str(html['port'])


def add_user(userid):
    try:
        cursor.execute('INSERT INTO [pyBot].[dbo].[Users] VALUES({})'.format(userid))
        cnxn.commit()
    except:
        pass


def del_user(userid):
    cursor.execute('DELETE FROM [pyBot].[dbo].[Users] WHERE [pyBot].[dbo].[Users].UserID = {}'.format(userid))
    for i in range(7):
        delete_timetable(i, userid)
    cnxn.commit()


def set_update(day, update_text, userid):
    if day <= datetime.datetime.today().weekday():
        days_to_sum = 7 + day - datetime.datetime.today().weekday()
    else:
        days_to_sum = day - datetime.datetime.today().weekday()
    date = datetime.date.today() + datetime.timedelta(days=days_to_sum)
    print("INSERT INTO [pyBot].[dbo].[changes] VALUES({}, '{}', '{}')".format(userid, update_text, date.isoformat()))
    cursor.execute("INSERT INTO [pyBot].[dbo].[changes] VALUES({}, '{}', '{}')".format(userid, update_text, date.isoformat()))
    cnxn.commit()
    return date


def insertion_timetable(day, table, userid):
    if is_userid_exists(day, userid):
        delete_timetable(day, userid)
    a = str(userid)+', '
    for i in range(len(table)-1):
        if table[i] is None:
            a += 'NULL, '
        else:
            a += "'" + table[i] + "', "
    if table[len(table)-1] is None:
        a += 'NULL'
    else:
        a += "'" + table[len(table)-1] + "'"
    print("INSERT INTO [pyBot].{} VALUES({})".format(days[day], a))
    cursor.execute("INSERT INTO [pyBot].{} VALUES({})".format(days[day], a))
    cnxn.commit()


def updates_for_date(day, userid):
    if day <= datetime.datetime.today().weekday():
        days_to_sum = 7 + day - datetime.datetime.today().weekday()
    else:
        days_to_sum = day - datetime.datetime.today().weekday()
    date = datetime.date.today() + datetime.timedelta(days=days_to_sum)
    a = cursor.execute("SELECT * FROM [pyBot].[dbo].[changes] WHERE [pyBot].[dbo].[changes].UserID = {0} AND [pyBot].[dbo].[changes].date = '{1}'".format(userid, date.isoformat())).fetchall()
    temp = ''
    if len(a) != 0:
        temp = date.strftime('%d.%m.%y') + ': У ВАС ИЗМЕНЕНИЯ В ЭТОТ ДЕНЬ!\n'
        print(a)
        for i in a:
            temp += i[1][0].upper()+i[1][1:] + '\n'
        temp += '\n'

        print(temp)
    return temp


def is_user_started(userid):
    if len(cursor.execute("SELECT * FROM [pyBot].[dbo].[Users] WHERE [pyBot].[dbo].[Users].UserID = {}".format(userid)).fetchall()) == 0:
        return False
    else:
        return True


def is_userid_exists(day, userid):
    if len(cursor.execute("SELECT * FROM [pyBot].{0} WHERE [pyBot].{0}.UserID = {1}".format(days[day], userid)).fetchall()) == 0:
        return False
    else:
        return True


def get_timetable(day, userid):
    print("SELECT * FROM [pyBot].{0} WHERE [pyBot].{0}.UserID = {1}".format(days[day], userid))
    if is_userid_exists(days[day], userid):
        return cursor.execute("SELECT * FROM [pyBot].{0} WHERE [pyBot].{0}.UserID = {1}".format(days[day], userid)).fetchone()
    else:
        raise NameError


def delete_timetable(day, userid):
    print('Удаление из', days[day], userid)
    cursor.execute("DELETE FROM [pyBot].{0} WHERE [pyBot].{0}.UserID = {1}".format(days[day], userid))
    print('Удаленo из', days[day], userid)
    cnxn.commit()

