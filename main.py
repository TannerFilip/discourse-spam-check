#!/usr/bin/python3
import argparse
import pprint
import sys
import webbrowser

import requests
from colorama import init, Fore

import config

init()  # initialize colorama

pp = pprint.PrettyPrinter(indent=4)

dd = config.DISCOURSE_DOMAIN
REQ_HEADERS = {'Api-Key': config.API_KEY,
               'Api-Username': config.API_USERNAME,
               'Content-Type': 'application/json'}


def get_suspect_users():
    """
    Get a list of suspect users.
    Discourse defines this as not having much "read time" or many "read posts".

    """
    pg_num = 1
    suspect_users_full = {}
    suspect_len = 0
    i = 0

    execute = True
    while execute:
        # Grab the admin page of suspect users, and convert it to json.
        # Requests automatically turns the json it receives into a list.
        # Discourse only shows a few on each page so this just loops until it gets to a blank page.
        suspect_users = requests.get(
            dd + '/admin/users/list/suspect.json?page=' + str(pg_num),
            headers=REQ_HEADERS).json()

        for usrs in suspect_users:  # there's probably a cleaner way to do this.
            suspect_users_full[i] = suspect_users[i]
            i += 1

        pg_num += 1
        suspect_len = len(suspect_users)
        if suspect_len <= 0:
            execute = False
    return suspect_users_full


def get_silenced_users():
    """Same as previous, but for silenced users."""

    pg_num = 1
    silenced_users_full = {}
    i = 0

    execute = True
    while execute:
        silenced_users = requests.get(
            dd + '/admin/users/list/silenced.json?page=' + str(pg_num),
            headers=REQ_HEADERS).json()

        for usrs in silenced_users:
            silenced_users_full[i] = silenced_users[i]
            i += 1

        pg_num += 1
        silenced_len = len(silenced_users)
        if silenced_len <= 0:
            execute = False
    return silenced_users_full


def delete_user(scan_username, scan_userid):
    """
    1.Asks for confirmation and if accepted
    2.if accepted delete a user, blocking their email, IP, and any URLs they posted
    """

    print('Really delete '+scan_username+'? There is no undo!')
    print('Type \'y\' and press return to delete.')
    confirmation = input()
    if confirmation.lower() == 'y':
        try:
            requests.delete(dd + '/admin/users/' + scan_userid + '.json', headers=REQ_HEADERS, params={
                'context': 'Determined to be a spammer by ' + config.API_USERNAME + ' (using discourse-spam-check)',
                'block_email': 'true',
                'block_urls': 'true',
                'block_ip': 'true',
                'delete_posts': 'true'
                })
        except KeyError:
            print('Unable to delete ' + scan_username)
        else:
            print('Deleted ' + scan_username)
    else:
        print('Not deleting...')


def get_user_action(scan_username, scan_userid):
    """ Prompt for an input on what to do with each user. """

    while True:
        user_action = input(': ')
        if user_action.lower() == 's' or user_action == '':
            break
        elif user_action.lower() == 'd':
            delete_user(scan_username, scan_userid)
            break
        elif user_action.lower() == 'o':
            webbrowser.open_new_tab(dd+'/u/'+scan_username)
            continue
        elif user_action.lower() == 'q':
            print('Quitting...' + Fore.RESET)
            sys.exit(0)
        else:
            print(Fore.RED + 'Invalid command.' + Fore.RESET)

    return user_action


def scan_suspect_users():
    """
    1. Scans suspect user list
    2. Prints in terminal the username and bio
    3. Gives options on what to do next
    """

    suspect_users = get_suspect_users()  # have to make the list first
    for usrs in suspect_users:
        scan_username = suspect_users[usrs]['username']
        scan_userid = str(suspect_users[usrs]['id'])
        scan_user = requests.get(dd + '/u/' + scan_username + '.json', headers=REQ_HEADERS).json()
        print(Fore.RED + 'Found user: ' + scan_username + Fore.RESET)
        print('User ID: ' + scan_userid)
        print('User bio: ')
        pp.pprint(str(scan_user['user']['bio_raw']))

        print(Fore.YELLOW + 'What would you like to do?')
        print('[S]kip, [d]elete and block IP, [o]pen in browser, [q]uit' + Fore.RESET)

        get_user_action(scan_username, scan_userid)


def scan_silenced_users():
    """Same as above, but for silenced users."""

    silenced_users = get_silenced_users()
    for usrs in silenced_users:
        scan_username = silenced_users[usrs]['username']
        scan_userid = str(silenced_users[usrs]['id'])
        scan_user = requests.get(dd + '/u/' + scan_username + '.json', headers=REQ_HEADERS).json()
        print(Fore.RED + 'Found user: ' + scan_username + Fore.RESET)
        print('User ID: ' + scan_userid)
        print('User bio: ')
        try:
            print(str(scan_user['user']['bio_raw']))
        except KeyError:
            print('User has no bio.')

        print(Fore.YELLOW + 'What would you like to do?')
        print('[S]kip, [d]elete and block IP, [o]pen in browser, [q]uit' + Fore.RESET)

        get_user_action(scan_username, scan_userid)


parser = argparse.ArgumentParser(prog="Discourse Spam Checker")
parser.add_argument('--type', '-t', help='Specify which user list to scan. Defaults to \'all\'',
                    choices=['all', 'suspect', 'silenced'], default='all')

args = parser.parse_args()

if args.type == 'all':
    scan_suspect_users()
    scan_silenced_users()
elif args.type == 'silenced':
    scan_silenced_users()
elif args.type == 'suspect':
    scan_suspect_users()
