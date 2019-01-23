import sys
import os
import random

fileName = sys.argv[1]
f = open(fileName, 'rb')
outFile = open(fileName.split('.avi')[0] + '_mosh.avi', 'wb')

print 'Reading file ' + fileName + '...'
inputFile = f.read()

frames = inputFile.split('\x00\xdc') #Splits at video chunk
#video chunk is '..\xdc', we're only focusing on '\x00\xdc' because there's enough of them in .avi files
#audio chunk is '..\xwb'
print '\tDone'


iframe = '\x00\x01\xb0'
regFrameLimit = 1
regFrames = 0
frameCount = 0
nextFrameLimit = 15

print 'Moshing...'
for frame in frames:
    if regFrameLimit > regFrames:
        outFile.write(frame + '\x00\xdc')

        if iframe in frame:
            regFrames += 1
    else:
        if frameCount < nextFrameLimit and not iframe in frame:
            outFile.write(frame + '\x00\xdc')
            frameCount += 1
        else:
            outFile.write(os.urandom(len(frame)) + '\x00\xdc')
            frameCount = 0
            nextFrameLimit = random.randint(10, 45)

outFile.close()

print '\tDone.'
