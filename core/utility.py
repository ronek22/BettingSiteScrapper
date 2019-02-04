import http.client
import json
from operator import itemgetter
from os.path import isfile, join
from os import listdir, environ
import re
from pathlib import Path
import redis


def get_user(db, user):
    return open_json(db.get('history:'+user)), open_json(db.get('deposits:'+user))  # tuple(history, deposits)


def cash_format(cash):
    return "{0:.2f}".format(cash)

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
