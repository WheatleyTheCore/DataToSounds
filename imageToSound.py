#TODO: TRY USING SINE WAVE AS CARRIER WAVE AND THEN IMAGE VALUES AS MODULATOR, SO DO FM SYNTHESIS

import cv2 as cv
import statistics
import wave
import struct
import math
import sys, getopt
from scipy.signal import savgol_filter

input_filename = None
output_filename = None
border_width = 10
border_color = 287
blur_size = 10
blur_iterations = 2

def printUsage():
    print('Usage for imageToSound.py:')
    print('Syntax: python imageToSound.py -i <path_to_sound> -o <output filename> --bw=<border_width> --bc=<border color (0-255)> --blursize=<blur_size> --bluriterations=<blur iterations>')
    print('Also Valid Syntax: python fixDB.py -i <inputFile> -o <outputFile>')

try:
    opts, args = getopt.getopt(sys.argv[1:], 'hi:o:', ['help', 'bw=', 'bc=', 'blursize=', 'bluriterations='])

except getopt.GetoptError as err:
    print(err)
    printUsage()
    sys.exit(2)

for o, a in opts:
    if o in ("-h", "--help"):
        printUsage()
        sys.exit()
    elif (o == "-i"):
        input_filename = a
    elif (o == '-o'):
        output_filename = a
    elif (o == '--bw'):
        border_width = int(a)
    elif (o == '--bc'):
        border_color = int(a)
    elif (o == '--blursize'):
        blur_size = int(a)
    elif (o == '--bluriterations'):
        blur_iterations = int(a)
    else:
        assert False, "unhandled option"

if (input_filename == None or output_filename == None):
    printUsage()
    sys.exit(2)

img = cv.imread(input_filename)

cv.imshow('original image [press any key to continue]', img)

cv.waitKey(0)
cv.destroyAllWindows()

cv.rectangle(img, (0, 0), ((len(img[0])), (len(img))), (border_color, border_color, border_color), border_width)

cv.imshow('added box for smoothing! [press any key to continue]', img)


cv.waitKey(0)
cv.destroyAllWindows()

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)


for i in range(0, blur_iterations):
    gray = cv.blur(gray, [blur_size, blur_size])


gray = cv.normalize(gray, gray, 0, 240, cv.NORM_MINMAX)


cv.imshow('greyscale image [press any key to continue]', gray)

cv.waitKey(0)
cv.destroyAllWindows()


brightnesses = []

for columnIndex in range(0, len(gray[0])):
    for rowIndex in range(0, len(gray)):
        brightnesses.append(gray[rowIndex][columnIndex])

brightnesses = savgol_filter(brightnesses, 60, 3)


maxBrightness = max(brightnesses)
minBrightness = min(brightnesses)

for i, item in enumerate(brightnesses):
    brightnesses[i] = (((brightnesses[i] - minBrightness) / (maxBrightness - minBrightness))) * (2 * 20000) - 20000

#do the audio file stuff
sampleRate = 44100.0 # hertz
duration = 1.0 # seconds
frequency = 440.0 # hertz
wav = wave.open(f'sounds/{output_filename}.wav','w')
wav.setnchannels(1) # mono
wav.setsampwidth(2)
wav.setframerate(sampleRate)


for i in brightnesses:
    sample = struct.pack('<h', int(i))
    wav.writeframesraw(sample)

wav.close()

