import json
from operator import itemgetter
from os.path import isfile, join
from os import listdir


def search_files():
    return [f for f in listdir('history') if isfile(join('history', f))]


def get_users_with_files():
    files = search_files()
    return [(x[:-5].split('_')[1], x) for x in files]


def choose_user():
    list_of_users = get_users_with_files()
    for i, user in enumerate(list_of_users):
        print(i+1, '->', user[0])

    choose = int(input("Choose user: "))
    return open_json(list_of_users[choose-1][1])


def sorting_json(database, field='date'):
    return sorted(database, key=itemgetter(field), reverse=True)


def save_to_json(database, filename):
    with open('history/' + filename, 'w') as outfile:
        json.dump(database, outfile, indent=4)


def open_json(filename):
    with open('history/' + filename, 'r') as f:
        return json.load(f)
