from types import *
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
                                print 'Episode', episodeNumber
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




def getContestantCompData(competitionDetails, seasons):
    contestantCompData = {} 
    newerSeasons = [18, 19]
    for sn in seasons:
        contestantsData = {}
        for weekIndex, weekDetails in enumerate(competitionDetails[sn]):
            if sn in newerSeasons:
                episodeSummary = weekDetails
                hasIndividualDates = 'One-on-One Date:' in episodeSummary
                hasGroupDates = 'Group Date:' in episodeSummary
                hasNoDates = True
                # find the one on one dates
                if hasIndividualDates or hasGroupDates:
                    for marker in ['One-on-One Date:', 'Group Date:']:
                        if not marker in episodeSummary:
                            continue
                        start = len(marker)+1+episodeSummary.index(marker)
                        end = start + episodeSummary[start:].index('.')
                        contestants = episodeSummary[start:end]
                        if 'and' in contestants:
                            contestants = contestants.replace(' and', ',')
                        contestants = contestants.replace(' ', '').split(',')

                        for contestant in contestants:
                            if contestant in contestantsData:
                                contestantsData[contestant].append(marker)
                            else:
                                contestantsData[contestant] = [marker]   
                        
                elif ':' in episodeSummary:
                    ends = [m.start() for m in re.finditer(':', episodeSummary)]
                    #start = [start + episodeSummary[start:].index('.') for start in starts]
                    contestants = []
                    for end in ends:
                        start = end-10
                        substring = episodeSummary[start:end]
                        if '\n' in substring:
                            start = substring.index('\n')
                            contestant = substring[start+1:end]
                        else:
                            contestant = substring
                        
                        contestants.append(contestant)
                        
                    for contestant in contestants:
                        if contestant in contestantsData:
                            contestantsData[contestant].append('One-on-one Date')
                        else:
                            contestantsData[contestant] = ['One-on-one Date']              
            else:
                for detailsIndex, details in enumerate(weekDetails):
                    if not(type(details.b) == NoneType):
                        eventType = details.b.text
                        if "One-on-one" in eventType or "Two-on-one" in eventType or "Group" in eventType:
                            start = details.text.index(':') +2
                            end = details.text.index('.')
                            contestants = details.text[start:end]
                            if 'and' in contestants:
                                contestants = contestants.replace(' and', ',')
                            contestants = contestants.replace(' ', '').split(',')

                            for contestant in contestants:
                                if contestant in contestantsData:
                                    contestantsData[contestant].append(eventType)
                                else:
                                    contestantsData[contestant] = [eventType]
                                    
        contestantCompData[sn] = contestantsData
        
    return contestantCompData
  


def addCompetitionData(seasonsDict, contestantCompData):
    for sn in seasonsDict:    
        for contestant in seasonsDict[sn]:
            contestant['group_dates'] = 0
            contestant['individual_dates'] = 0
            for contestantFirstName in contestantCompData[sn]:
                contestantName = "None"
                if contestantFirstName == "" or " " in contestantFirstName or len(contestantFirstName) < 3:
                    continue
                if contestantFirstName[-1].isupper():
                    contestantName = contestantFirstName[:-1] + ' ' + contestantFirstName[-1]

                if contestantFirstName in contestant['name'] or contestantName in contestant['name']:
                    compData = contestantCompData[sn][contestantFirstName]
                    compData = '_'.join(compData).lower()
                    groupDates = len([m.start() for m in re.finditer('group', compData)])
                    individualDates = len([m.start() for m in re.finditer('on-one', compData)])
                    contestant['group_dates'] = groupDates
                    contestant['individual_dates'] = individualDates
                    break

