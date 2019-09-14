#!/usr/bin/python3
import requests
import config
import pprint
import json
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



def scan_suspect_users():
    suspect_users = get_suspect_users() # have to make the list first
    for usrs in suspect_users:
        scan_username = suspect_users[usrs]['username']
        scan_user = requests.get(dd+'/u/'+scan_username+'.json', headers=req_headers).json()
        print('Found user: ' + scan_username)
        pp.pprint('User bio: ' + str(scan_user['user']['bio_raw']))


#suspect_users = get_suspect_users()
#pp.pprint(suspect_users)

scan_suspect_users()