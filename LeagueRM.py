# Python v3. must "pip install requests"
import requests # allows easy use of JSONs from API
import sys # allows closing of program in try/except

def requestSummonerData(region, summonerName, APIKey):
    URL = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v1.4/summoner/by-name/" + summonerName + "?api_key=" + APIKey
    response = requests.get(URL) # Gets the JSON File
    return response.json() # Return JSON File

def requestChampionData(championName, APIKey):
    URL = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion?api_key=" + APIKey
    response = requests.get(URL) # Gets the JSON File
    return response.json() # Return JSON File

def requestChampionHistory(region, ID, CID, APIKey):
    URL = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v2.2/matchlist/by-summoner/" + ID + "?championIds=" + CID + "&rankedQueues=TEAM_BUILDER_RANKED_SOLO&beginIndex=0&endIndex=5&api_key=" + APIKey
    response = requests.get(URL) # Gets the JSON File
    return response.json() # Return JSON File

def requestGameMatch(region, MID, APIKey):
    URL = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v2.2/match/" + MID + "?api_key=" + APIKey
    response = requests.get(URL) # Gets the JSON File
    return response.json() # Return JSON File

def requestRuneData(runeId, APIKey):
    URL = 'https://global.api.pvp.net/api/lol/static-data/na/v1.2/rune/' + runeId + '?api_key=' + APIKey
    response = requests.get(URL) # Gets the JSON File
    json = response.json() # Stores JSON File
    return str(json['name']) # Return Rune Name

def getParticipantIdentity(MatchJSON, ID):
    try:
        for i in range(10):
            if(MatchJSON['participantIdentities'][i]['player']['summonerId'] == int(ID)):
                PID = MatchJSON['participantIdentities'][i]['participantId']
    except:
        print("No Riot API Calls remaining. Try again later.")
        sys.exit(1)
    return PID

def getRunes(MatchJSON, ID, PID, APIKey):
    for i in range(len(MatchJSON['participants'][PID-1]['runes'])):
        rank = str(MatchJSON['participants'][PID-1]['runes'][i]['rank'])
        runeId = str(MatchJSON['participants'][PID-1]['runes'][i]['runeId'])
        runeName = requestRuneData(runeId, APIKey)
        print(rank + 'x' + ' ' + runeName)
    return
    
def main():
    # Introduction
    print("Hello! This is my program. It returns the last 5 rune pages a summoner")
    print("has used on a particular champion. Example regions are: NA, KR, EUW.")
    print("DO NOT PUT SPACES ANYWHERE BELOW, even for summoner / champion names.")
    print("Champion names MUST start with a capital letter and then lowercase letters.")
    print("Here is the list of exceptions: AurelionSol, Chogath, DrMundo, FiddleSticks,")
    print("JarvanIV, Khazix, KogMaw, Leblanc, LeeSin, MasterYi, MissFortune, MonkeyKing,")
    print("RekSai, TahmKench, TwistedFate, Velkoz, XinZhao.\n")

    # Inputs
    region = (str)(input('Region: ')).lower()
    summonerName = (str)(input('Summoner Name: ')).lower()
    championName = (str)(input('Champion Name: '))
    APIKey = (str)(input('Type in your API Key here: '))

    # Look up their Summoner ID.
    try:
        responseJSON = requestSummonerData(region, summonerName, APIKey)
    except:
        print("Invalid Region or APIKey.")
        sys.exit(1)
    
    # Save their Summoner ID.
    try:
        ID = responseJSON[summonerName]['id']
        ID = str(ID)
    except:
        print("Invalid summoner name.")
        sys.exit(1)

    # Look up list of Champions and IDs.
    responseJSON2 = requestChampionData(championName, APIKey)

    # Translate Champion Name to Champion ID.
    try:
        CID = responseJSON2['data'][championName]['id']
        CID = str(CID)
    except:
        print("Invalid champion name.")
        sys.exit(1)

    # Look for 5 matches of that champion
    responseJSON3 = requestChampionHistory(region, ID, CID, APIKey)

    # Save the 5 match history IDs
    try:
        MID = []
        for i in range(5):
            temp = responseJSON3['matches'][i]['matchId']
            temp = str(temp)
            MID.append(temp)
    except:
        print("Either Summoner has not played 5 games of this champion in 2017 solo ranked,")
        print("OR Riot APIKey has ran out of calls early on in the program: Try again.")
        sys.exit(1)

    # Save the 5 match history JSONs
    MatchJSON = []
    for i in range(5):
        temp = requestGameMatch(region, MID[i], APIKey)
        MatchJSON.append(temp)

    # Save the 5 participant IDs from matches
    PID = []
    for i in range(5):
        temp = getParticipantIdentity(MatchJSON[i], ID)
        PID.append(temp)

    # Print the runes used in the 5 matches
    for i in range(5):
        print('Match ' + str(i+1) + ': ')
        getRunes(MatchJSON[i], ID, PID[i], APIKey)

# Start
main()