#all supporting docs at https://developer.riotgames.com/docs/lol
import your_api_key
import requests
import json
import stringify
import tkinter as tk
import PIL.Image as Image
import PIL.ImageTk as ImageTk
#idk why i have to import pil like this but see https://stackoverflow.com/questions/11911480/python-pil-has-no-attribute-image

print("program start")



#tkinter gui stuff
window = tk.Tk()

#------------------------
#frame spawning stuff here
#------------------------
framePrompt = tk.Frame(master=window)
frameInputs = tk.Frame(master=window)
upperFrameForWidgets = tk.Frame(master=window)

summonerNamePrompt= tk.Label(text="Input summoner name:",
    background="black",
    foreground="white",
    master=framePrompt,
#    relief=tk.RIDGE,
    width=50
)

#summonerNamePrompt.pack()
summonerNameEntryBox= tk.Entry(master=frameInputs)#width=50)
#summonerNameEntryBox.pack()
#TODO: begin laying out blank display widgets here
spacerWidget = tk.Label(text="                            ")
#spacerWidget.pack()
displaySummonerNameStatic = tk.Label(text="Summoner:", relief=tk.SUNKEN,master=upperFrameForWidgets,width=20)
displaySummonerNameDynamic = tk.Label(text="", relief=tk.SUNKEN, master=upperFrameForWidgets,width=20)
displaySummonerLevelStatic = tk.Label(text="Summoner Level:",relief=tk.SUNKEN,master=upperFrameForWidgets,width=20)#, background="black", foreground="white")
#displaySummonerLevelStatic.pack()
displaySummonerLevelDynamic = tk.Label(text="",relief=tk.SUNKEN,master=upperFrameForWidgets,width=20)#, background="white", foreground="black")
#displaySummonerLevelDynamic.pack()
#TODO: displayProfileIconId image loading
displayRankStatic = tk.Label(text="Rank:",relief=tk.SUNKEN,master=upperFrameForWidgets,width=20)
#displayRankStatic.pack()
displayRankDynamic = tk.Label(text="",relief=tk.SUNKEN,master=upperFrameForWidgets,width=20)
#displayRankDynamic.pack()
displayLeaguePointsStatic = tk.Label(text="League Points:",relief=tk.SUNKEN,master=upperFrameForWidgets,width=20)
#displayLeaguePointsStatic.pack()
displayLeaguePointsDynamic = tk.Label(text="",relief=tk.SUNKEN,master=upperFrameForWidgets,width=20)
#displayLeaguePointsDynamic.pack()
displayWinsStatic = tk.Label(text="Ranked Wins:",relief=tk.SUNKEN,master=upperFrameForWidgets,width=20)
#displayWinsStatic.pack()
displayWinsDynamic = tk.Label(text="",relief=tk.SUNKEN,master=upperFrameForWidgets,width=20)
#displayWinsDynamic.pack()
displayChallengesLevelStatic = tk.Label(text="Challenges:",relief=tk.SUNKEN,master=upperFrameForWidgets,width=20)
#displayChallengesLevelStatic.pack()
displayChallengesLevelDynamic = tk.Label(text="",relief=tk.SUNKEN,master=upperFrameForWidgets,width=20)
#displayChallengesLevelDynamic.pack()
displayRankedIcon = tk.Label(height = 8, width = 20)
#TODO: champion stuff
def summonerNameSearch(event):
    entryBoxInput=summonerNameEntryBox.get()
    print("we should search for a summoners name using the api now..., their name: "+entryBoxInput)
    compiledSummonerInfo = mainBackend(entryBoxInput) 
    #schema: Summoner Name, Summoner Level (long), ProfileIconId (int), tier (word), rank (I-IV), leaguePoints (int), wins (int), challengesLevel(str), topChampion:{championId (long), championLevel (int), championPoints (int)}
    if compiledSummonerInfo == "bad_http_request":
        print("bad http request or summoner not found")
        spacerWidget["text"] = "Summoner could not be searched or does not exist"
    else:
        spacerWidget["text"] = "                            "
        summonerDisplayCardDebug(compiledSummonerInfo)
        displaySummonerNameDynamic["text"] = compiledSummonerInfo.get("Summoner Name")
        displaySummonerLevelDynamic["text"] = compiledSummonerInfo.get('Summoner Level')
        displayRankDynamic["text"] = compiledSummonerInfo.get('tier') +" "+ compiledSummonerInfo.get('rank')
        displayLeaguePointsDynamic["text"] = compiledSummonerInfo.get('leaguePoints')
        displayWinsDynamic["text"] = compiledSummonerInfo.get('wins')
        displayChallengesLevelDynamic["text"] = compiledSummonerInfo.get('challengesLevel')
        #time to pick the right ranked icon, see https://www.activestate.com/resources/quick-reads/how-to-add-images-in-tkinter/ for image loading guide on this program
        rankedIconNameStringPath = "league_ranked_icons/"+ compiledSummonerInfo.get('tier') + ".png"
        print(rankedIconNameStringPath) 
        rankedIcon = Image.open(rankedIconNameStringPath)
        displayRankedIcon["height"]="0"
        displayRankedIcon["width"]="0" #i gotta do this funky resize to zero stuff or the PIL.Image resize and Label height/width is gonna conflict with each other and cause glitchy images
        rankedIcon = rankedIcon.resize((120, 120), Image.LANCZOS) #first parameter is size, second parameter is resampling algorithm. LANCZOS replacing Antialias because deprecation
        rankedIconSelectedWidgeted = ImageTk.PhotoImage(rankedIcon)
        displayRankedIcon["image"] = rankedIconSelectedWidgeted
        displayRankedIcon.image = rankedIconSelectedWidgeted

searchButton = tk.Button(text="Search",master=frameInputs)
searchButton.bind('<Button-1>', summonerNameSearch)
#searchButton.pack()

#importation simplification and variable simplification
apikey=your_api_key.API_KEY_URL_SNIPPET
APIKEY=apikey
apiKey=apikey
null=None #yall are weird for making None be null, and not just let null be null *rolls eyes*
rankedValues={
    "IRON":0,
    "BRONZE":1,
    "SILVER":2,
    "GOLD":3,
    "PLATINUM":4,
    "DIAMOND":5,
    "MASTER":6,
    "GRANDMASTER":7,
    "CHALLENGER":8
}
rankedNumbers={
    "I":1,
    "II":2,
    "III":3,
    "IV":4
}

#full url example: apiUrl + "{whatever the api call is in specfic particularity} / query variable" + apikey

#server or region value:
server="na1"
serverList = [ #for future use
    'NA',
    'BR',
    'LAN',
    'LAS',
    'EUW',
    'EUNE',
    'OCE',
    'KR',
    'JP',
    'RU',
    'TR',
    'SG', #Singapore
    'PH',
    'TH', #THAILAND
    'TW',
    'VN'
]
justNa = ['NA'] #literally just na
server2routingValuesConverter = { #for future use
    'NA':'na1',
    'BR':'br1',
    'LAN':'la1',
    'LAS':'la2',
    'EUW':'euw1',
    'EUNE':'eun1',
    'OCE':'oc1',
    'KR':'kr',
    'JP':'jp1',
    'RU':'ru',
    'TR':'tr1',
    'SG':'sg2', #Singapore
    'PH':'ph2',
    'TH':'th2', #THAILAND
    'TW':'tw2', #TAIWAN
    'VN':'vn2'
}
serverSelection = tk.StringVar(window)
serverSelection.set(serverList[0]) #default value
#serverSelectionMenu = tk.OptionMenu(window, serverSelection, *serverList)
#serverSelectionMenu = tk.OptionMenu(window, serverSelection, *justNa)
serverSelectionMenu = tk.OptionMenu(frameInputs, serverSelection, *justNa)
#serverSelectionMenu.pack()
server=server2routingValuesConverter[serverSelection.get()]
#print(server)
#"static" api url using region
apiUrl="https://" + server + ".api.riotgames.com"
#TODO: need to make server dropdown list actually work



#------------------------
#packing occurs here
#.pack() is used on the master window from the top down on various widgets and frames
#frames have a local .grid() method of arranging widgets inside of them
#------------------------
summonerNamePrompt.pack()
framePrompt.pack(side=tk.TOP,fill=tk.X)
serverSelectionMenu.grid(row=0,column=0)
summonerNameEntryBox.grid(row=0,column=1)
searchButton.grid(row=0, column=2)
frameInputs.pack(side=tk.TOP)
spacerWidget.pack(side=tk.TOP)
displaySummonerNameStatic.grid(row=0,column=0)
displaySummonerNameDynamic.grid(row=0,column=1)
displaySummonerLevelStatic.grid(row = 1, column = 0)
displaySummonerLevelDynamic.grid(row = 1, column = 1)
displayRankStatic.grid(row = 2, column = 0)
displayRankDynamic.grid(row = 2, column = 1)
displayLeaguePointsStatic.grid(row = 3, column = 0)
displayLeaguePointsDynamic.grid(row = 3, column = 1)
displayWinsStatic.grid(row = 4, column = 0)
displayWinsDynamic.grid(row =4, column = 1)
displayChallengesLevelStatic.grid(row=5, column=0)
displayChallengesLevelDynamic.grid(row=5,column=1)
upperFrameForWidgets.pack(side=tk.TOP)
displayRankedIcon.pack(side=tk.TOP)

#===================================================================================================================
#end of global defining nonsense
#===================================================================================================================




#query function for ez pz modular coding
def getQueryUrl(query):
    queryUrl=apiUrl + query + apikey
    #print(queryUrl)
    return queryUrl

def summonerDisplayCardDebug(summonerDisplayCard):
    print("display card:")
    print(summonerDisplayCard)
    return

def getSummonerNameInfo(summonerName):
    query="/lol/summoner/v4/summoners/by-name/"+summonerName
    print(getQueryUrl(query))
    r = requests.get(getQueryUrl(query)) #{id, accountId, puuid, name, profileIconID, revisionDate, summonerLevel}, this is a request response type object
    #r.json()
    #rd = r.json() #converts response object into a python dictionary
    print(r) #prints https response code
    #print(r.json()) #prints actual json format content
    #print(rd) #does same as line above
    #print(str((r.json()).get('summonerLevel')) + " asdf") #does work, note that r.json().get() will return an int
    #print(str(rd.get('summonerLevel'))+ " asdf") #does work, note that rd.get() is apparently an int type
    
    return r
#end summonerNameInfo

def getSummonerRankedInfo(summonerID):
    query="/lol/league/v4/entries/by-summoner/"+summonerID
    r = requests.get(getQueryUrl(query)) #[{id, queueType, tier (gold etc), rank (3 etc), summonerID, summonerName, leaguePoints, wins, losses, veteran (bool), inactive (bool), freshBlood (bool), hotStreak (bool)},{returns flex queue if available}]
    #print(r.json()) #it's a list of dictionaries, can be one or two dictionaries pending on if summoner is placed in 1 or both ranked queues
    
    return r
#end getSummonerRankedInfo

def getChallengesInfo(puuid):
    queury="/lol/challenges/v1/player-data/"+puuid
    r = requests.get(getQueryUrl(queury)) #{totalPoints:{level, current, max, percentile}, stuff... go read docs https://developer.riotgames.com/apis#lol-challenges-v1/GET_getPlayerData}
    return r
#end getChallengesInfo

def getTopChampionMastery(summonerID):
    champMasteryAPIkey = str(apikey).replace('?','&')
    query="/lol/champion-mastery/v4/champion-masteries/by-summoner/"+summonerID+"/top?count=1"+champMasteryAPIkey
    queryUrl=apiUrl + query
    #print(queryUrl)
    #r = requests.get(getQueryUrl(query)) #[{championId, championLevel, championPoints, lastPlayTime, championPointsSinceLastLevel, championPointsUntilNextLevel, chestGranted, tokensEarned, summonerId}]
    r=requests.get(queryUrl)
    return r
#end getTopChampMastery



#MAIN FUNCTION
def mainBackend(summonerName):
    #summonerName="berisoniqui"
    #summonerName="DrBigMa"
    #summonerName="Leilaxb"
    #summonerName=input("Enter a summoner name: ")
    summonerIDcard = getSummonerNameInfo(summonerName)
    summonerIDcardHttpCodeStringified = str(summonerIDcard)
    print ("summonerIDcard is " + summonerIDcardHttpCodeStringified)
    if summonerIDcardHttpCodeStringified != "<Response [200]>":
        #print("bad http response error")
        return "bad_http_request"
    summonerIDcard = summonerIDcard.json()
    #print(summonerIDcard)
    #print(str(summonerIDcard.get('summonerLevel'))+" asdf")
    print(summonerName)
    print("id: " + summonerIDcard.get('id'))
    #just gonna get all the important info about the summoner into a dictionary for simplification stuff and final product
    summonerDisplayCard = {
        "Summoner Name": summonerName,
        "Summoner Level": summonerIDcard.get('summonerLevel'), #this is a Long type
        "ProfileIconId":int(summonerIDcard.get('profileIconId'))
    }#schema: Summoner Name, Summoner Level (long), ProfileIconId (int), tier (word), rank (I-IV), leaguePoints (int), wins (int), challengesLevel(str), topChampion:{championId (long), championLevel (int), championPoints (int)}
    
    summonerRankedInfoList = getSummonerRankedInfo(str(summonerIDcard.get('id'))).json()
    isRanked=False
    betterRankedDict={}
    if len(summonerRankedInfoList) == 1:
        betterRankedDict = summonerRankedInfoList[0]
        isRanked=True
    elif len(summonerRankedInfoList) == 2: #two ranked queues? compare their hard ranked tier: gold, diamond etc
        isRanked=True
        if rankedValues.get(str(summonerRankedInfoList[0].get('tier'))) > rankedValues.get(str(summonerRankedInfoList[1].get('tier'))):
            betterRankedDict=summonerRankedInfoList[0]
        elif rankedValues.get(str(summonerRankedInfoList[0].get('tier'))) < rankedValues.get(str(summonerRankedInfoList[1].get('tier'))):
            betterRankedDict=summonerRankedInfoList[1]
        else: #conclude that they are the same ranked tier. Now compare in-tier divisions.
            if (str(summonerRankedInfoList[0].get('tier')) != "MASTER") and (str(summonerRankedInfoList[0].get('tier')) != "GRANDMASTER") and (str(summonerRankedInfoList[0].get('tier')) != "CHALLENGER"): #non master+ can compare with Iv,II, etc
                if rankedNumbers.get(str(summonerRankedInfoList[0].get('rank'))) > rankedNumbers.get(str(summonerRankedInfoList[1].get('rank'))):
                    betterRankedDict=summonerRankedInfoList[0]
                else:
                    betterRankedDict=summonerRankedInfoList[1]
            else: #must compare with lp cuz master, gm, and cha are all homogenous within each other
                if int(summonerRankedInfoList[0].get('leaguePoints')) > int(summonerRankedInfoList[1].get('leaguePoints')):
                    betterRankedDict=summonerRankedInfoList[0]
                else: #assumes that both ranked queues are the same lp or the second queue is higher
                    betterRankedDict=summonerRankedInfoList[1]
    else: #if summoner is unranked or it doesnt conform to the above, it's gonna be a list looking exactly like this: []
        betterRankedDict.update({"tier":"UNRANKED"})
        betterRankedDict.update({"rank":""})
        betterRankedDict.update({"leaguePoints":""})
        betterRankedDict.update({"wins":""})

    if isRanked==True:
        betterRankedDict.pop("leagueId") #throws error on unranked players because no league id
        betterRankedDict.pop("queueType") #throws error on unranked players
        betterRankedDict.pop("summonerId") #this will also throw an error if unranked? 
        betterRankedDict.pop("summonerName")
        betterRankedDict.pop("losses")
        betterRankedDict.pop("veteran")
        betterRankedDict.pop("inactive")
        betterRankedDict.pop("freshBlood")
        betterRankedDict.pop("hotStreak")
        summonerDisplayCard.update(betterRankedDict)
    else:
        summonerDisplayCard.update(betterRankedDict)

    challengesInfo = getChallengesInfo(str(summonerIDcard.get("puuid"))).json() #{totalPoints:{level, current, max, percentile}, stuff... go read docs https://developer.riotgames.com/apis#lol-challenges-v1/GET_getPlayerData}
    challengesLevel=str((challengesInfo.get('totalPoints')).get("level"))
    summonerDisplayCard.update({"challengesLevel":challengesLevel})

    topChampionMastery = getTopChampionMastery(str(summonerIDcard.get('id'))).json() #[{championId, championLevel, championPoints, lastPlayTime, championPointsSinceLastLevel, championPointsUntilNextLevel, chestGranted, tokensEarned, summonerId}]
    #print("topChampionMaster is " +str(topChampionMastery))
    if len(topChampionMastery)!=0: #TODO: may throw an error when i display on a widget
        topChampionMasteryRevised = {
            "championId":topChampionMastery[0].get('championId'),
            "championLevel":topChampionMastery[0].get('championLevel'),
            "championPoints":topChampionMastery[0].get('championPoints'),
        }
        summonerDisplayCard.update({"topChampion":topChampionMasteryRevised})

    #summonerDisplayCardDebug(summonerDisplayCard)
    return summonerDisplayCard
#END MAINBACKEND

window.mainloop()
print("program end")
