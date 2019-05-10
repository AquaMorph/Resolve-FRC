import tbapy
import re
import operator
import datetime
from pytube import YouTube
import DaVinciResolveScript as drs

# Reads TBA access key from tba.txt file.
def getTBAKey():
    tbafile = open('tba.txt', 'r')
    key = tbafile.read()
    tbafile.close()
    return key

# Prints a list of subfolders in a folder.
def printSubFolderNames(folder, mp):
    subfolders = folder.GetSubFolders()
    for f in subfolders:
        print(f, subfolders[f].GetName())

# Returns subfolder with the given name.
def getSubFolderByName(folder, name, mp):
    subfolders = folder.GetSubFolders()
    for f in subfolders:
        if name in subfolders[f].GetName():
            return subfolders[f]

# Converts camera timestamp to UNIX time.
def timeStampToUnix(timestamp, timeZoneOffset=None):
    t = datetime.datetime.strptime(timestamp, '%a %b %d %H:%M:%S %Y')
    if timeZoneOffset is None:
        return int(t.timestamp())
    else:
        return timeStampToUnix(timestamp) - (timeZoneOffset * 60 * 60)

tba = tbapy.TBA(getTBAKey())

# Gets a list of matches at an event.
def getMatches(event):
    matches = tba.event_matches(event)
    matches.sort(key=operator.attrgetter('actual_time'))
    return matches

# Downloads match video from YouTube.
def downloadMatchVideo(match):
    videos = match['videos']
    for video in videos:
        if video['type'] == 'youtube':
            print('Downloading')
            YouTube('https://www.youtube.com/watch?v={}'.format(video['key'])).streams.first().download('.', match['key'])

matches = getMatches('2019ncwak')
for match in matches:            
    print(match['key'], match['actual_time'])
    if(match['key'] == ''):
        downloadMatchVideo(match)

resolve = drs.scriptapp("Resolve")
ms = resolve.GetMediaStorage()
pm = resolve.GetProjectManager()
project = pm.GetCurrentProject()
mp = project.GetMediaPool()
rootFolder = mp.GetRootFolder()

matchFolder = getSubFolderByName(rootFolder, 'Matches', mp)
print(matchFolder)
clips = matchFolder.GetClips()
for i in clips:
    dt = timeStampToUnix(clips[i].GetClipProperty()['Date Created'], 5)
    print(dt)

