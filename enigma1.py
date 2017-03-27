
alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']


rotor1 = [4,12,19,22,18,8,11,17,20,24,16,13,10,5,4,9,2,0,25,1,15,6,23,14,7,21]
rotor2 = [7,16,25,6,15,9,19,12,14,1,11,13,2,8,5,3,24,0,22,21,4,20,18,17,10,23]
rotor3 = [20,16,13,19,11,18,25,5,12,17,4,7,3,15,23,10,8,1,21,24,6,9,2,22,14,0]
reflector = [4,9,12,25,0,11,24,23,21,1,22,5,2,17,16,20,14,13,19,18,15,8,10,7,6,3]

print len(rotor1), len(rotor2), len(rotor3), len(reflector)

def ringSetting(offset):
    ring = {}
    for i in range(26):
        ring[alphabet[i]] = (i + offset) % 26

    return ring

ring1 = ringSetting()

plainLetter = 'A'
inputPin = ring1[plainLetter]
outputPin = rotor1[inputPin]
cipherLetter = alphabet[outputPin]

print cipherLetter

outputPin = alphabet.index(cipherLetter)
inputPin = rotor1.index(outputPin)
for key, pin in ring1.items():
    if pin == inputPin:
        plainLetter = key

print plainLetter

