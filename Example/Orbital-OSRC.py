import urllib2
import json
from operator import itemgetter
import datetime

instructorList = ["weesun", "knmnyn", "wgx731", "Leventhan", "franklingu", "Limy", "Muhammad-Muneer"]

"""
    This function fetches the json data for a given username
"""
def fetchJSON(userName):
    urlString = "http://osrc.dfm.io/%s.json" % userName
    jsonData = json.load(urllib2.urlopen(urlString))
    return jsonData

"""
    This function extracts the push event data for a given osrc user json
"""    
def getPushEvents(jsonData):
    pushDict = [eventData for eventData in jsonData["usage"]["events"] if eventData["type"] == "PushEvent"]
    return pushDict

"""
    Creates a dictionary mapping instructors to their push event dictionary
"""
def getPushEventDictionary():
    pushEventDictionary = {}

    for instructor in instructorList:
        jsonData = fetchJSON(instructor)
        pushEvents = getPushEvents(jsonData)
        if (pushEvents):
            pushEventDictionary[instructor] = pushEvents[0]
        else:
            print instructor, " push events not found"
    return pushEventDictionary;

"""
    Sorts the instructor activity for a given hour from max to min, and resolves conflicts lexicographically
    Returns a list of tuples of the form (instructor name, hours)
"""
def getSortedHourActivityList(pushEventDictionary, hour):
    #First argument creates a tuple list sorted lexicographically
    hourActivityList = sorted([(instructor, pushEventDictionary[instructor]["day"][hour]) for instructor in pushEventDictionary],
                          key = itemgetter(0), reverse = False)
    
    #Sorts the tuple list by hours
    #Note that since we first sorted by strings, and both sorts are stable, lexicographic ordering for
    #conflicts are preserved
    hourActivityList.sort(key = itemgetter(1), reverse = True)
    return hourActivityList

"""
    Sorts the instructor activity for a given day from max to min, and resolves conflicts lexicographically
    Returns a list of tuples of the form (instructor name, hours)
"""
def getSortedDayActivityList(pushEventDictionary, day):
    dayActivityList = sorted([(instructor, pushEventDictionary[instructor]["week"][day]) for instructor in pushEventDictionary],
                          key = itemgetter(0), reverse = False)
    dayActivityList.sort(key = itemgetter(1), reverse = True)
    return dayActivityList

def outputHourHighScores(pushEventDictionary):
    print "\nHour High Scores: \n"
    for i in range(0, 24):
        hourActivityList = getSortedHourActivityList(pushEventDictionary, i)
        print "%d:00 - %d:00 => %s" % (i, i+1, hourActivityList[0][0])

def outputDayHighScores(pushEventDictionary):
    print "\nDay High Scores: \n"
    for i in range(0, 7):
        dayActivityList = getSortedDayActivityList(pushEventDictionary, i)
        #1990 started on a Monday, and the json data day 0 is Sunday, and python day starts from 1, so we offset by 7
        #For why %A prints day, look up the datetime documentation for python
        print "%s => %s" % (datetime.date(day = i + 7, year = 1990, month = 1).strftime("%A"), dayActivityList[0][0])

def run():
    pushEventDictionary = getPushEventDictionary()
    outputHourHighScores(pushEventDictionary)
    outputDayHighScores(pushEventDictionary)

run()