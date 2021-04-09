import sys
import os

fileName = sys.argv[1]
f = open(fileName, 'rb')
outFile = open(fileName.split('.avi')[0] + '_mosh.avi', 'wb')

print 'Reading file ' + fileName + '...'
inputFile = f.read()

frames = inputFile.split('\x00\xdc') #\x00\xdc indicates the end of a frame
print '\tDone'


iframe = '\x00\x01\xb0' #\x00\x01\xb0 denotes an iframe
regFrameLimit = 1
regFrames = 0
frameCount = 0

print 'Moshing...'
for frame in frames:
    #Make sure the first iframe is displayed normally or the video will be an absolute mess
    if regFrameLimit > regFrames:
        outFile.write(frame + '\x00\xdc')
        if iframe in frame:
            regFrames += 1
    else:
        #If we haven't seen 15 non-iframes and we're currently looking at a non-frame write the frame normally
        if frameCount < 15 and not iframe in frame: #not iframe in frame and frameCount < 20:
            outFile.write(frame + '\x00\xdc')
            frameCount += 1
        #If we have either seen fifteen regular frames in a row, or are looking at an iframe garble the frame data
        else:
            outFile.write(os.urandom(len(frame)) + '\x00\xdc') #Need to keep the same number of bytes per frame otherwise the entire video gets messed up
            frameCount = 0

outFile.close()

print '\tDone.'
