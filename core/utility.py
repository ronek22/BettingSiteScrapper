import json
from operator import itemgetter
from os.path import isfile, join
from os import listdir
import re
from pathlib import Path


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


def cash_format(cash):
    return "{0:.2f}".format(cash)


def printf(header, value, value_type='cash'):
    if 'cash' in value_type:
        print('{:<35} {:>10} zł'.format(header, cash_format(value)))
    elif 'percent' in value_type:
        print('{:<35} {:>10} %'.format(header, cash_format(value)))
    elif 'bool' in value_type:
        print('{:<35} {:>10}'.format(header, 'Possible' if True else 'Not possible'))


def sorting_json(database, field='date'):
    return sorted(database, key=itemgetter(field), reverse=True)


def save_to_json(database, filename):
    path = Path('history', filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as outfile:
        json.dump(database, outfile, indent=4)


def open_json(filename):
    with open('history/' + filename, 'r') as f:
        return json.load(f)


def str_to_float(text):
    return re.sub('[^\d\.]', '', text)
