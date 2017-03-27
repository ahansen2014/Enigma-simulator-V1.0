
keys = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']


rotor1 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,0]

def ringSetting():
    offset = 2
    ring1 = {}
    for i in range(26):
        ring1[keys[i]] = (i + offset) % 26

    return ring1

ring1 = ringSetting()

plainLetter = 'A'
inputPin = ring1[plainLetter]
outputPin = rotor1[inputPin]
cipherLetter = keys[outputPin]

print cipherLetter

outputPin = keys.index(cipherLetter)
inputPin = rotor1.index(outputPin)
for key, pin in ring1.items():
    if pin == inputPin:
        plainLetter = key

print plainLetter

