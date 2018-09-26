import sys
import os

fileName = sys.argv[1]
f = open(fileName, 'rb')
outFile = open(fileName.split('.avi')[0] + '_mosh.avi', 'wb')

print 'Reading file ' + fileName + '...'
inputFile = f.read()

frames = inputFile.split('\x00\xdc')
print '\tDone'


iframe = '\x00\x01\xb0'
regFrameLimit = 1
regFrames = 0
frameCount = 0

print 'Moshing...'
for frame in frames:
    if regFrameLimit > regFrames:
        outFile.write(frame + '\x00\xdc')

        if iframe in frame:
            regFrames += 1
    else:
        if frameCount < 15 and not iframe in frame: #not iframe in frame and frameCount < 20:
            outFile.write(frame + '\x00\xdc')
            frameCount += 1
        else:
            outFile.write(os.urandom(len(frame)) + '\x00\xdc')
            frameCount = 0

outFile.close()

print '\tDone.'
