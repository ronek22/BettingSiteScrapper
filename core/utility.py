import http.client
import json
from operator import itemgetter
from os.path import isfile, join
from os import listdir, environ
import re
from pathlib import Path
import redis


def search_files():
    return [f for f in listdir('history') if isfile(join('history', f))]


def get_users_with_files():
    # TODO: Maybe is possible to make this with only one loop
    files = search_files()
    users_diary = {x[:-5].split('_')[1]: {} for x in files}
    for x in files:
        user = (x[:-5].split('_'))[1]
        if 'history' in x:
            users_diary[user]['history'] = x
        else:
            users_diary[user]['deposit'] = x

    return users_diary


def choose_user():
    users = get_users_with_files()
    for key in users.keys():
        print(key)

    user = input("Choose user: ")
    return open_json(users[user]['history']), open_json(users[user]['deposit'])  # tuple(history, deposits)


def get_user(db, user):
    return open_json(db.get('history:'+user)), open_json(db.get('deposits:'+user))  # tuple(history, deposits)


def cash_format(cash):
    return "{0:.2f}".format(cash)


def printf(header, value, value_type='cash'):
    if 'cash' in value_type:
        print('{:<35} {:>10} zł'.format(header, cash_format(value)))
    elif 'percent' in value_type:
        print('{:<35} {:>10} %'.format(header, cash_format(value)))
    elif 'bool' in value_type:
        print('{:<35} {:>10}'.format(header, 'Possible' if True else 'Not possible'))


def stringf(header, value, value_type='cash'):
    if 'cash' in value_type:
        return '{:<35} {:>10} zl\n'.format(header, cash_format(value))
    elif 'percent' in value_type:
        return '{:<35} {:>10} %\n'.format(header, cash_format(value))
    elif 'bool' in value_type:
        return '{:<35} {:>10}\n'.format(header, 'Possible' if True else 'Not possible')


def sorting_json(database, field='date'):
    return sorted(database, key=itemgetter(field), reverse=True)


def save_to_json(database, filename, connection):
    connection.set(filename, json.dumps(database, indent=4))


def open_json(key):
    return json.loads(key)


def str_to_float(text):
    return re.sub('[^\d\.]', '', text)


def send_to_discord(login, message):

    webhookurl = "https://discordapp.com/api/webhooks/541753226643636234/z28EEXowrz76aGV1iQxTgDBwk0HZo_l5OA73sJBkjGxWi8svSFQER0Vyrt50Y9AVo-7E"

    formdata = "------:::BOUNDARY:::\r\nContent-Disposition: form-data; name=\"content\"\r\n\r\n" + login + '\n' + message + "\r\n------:::BOUNDARY:::--"

    connection = http.client.HTTPSConnection("discordapp.com")
    connection.request("POST", webhookurl, formdata, {
        'content-type': "multipart/form-data; boundary=----:::BOUNDARY:::",
        'cache-control': "no-cache",
    })

    # get the response
    response = connection.getresponse()
    result = response.read()

    # return back to the calling function with the result
    return result.decode("utf-8")
