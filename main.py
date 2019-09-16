#!/usr/bin/python3
import requests
import config
import json
from colorama import init, Fore, Back, Style
import webbrowser
import sys
import argparse
import pprint


init() # initialize colorama

pp = pprint.PrettyPrinter(indent=4)

dd = config.DISCOURSE_DOMAIN
req_headers = {'Api-Key': config.API_KEY,'Api-Username': config.API_USERNAME,'Content-Type': 'application/json'}

def get_suspect_users():
    pgNum = 1
    suspect_users_full = {}
    suspect_len = 0
    i = 0

    execute = True
    while execute:
        # Grab the admin page of suspect users, and convert it to json.
        # Requests automatically turns the json it receives into a list.
        # Discourse only shows a certain number on each page, so this will just loop until it gets to an empty page.
        suspect_users = requests.get(dd+'/admin/users/list/suspect.json?page='+str(pgNum), headers=req_headers).json()

        for usrs in suspect_users: # there's probably a cleaner way to do this.
            suspect_users_full[i] = suspect_users[i]
            i += 1

        pgNum += 1
        suspect_len = len(suspect_users)
        if suspect_len <= 0:
            execute = False
    return suspect_users_full


def get_silenced_users():
    i = 1
    silenced_users_full = []
    silenced_users = []
    silenced_len = 0

    execute = True
    while execute:
        silenced_users = requests.get(dd+'/admin/users/list/silenced.json?page='+str(i), headers=req_headers).json()

        silenced_users_full = silenced_users_full.append(silenced_users)
        i += 1
        silenced_len = len(silenced_users)
        if silenced_len <= 0:
            execute = False

    return silenced_users_full


def delete_user(scan_username, scan_userid):
    print('Really delete? There is no undo!')
    print('Type \'y\' and press return to delete.')
    confirmation = input()
    if confirmation.lower() == 'y':
        try:
            requests.delete(dd+'/admin/users/'+scan_userid+'.json', headers=req_headers, params={
                'context':'Determined to be a spammer by '+config.API_USERNAME+' (using discourse-spam-check)',
                'block_email':'true',
                'block_urls':'true',
                'block_ip':'true',
                'delete_posts':'true'
                })
        except:
            print('Unable to delete ' + scan_username)
        else:
            print('Deleted ' + scan_username)
    else:
        print('Not deleting...')


def get_user_action(scan_username, scan_userid):

    while True:
        user_action = input(': ')
        if user_action.lower() == 's' or user_action == '':
            break
        elif user_action.lower() == 'd':
            delete_user(scan_username, scan_userid)
            break
            break
        elif user_action.lower() == 'o':
            webbrowser.open_new_tab(dd+'/u/'+scan_username)
            continue
        elif user_action.lower() == 'q':
            print('Quitting...' + Fore.RESET)
            sys.exit(0)
        else:
            print(Fore.RED + 'Invalid command.' + Fore.RESET)
            pass

    return user_action



def scan_suspect_users():
    suspect_users = get_suspect_users() # have to make the list first
    for usrs in suspect_users:
        scan_username = suspect_users[usrs]['username']
        scan_userid = str(suspect_users[usrs]['id'])
        scan_user = requests.get(dd+'/u/'+scan_username+'.json', headers=req_headers).json()
        print(Fore.RED + 'Found user: ' + scan_username + Fore.RESET)
        print('User ID: ' + scan_userid)
        print('User bio: ')
        pp.pprint(str(scan_user['user']['bio_raw']))

        print(Fore.YELLOW + 'What would you like to do?')
        print('[S]kip, [d]elete and block IP, [o]pen in browser, [q]uit' + Fore.RESET)

        get_user_action(scan_username, scan_userid)



# scan_suspect_users()

parser = argparse.ArgumentParser(prog="Discourse Spam Checker")
parser.add_argument('--type', '-t', help='Specify which user list to scan. Defaults to \'all\'', choices=['all','suspect','silenced'], default='all')

args = parser.parse_args()

if args.type == 'all':
    scan_suspect_users()
    scan_silenced_users()
elif args.type == 'silenced':
    scan_silenced_users()
elif args.type == 'suspect':
    scan_suspect_users()