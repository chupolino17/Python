import pyodbc
import requests
import json
import interp
import random
days = ['[dbo].[monday]', '[dbo].[tuesday]', '[dbo].[wednesday]', '[dbo].[thursday]', '[dbo].[friday]', '[dbo].[saturday]', '[dbo].[sunday]']
days_rus = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=pyBot;UID=python;PWD=python')
cursor = cnxn.cursor()
print("Connected")
git_html = requests.get('https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt').text.split('\n')[4:]

def get_git_proxy():
    a = random.randint(4, len(git_html))
    print(git_html[a].split()[0])
    return git_html[a].split()[0]


def get_proxy():
    html = requests.get('http://pubproxy.com/api/proxy?not_country=RU&https=true')
    html = json.loads(html.text)
    print(html)
    print(html['data'][0]['ipPort'])
    return html['data'][0]['ipPort']

def get_proxy_second():
    html = requests.get('https://api.getproxylist.com/proxy?notCountry[]=RU&allowsHtts=1')
    html = json.loads(html.text)
    print(html)
    return html['ip']+':'+str(html['port'])

def add_user(userid):
    try:
        cursor.execute("INSERT INTO [pyBot].[dbo].[Users] VALUES(" + str(userid) + ")")
        cnxn.commit()
    except:
        pass


def del_user(userid):
    cursor.execute("DELETE FROM [pyBot].[dbo].[Users] WHERE [pyBot].[dbo].[Users].UserID = " + str(userid))
    for i in range(7):
        delete_timetable(i, userid)
    cnxn.commit()


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
    print("INSERT INTO [pyBot]." + days[day] + " VALUES(" + a + ")")
    cursor.execute("INSERT INTO [pyBot]." + days[day] + " VALUES(" + a + ")")
    cnxn.commit()


def is_user_started(userid):
    if len(cursor.execute("SELECT * FROM [pyBot].[dbo].[Users] WHERE [pyBot].[dbo].[Users].UserID = " + str(userid)).fetchall()) == 0:
        return False
    else:
        return True

def is_userid_exists(day, userid):
    if len(cursor.execute("SELECT * FROM [pyBot]." + days[day] + " WHERE [pyBot]." + days[day] + ".UserID = " + str(userid)).fetchall()) == 0:
        return False
    else:
        return True


def get_timetable(day, userid):
    if is_userid_exists(day, userid):
        return cursor.execute("SELECT * FROM [pyBot]." + days[day] + " WHERE [pyBot]." + days[day] + ".UserID = " + str(userid)).fetchone()
    else:
        raise NameError

def delete_timetable(day, userid):
    cursor.execute("DELETE FROM [pyBot]." + days[day] + " WHERE [pyBot]." + days[day] + ".UserID = " + str(userid))
    cnxn.commit()
