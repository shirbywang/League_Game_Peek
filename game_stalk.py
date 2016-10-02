#test riot api

import urllib.request
import json

import collections

APP_KEY = 'RGAPI-35CB880B-58C8-4B54-AE8E-6911B4396843'
BASE_URL = 'https://na.api.pvp.net/'

CHAMPION_INFO_URL = 'http://ddragon.leagueoflegends.com/cdn/5.14.1/data/en_US/champion/'
STATIC_CHAMPION_INFO_URL = 'https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion?dataById=true&api_key='

#build summoner info url

def summoner_url_build(user_input: str) -> str:
    '''takes user input of a summoner name and returns a URL'''
    url = BASE_URL + 'api/lol/na/v1.4/summoner/by-name/' + user_input + '?api_key=' + APP_KEY
    return url


#build champion mastery info url

def summoner_champmastery_url_build(playerID: str, champID: str) -> str:
    '''takes user input of a summoner name and returns a URL'''
    url = BASE_URL + 'championmastery/location/NA1/player/' + playerID + '/champion/' + champID + '?api_key=' + APP_KEY
    return url

#build champion url

def champion_url_build(champ: str) -> str:
    '''takes user input of a champion name and returns a URL'''
    #assumes user input is correct
    url = CHAMPION_INFO_URL + champ + '.json'
    return url

# build current game info url

def current_game_url_build(playerID: str) -> str:
    '''takes user input of a summoner ID and returns a URL'''
    url = BASE_URL + 'observer-mode/rest/consumer/getSpectatorGameInfo/NA1/' + playerID + '?api_key=' + APP_KEY
    return url


#return json
def return_json(url: str) -> str:
    '''builds the json string'''
    response = urllib.request.urlopen(url)
    data = response.read()
    response.close()
    string_data = data.decode(encoding = 'utf-8')
    return json.loads(string_data)



#parsing JSON

## summoner info

def get_rank(obj: json, summoner: str) -> str:
    return str(obj[summoner]['summonerLevel'])

def get_playerID(obj:json, summoner: str) -> str:
    return str(obj[summoner]['id'])

## champ info

def get_champID(obj:json, champ: str) -> str:
    return str(obj['data'][champ]['key'])

## champion mastery info

def get_champ_mastery(obj: json) -> str:
    return str(obj['championLevel'])

def get_tokens_earned(obj: json) -> str:
    return str(obj['tokensEarned'])

## get champ name from id

def get_champ_name(obj: json, champID: str) -> str:
    return str(obj['data'][champID]['name']) 

### GAME INFO

def get_players_champ_list(obj: json, summoner_id: str) -> dict:
    gamelist = {}
    same_team = '' 
    for player in obj['participants']:
        if str(player['summonerId']) == str(summoner_id):
            same_team = str(player['teamId'])
    for player in obj['participants']:
        if str(player['teamId']) != same_team:
            item = []
            item.append(player['summonerName']) #player name
            item.append(str(player['championId']))#champ
##            item.append(str(player['teamId']))#teamID
            gamelist[str(player['summonerId'])] = item
    return gamelist



### fixing the user input because the user is stupid

def fix_champ_input(champ: str) -> str:
    new_champ = champ.title().replace(" ", "")
    return new_champ

def fix_summoner_input(summoner: str) -> str:
    new_summoner = summoner.lower().replace(" ", "")
    return new_summoner





if __name__ == '__main__':

    print("Find out the masteries of your opponents with this handy dandy app!")
    print("")

    ## getting all_champs object
    all_champs = return_json(STATIC_CHAMPION_INFO_URL+ APP_KEY) #string with all the champs according to ID

    summoner_real = True
    
    while True:

        try:
                
            input_name = input("your summoner name: ")
            name = fix_summoner_input(input_name)
            summoner_url = summoner_url_build(name)

            summoner_obj = return_json(summoner_url)
            summoner_id = get_playerID(summoner_obj, name)

            current_game_url = current_game_url_build(str(summoner_id))

            current_game_obj = return_json(current_game_url)
            gamelist = get_players_champ_list(current_game_obj, summoner_id)

            for x in gamelist:
                
                print(gamelist[x][0])

                champ_ID = gamelist[x][1]
                
                mastery_url = summoner_champmastery_url_build(x, gamelist[x][1])
                mastery_obj = return_json(mastery_url)
                ##champ_ID = get_champID(champ_obj, champ)

                print("champ: " + get_champ_name(all_champs, champ_ID))
                print("mastery level " + get_champ_mastery(mastery_obj))
                print("tokens earned: " + get_tokens_earned(mastery_obj))

            goodbye = input("would you like to stalk another summoner? (Y/N)")
            if goodbye.capitalize() == 'N':
                exit()

        except:
            print("umm that didn't work can you try that again")



'''
    summoner_real = True
    
    while True:

    ### summoner info

        try: 
            input_name = input("summoner name: ")
            name = fix_summoner_input(input_name)
            summoner_url = summoner_url_build(name)
            summoner_obj = return_json(summoner_url)
            print("rank: " + get_rank(summoner_obj, name))
            summoner_id = get_playerID(summoner_obj, name)
            print(summoner_id)
            summoner_real = True

            ### current game info test
            current_game_url = current_game_url_build(str(summoner_id))
            print(current_game_url)
            current_game_obj = return_json(current_game_url)
            print(current_game_obj)
            
        except:
            print("who da faq is dat lmao")
            summoner_real = False

        while summoner_real:

            try:
                
                ### champ info
                      
                input_champ = input("what champ would you like to find their mastery of? ") 
                champ = fix_champ_input(input_champ)

                champ_url = champion_url_build(champ)  
                champ_obj = return_json(champ_url)
                
                champ_ID = get_champID(champ_obj, champ)


                ### champ mastery info

                mastery_url = summoner_champmastery_url_build(summoner_id, champ_ID)
                mastery_obj = return_json(mastery_url)
                print("mastery level " + get_champ_mastery(mastery_obj))
                print("tokens earned: " + get_tokens_earned(mastery_obj))

            except:
                print("This person has no mastery on that champ.")

            ###end?

            another = input("do you want to find the mastery of a champ? (Y/N)")
            if another.capitalize() == 'N':
                break

        goodbye = input("would you like to stalk another summoner? (Y/N)")
        if goodbye.capitalize() == 'N':
            exit()

'''
