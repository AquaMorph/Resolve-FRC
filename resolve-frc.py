import tbapy
import re
import operator
from pytube import YouTube

# Reads TBA access key from tba.txt file.
def getTBAKey():
    tbafile = open('tba.txt', 'r')
    key = tbafile.read()
    tbafile.close()
    return key

tba = tbapy.TBA(getTBAKey())

# Gets a list of matches at an event.
def getMatches(event):
    matches = tba.event_matches(event)
    matches.sort(key=operator.attrgetter('actual_time'))
    return matches
    

matches = getMatches('2019ncwak')
for match in matches:
    videos = match['videos']
    for video in videos:
        print(video['key'])
        if (match['key'] == '2019ncwak_f1m2'):
            print('Downloading')
            YouTube('https://www.youtube.com/watch?v={}'.format(video['key'])).streams.first().download('.', match['key'])
    print(match['key'], match['actual_time'])
