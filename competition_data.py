from types import *
from collections import Counter
import operator
import re

def getCompetitionDetails(wikiPages, seasons):
    competitionDetails = dict()
    newerSeasons = [18,19] # these season have a different page layout and must be handled differently
    for sn in seasons:
        weeklyDetails = []
        seasonPage = wikiPages[sn]      #get BS element for this season
        seasonPage = seasonPage.find("div", attrs={"id":"content"}).find("div", attrs={"id":"bodyContent"})
        seasonPage = seasonPage.find("div", attrs={"id":"mw-content-text"})
        bodyElements = seasonPage.find_all(['h2','h3','p','table']) #put body elements into a list so they can be parsed through
        

        # iterater over the list of body elements to find the relevent data
        for i, element in enumerate(bodyElements):
            if sn in newerSeasons:
                # find the episodes section
                if element.name == 'h2' and not type(element.span) == NoneType:
                    if element.span.text == "Episodes":
                        # capture each table row into the episodesDetail list excluding 
                        # the first tr, which is the table header.
                        # the rows are arranged in pairs, with the first the row containing 
                        # the episode num, title and air date and the second row containing
                        # the episode summary
                        episodesDetails = bodyElements[i+1].find_all('tr')
                        for episodeIndex, episodeDetails in enumerate(episodesDetails):
                            
                            
                            if not episodeIndex % 2 == 0:
                                episodeNumber = (episodeIndex+1) / 2
                                if episodeIndex+1 < len(episodesDetails):
                                    episodeSummary = episodesDetails[episodeIndex+1].text
                                    episodeTitle = episodeDetails.find('td', {'class':'summary'}).text
                                    if "Week" in episodeTitle:
                                        weeklyDetails.append(episodeSummary)
                                    
                # get the tab
            else:
                text = element.find(text=True)
                if "Week" in str(text):
                    parsingSection = True
                    nextElementIndex = i+1
                    # parse through the next elements until we reach 
                    # elements pertaining to the next week
                    while parsingSection:
                        if not (nextElementIndex < len(bodyElements)):
                            break

                        nextElement = bodyElements[nextElementIndex]
                        # if the next element is an h3 element then it is the header of the 
                        # next we and we should stop here
                        if nextElement.name == 'h2' or nextElement.name == 'h3':
                            parsingSection = False
                            weeklyDetails.append(bodyElements[i+1:nextElementIndex])
                        # otherwise we go to the next element
                        else:
                            nextElementIndex += 1


        competitionDetails[sn] = weeklyDetails 

    return competitionDetails




def getContestantCompData(competitionDetails, allContestants):
    contestantCompData = {} 
    newerSeasons = [18, 19]
    
    for sn in list(allContestants.keys()):
        contestantsData = {}
        # for each episode determine who had a group or one on one date and whether they got a rose 
        for weekIndex, weekDetails in enumerate(competitionDetails[sn]):
            if sn in newerSeasons:
                episodeSummary = weekDetails
                hasIndividualDates = 'one-on-one' in episodeSummary.lower() or 'two-on-one' in episodeSummary.lower()
                hasGroupDates = 'group date:' in episodeSummary.lower()
                
                if hasIndividualDates or hasGroupDates:
                    for marker in ['one-on-one', 'group date:', 'two-on-one']:
                        dateType = marker.replace(' date:','') 
                        if not marker in episodeSummary.lower():
                            continue
                        # find all indexes of the markers specified
                        markerIndexes = [m.end() for m in re.finditer(marker, episodeSummary.lower())]
                        for markerIndex in markerIndexes:                        
                            endOfContestants = markerIndex + episodeSummary[markerIndex:].index('. ')
                            contestants = episodeSummary[markerIndex:endOfContestants]
                            endOfSection = episodeSummary[markerIndex:].index('\n') + markerIndex
                            section = episodeSummary[markerIndex:endOfSection]
                            generateRoseData(allContestants[sn], contestantsData, weekIndex+1, dateType, contestants, section)

            else:
                for detailsIndex, details in enumerate(weekDetails):
                    if not(type(details.b) == NoneType):
                        dateType = details.b.text.lower()
                        if "one-on-one" in dateType or "two-on-one" in dateType or "group" in dateType:
                            start = details.text.index(':') +2
                            end = details.text.index('. ')
                            contestants = details.text[start:end]
                            generateRoseData(allContestants[sn], contestantsData, weekIndex+1, dateType, contestants, details.text)
                                    
        contestantCompData[sn] = contestantsData
        
    return contestantCompData
  
def generateRoseData(allContestants, contestantsData, week, dateType, contestantsOnDate, section):

    # find the contestants that are on the date 
    contestants = []
    for contestant in allContestants:
        contestantFirstName = contestant['name'].split(' ')[0]
        if contestantFirstName in contestantsOnDate:
            contestants.append(contestantFirstName)
    # account for any contestants with same name
    contestants = dict(Counter(contestants))
    contestantsToRemove = []
    contestantsToAdd = []
    for name in contestants:
        if contestants[name] > 1:
            contestantsToRemove.append(name)
            for contestant in allContestants:
                if name in contestant['name']:
                    fullName = contestant['name'].split(' ')
                    if len(fullName) == 3:
                        firstName, middleName, lastName = fullName
                        if '(' in lastName and ')' in lastName:
                            ref = lastName
                            lastName = middleName
                            searchableName = firstName+' '+ref
                    else:
                        firstName, lastName = fullName
                        searchableName = firstName+' '+lastName[0]
                        #searchableName2 = firstName+lastName[0]
                    if searchableName in contestantsOnDate:
                        contestantsToAdd.append(searchableName)

    for name in contestantsToRemove:
        del contestants[name]

    for name in contestantsToAdd:
        contestants[name] = 1

    contestants = contestants.keys()
    

    # determine who got a rose
    if 'rose' in section:
        roseIndex = section.index('rose')
        endOfSentence = section[roseIndex:].index('.') + roseIndex
        startOfSentence = endOfSentence - section[:endOfSentence][::-1].index('.') + 1
        roseSentence = section[startOfSentence:endOfSentence]
        
        for contestant in contestants:
            contestantFirstName = contestant.split(' ')[0]
            receivedRose = False
            for got in ['got', 'receiv', 'gets', 'presents', 'gives','holds','has','giving', 'gave', 'extend']:
                if got in roseSentence and not (' not ' in roseSentence):
                    if contestantFirstName in roseSentence:
                        receivedRose = True
                        break
                    elif 'one' in dateType: # we assume the pronoun refers to contestant on the date
                            receivedRose = True
                            break
                    elif 'group' in dateType: # we assume the pronoun refers to the last mentioned contestant
                        contestantIndex = {}
                        for c in contestants:
                            contestantIndex[c.split(' ')[0]] = section[:endOfSentence][::-1].index(c.split(' ')[0][::-1])

                        closestContestant = min(contestantIndex.iteritems(), key=operator.itemgetter(1))[0]
                        if closestContestant in contestant:
                            receivedRose = True
                            break
                            
            compData = (week, dateType, receivedRose)

            if contestant in contestantsData:
                contestantsData[contestant].append(compData)
            else:
                contestantsData[contestant] = [compData] 
def getWeeklyCompData(contestantCompData):
    result = {}
    for sn in contestantCompData:
        weeklyCompData = {}
        for contestant in contestantCompData[sn]: 
            dates = contestantCompData[sn][contestant]
            for week,dateType,receivedRose in dates:
                if not week in weeklyCompData:
                    weeklyCompData[week] = {}
                if not contestant in weeklyCompData[week]:
                    weeklyCompData[week][contestant] = {}
                if not dateType in weeklyCompData[week][contestant]:
                    weeklyCompData[week][contestant][dateType] = {}

                weeklyCompData[week][contestant][dateType] = receivedRose
        result[sn] = weeklyCompData
    return result

def addCompetitionData(seasonsDict, contestantCompData):
    for sn in seasonsDict:    
        for contestant in seasonsDict[sn]:
            contestant['group_dates'] = 0
            contestant['individual_dates'] = 0
            contestant['roses_from_group_dates'] =  0
            contestant['roses_from_individual_dates'] = 0
            for contestantFirstName in contestantCompData[sn]:
                contestantName = "None"
                if contestantFirstName == "" or " " in contestantFirstName or len(contestantFirstName) < 3:
                    continue
                if contestantFirstName[-1].isupper():
                    contestantName = contestantFirstName[:-1] + ' ' + contestantFirstName[-1]

                if contestantFirstName in contestant['name'] or contestantName in contestant['name']:
                    dates = contestantCompData[sn][contestantFirstName]
                    numGroupDates = 0
                    numIndividualDates = 0
                    numRoseOnGroupDates = 0
                    numRoseOnIndividualDates = 0
                    for week, dateType, receivedRose in dates:
                        if 'group' in dateType.lower():
                            numGroupDates += 1
                            if receivedRose:
                                numRoseOnGroupDates += 1
                        if 'one' in dateType.lower():
                            numIndividualDates += 1
                            if receivedRose:
                                numRoseOnIndividualDates += 1
                        
                    
                    contestant['group_dates'] = numGroupDates
                    contestant['individual_dates'] = numIndividualDates
                    contestant['roses_from_group_dates'] =  numRoseOnGroupDates
                    contestant['roses_from_individual_dates'] = numRoseOnIndividualDates
                    break

