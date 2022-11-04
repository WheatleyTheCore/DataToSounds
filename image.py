import cv2 as cv
import statistics
import wave
import struct

img = cv.imread('assets/lonelySpiral.jpg')

cv.imshow('regular!', img)

cv.waitKey(0)
cv.destroyAllWindows()

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

ret, gray = cv.threshold(gray, 80, 255, cv.THRESH_BINARY)

gray = cv.blur(gray, [2, 2])

cv.imshow('grayscale!', gray)

cv.waitKey(0)
cv.destroyAllWindows()


averages = []

for columnIndex in range(0, len(gray[0])):
    for rowIndex in range(0, len(gray)):
        averages.append(gray[rowIndex][columnIndex])

# for i in range(0, len(gray)):
#     averages.append(statistics.mean(gray[i]))


maxBrightness = max(averages)
minBrightness = min(averages)

# for i, item in enumerate(averages):
#     averages[i] = (((averages[i] - minBrightness) / (maxBrightness - minBrightness))) * 32767

for i, item in enumerate(averages):
    averages[i] = (((averages[i] - minBrightness) / (maxBrightness - minBrightness))) * (2 * 32767) - 32767

# for i in averages:
#     print(i)

#print(f'min: {min(averages)}, max: {max(averages)}')

#do the audio file stuff
sampleRate = 44100.0 # hertz
duration = 1.0 # seconds
frequency = 440.0 # hertz
wav = wave.open('sounds/space.wav','w')
wav.setnchannels(1) # mono
wav.setsampwidth(2)
wav.setframerate(sampleRate)


for i in averages:
    sample = struct.pack('<h', int(i))
    wav.writeframesraw(sample)

wav.close()

