# Python v3. must cmd "pip install requests"
import requests # allows easy use of JSONs from API
import sys # allows closing of program in try/except

# summoner-v1.4
def requestSummonerID(region, summonerName, APIKey):
    URL = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v1.4/summoner/by-name/" + summonerName + "?api_key=" + APIKey
    JSON = requests.get(URL).json() # Gets the JSON File

    try:
        SID = JSON[summonerName]['id']
        SID = str(SID)
    except:
        print("Invalid summoner name.")
        sys.exit(1)
    return SID

# lol-static-data-v1.2
def requestChampionID(championName, APIKey):
    URL = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion?api_key=" + APIKey
    JSON = requests.get(URL).json() # Gets the JSON File

    try:
        CID = JSON['data'][championName]['id']
        CID = str(CID)
    except:
        print("Invalid champion name.")
        sys.exit(1)
    return CID # Return JSON File

# matchlist-v2.2
def requestMatchID(region, SID, CID, APIKey):
    URL = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v2.2/matchlist/by-summoner/" + SID + "?championIds=" + CID + "&rankedQueues=TEAM_BUILDER_RANKED_SOLO&beginIndex=0&endIndex=5&api_key=" + APIKey
    JSON = requests.get(URL).json() # Gets the JSON File

    try:
        MID = []
        for i in range(5):
            temp = JSON['matches'][i]['matchId']
            temp = str(temp)
            MID.append(temp)
    except:
        print("Summoner has not played five 2017 ranked solo games on this champion.")
        sys.exit(1)
    return MID # Return JSON File

# match-v2.2
def requestGameMatch(region, MID, APIKey):
    URL = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v2.2/match/" + MID + "?api_key=" + APIKey
    JSON = requests.get(URL).json() # Gets the JSON File

    try:
        test = JSON['participantIdentities'][0]['player']['summonerId']
        test = str(test)
    except:
        print("No API Calls remaining. Try again later.")
        sys.exit(1)
    return JSON # Return JSON File

# lol-static-data-v1.2
def requestRuneData(runeId, APIKey):
    URL = 'https://global.api.pvp.net/api/lol/static-data/na/v1.2/rune/' + runeId + '?api_key=' + APIKey
    JSON = requests.get(URL).json() # Gets the JSON File
    return str(JSON['name']) # Return Rune Name

def getParticipantID(MatchJSON, SID):
    for i in range(10):
        if(MatchJSON['participantIdentities'][i]['player']['summonerId'] == int(SID)):
            PID = MatchJSON['participantIdentities'][i]['participantId']
    return PID

def getRunes(MatchJSON, PID, APIKey):
    for i in range(len(MatchJSON['participants'][PID-1]['runes'])):
        rank = str(MatchJSON['participants'][PID-1]['runes'][i]['rank'])
        runeId = str(MatchJSON['participants'][PID-1]['runes'][i]['runeId'])
        runeName = requestRuneData(runeId, APIKey)
        print(rank + 'x ' + runeName)
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

    # Input
    region = (str)(input('Region: ')).lower()
    summonerName = (str)(input('Summoner Name: ')).lower()
    championName = (str)(input('Champion Name: '))
    APIKey = (str)(input('Riot API Key: '))

    # Look up Summoner ID
    SID = requestSummonerID(region, summonerName, APIKey)

    # Look up Champion ID
    CID = requestChampionID(championName, APIKey)

    # Look for 5 matches of that champion
    MID = requestMatchID(region, SID, CID, APIKey)

    # Save the 5 match JSONs
    MatchJSON = []
    for i in range(5):
        temp = requestGameMatch(region, MID[i], APIKey)
        MatchJSON.append(temp)

    # Save the 5 participant IDs
    PID = []
    for i in range(5):
        temp = getParticipantID(MatchJSON[i], SID)
        PID.append(temp)

    # Print the runes used in the matches
    for i in range(5):
        print('Match ' + str(i+1) + ': ')
        getRunes(MatchJSON[i], PID[i], APIKey)

# Start
main()