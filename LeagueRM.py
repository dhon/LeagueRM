# Python v3. must cmd "pip install requests"
import requests # allows easy use of JSONs from API
import sys # allows closing of program in try/except
import sqlite3 # database

# summoner-v1.4
def requestSummonerID(region, summonerName, APIKey):
    URL = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v1.4/summoner/by-name/" + summonerName + "?api_key=" + APIKey
    JSON = requests.get(URL).json()

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
    JSON = requests.get(URL).json()

    try:
        CID = JSON['data'][championName]['id']
        CID = str(CID)
    except:
        print("Invalid champion name.")
        sys.exit(1)
    return CID

# matchlist-v2.2
def requestMatchID(region, SID, CID, APIKey):
    URL = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v2.2/matchlist/by-summoner/" + SID + "?championIds=" + CID + "&rankedQueues=TEAM_BUILDER_RANKED_SOLO&beginIndex=0&endIndex=5&api_key=" + APIKey
    JSON = requests.get(URL).json()

    try:
        MID = []
        for i in range(5):
            temp = JSON['matches'][i]['matchId']
            temp = str(temp)
            MID.append(temp)
    except:
        print("Summoner has not played five 2017 ranked solo games on this champion.")
        sys.exit(1)
    return MID

# match-v2.2
def requestGameMatch(region, MID, APIKey):
    URL = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v2.2/match/" + MID + "?api_key=" + APIKey
    JSON = requests.get(URL).json()

    try:
        test = JSON['participantIdentities'][0]['player']['summonerId']
        test = str(test)
    except:
        print("No API Calls remaining. Try again later.")
        sys.exit(1)
    return JSON

# lol-static-data-v1.2
def requestRuneData(runeId, APIKey):
    URL = 'https://global.api.pvp.net/api/lol/static-data/na/v1.2/rune/' + runeId + '?api_key=' + APIKey
    JSON = requests.get(URL).json()
    rune = []
    rune.append(JSON['rune']['type'])
    rune.append(JSON['name'])
    return rune

def getParticipantID(MatchJSON, SID):
    for i in range(10):
        if(MatchJSON['participantIdentities'][i]['player']['summonerId'] == int(SID)):
            PID = MatchJSON['participantIdentities'][i]['participantId']
    return PID

def getRunes(MatchJSON, PID, APIKey):
    black = ""
    red = ""
    yellow = ""
    blue = ""
    for i in range(len(MatchJSON['participants'][PID-1]['runes'])):
        rank = str(MatchJSON['participants'][PID-1]['runes'][i]['rank'])
        runeId = str(MatchJSON['participants'][PID-1]['runes'][i]['runeId'])
        rune = requestRuneData(runeId, APIKey)
        if(rune[0] == 'black'):
            if(len(black) < 3):
                black = rank + 'x ' + rune[1]
            else:
                black = black + ', ' + rank + 'x ' + rune[1]
        elif(rune[0] == 'red'):
            if(len(red) < 3):
                red = rank + 'x ' + rune[1]
            else:
                red = red + ', ' + rank + 'x ' + rune[1]
        elif(rune[0] == 'yellow'):
            if(len(yellow) < 3):
                yellow = rank + 'x ' + rune[1]
            else:
                yellow = yellow + ', ' + rank + 'x ' + rune[1]
        elif(rune[0] == 'blue'):
            if(len(blue) < 3):
                blue = rank + 'x ' + rune[1]
            else:
                blue = blue + ', ' + rank + 'x ' + rune[1]
        else:
            print("Something went wrong with the runes...")
            sys.exit(1)
    runes = []
    runes.append(black)
    runes.append(red)
    runes.append(yellow)
    runes.append(blue)
    print("Blacks: " + runes[0])
    print("Reds: " + runes[1])
    print("Yellows: " + runes[2])
    print("Blues: " + runes[3])
    return runes

# SQLite Commands Below
def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS runes(champion TEXT, count INTEGER, black TEXT, red TEXT, yellow TEXT, blue TEXT)")

def data_entry(champion, runes):
    black = runes[0]
    red = runes[1]
    yellow = runes[2]
    blue = runes[3]
    c.execute("SELECT * FROM runes WHERE champion = ? AND black = ? AND red = ? AND yellow = ? AND blue = ?",
        (champion, black, red, yellow, blue))
    data = c.fetchall()
    if(len(data) > 0):
        count = data[0][1]
        c.execute("UPDATE runes SET count = ? WHERE champion = ? AND black = ? AND red = ? AND yellow = ? AND blue = ?",
            (count+1, champion, black, red, yellow, blue))
    else:
        c.execute("INSERT INTO runes(champion, count, black, red, yellow, blue) VALUES (?, ?, ?, ?, ?, ?)",
        (champion, 1, black, red, yellow, blue))
    conn.commit()
    
def main():
    # Introduction
    print("Hello! This is my program. It returns the last 5 rune pages a summoner")
    print("has used on a particular champion. Allowed regions are: NA, KR, EUW.")
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
    if(region != 'na' and region != 'euw' and region != 'kr'):
        print('Invalid region')
        sys.exit(1)

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
    runes = []
    for i in range(5):
        print('Match ' + str(i+1) + ': ')
        temp = getRunes(MatchJSON[i], PID[i], APIKey)
        runes.append(temp)

    # Store runes in SQLite database
    for i in range(5):
        data_entry(championName, runes[i])

# Start
create_table()
conn = sqlite3.connect('LeagueDB.db')
c = conn.cursor()
main()
c.close()
conn.close()