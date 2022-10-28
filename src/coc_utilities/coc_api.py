import json
import os
import requests

from dotenv import load_dotenv

env_path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), '.env')
load_dotenv(dotenv_path=env_path)

url = 'https://api.clashofclans.com/v1'
auth = f"Bearer {os.environ['COC_TOKEN']}"
headers = {
    'Accept': 'application/json',
    'authorization' : auth
}

def get_member(player_tag: str) -> dict:
    tag = player_tag.split('#')[1]
    response = requests.get(f'{url}/players/%23{tag}', headers=headers)
    member_json = response.json()

    return member_json

def get_members(clan_tag: str) -> dict:
    tag = clan_tag.split('#')[1]
    response = requests.get(f'{url}/clans/%23{tag}/members', headers=headers)
    members_json = response.json()

    return members_json

def get_members_for_war() -> list:
    war_participants = []
    member_info = {}
    clan_members = get_members(os.environ['COC_CLAN_TAG'])

    for member in clan_members['items']:
        war = True if get_member(member['tag'])['warPreference'] == 'in' else False
        member_info[member['name']] = {
            'tag': member['tag'],
            'war': war
        }
    
    for key in member_info.keys():
        if member_info[key]['war']:
            war_participants.append(key)

    return war_participants

def update_strikes(player: str, add: bool, reset=False) -> dict:
    cache_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'cache.json')
    cache = {}

    with open(cache_path, 'a+') as fp:
        if os.path.getsize(cache_path) != 0:
            fp.seek(0)
            cache = json.load(fp)

    clan_members = get_members(os.environ['COC_CLAN_TAG'])
    if player not in (member['name'] for member in clan_members['items']):
        print(f"'{player}' is not a member of the clan")
        return

    if player in (member['name'] for member in clan_members['items']):
        print(f"'{player}' is a member of the clan")
        if reset:
            cache[player] = {'strikes': 0}
        elif player in (key for key in cache.keys()):
            if add and cache[player]['strikes'] < 3:
                cache[player]['strikes'] = cache[player]['strikes'] + 1
            if not add and cache[player]['strikes'] > 0:
                cache[player]['strikes'] = cache[player]['strikes'] - 1
        else:
            cache[player] = {'strikes': 1}

    with open(cache_path, 'w') as fp:
        json.dump(cache, fp)

    return cache

def get_strikes() -> dict:
    cache_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'cache.json')
    cache = {}

    with open(cache_path, 'a+') as fp:
        if os.path.getsize(cache_path) != 0:
            fp.seek(0)
            cache = json.load(fp)

    return cache