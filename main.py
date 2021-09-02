"""
Copyright 2021 by Andrew R. Hansen.
This simulator has been tested against the (very beautiful) simulator here:
https://piotte13.github.io/enigma-cipher/
using the genuine Enigma intercepts and their decrypts found here:
http://wiki.franklinheath.co.uk/index.php/Enigma/Sample_Messages
It can reliably decrypt messages encrypted with Enigma I and M3.  Both are three rotor machines.
It cannot decrypt messages encrypted with the four rotor machine used by the Kriegsmarine.
"""
from Enigma_classes import Rotor, Reflector, Plugboard, Machine

rotors = {
    'I': ['EKMFLGDQVZNTOWYHXUSPAIBRCJ', ['Q']],
    'II': ['AJDKSIRUXBLHWTMCQGZNPYFVOE', ['E']],
    'III': ['BDFHJLCPRTXVZNYEIWGAKMUSQO', ['V']],
    'IV': ['ESOVPZJAYQUIRHXLNFTGKDCMWB', ['J']],
    'V': ['VZBRGITYUPSDNHLXAWMJQOFECK', ['Z']],
    'VI': ['JPGVOUMFYQBENHZRDKASXLICTW', ['M', 'Z']],
    'VII': ['NZJHGRCXMYSWBOUFAIVLPEKQDT', ['M', 'Z']],
    'VIII': ['FKQHTLXOCBJSPDZRAMEWNIUYGV', ['M', 'Z']]
}
reflectors = {
    'A': 'EJMZALYXVBWFCRQUONTSPIKHGD',
    'B': 'YRUHQSLDPXNGOKMIEBFZCWVJAT',
    'C': 'FVPJIAOYEDRZXWGCTKUQSBNMHL',
    'Beta': 'LEYJVCNIXWPBQMDRTAKZGFUHOS',
    'Gamma': 'FSOKANUERHMBTIYCWLQPZXVGJD'
}


def process_inputs(rotor_selection, ring_setting, reflector, plug_pairs, message_key):
    rotor_selections = rotor_selection.split(',')
    ring_settings = ring_setting.split(',')
    plug_list = []
    plug_list_bits = plug_pairs.split(',')
    for plug in plug_list_bits:
        plug_list.append(plug)

    slow = Rotor(rotors[rotor_selections[0]], int(ring_settings[0]), message_key[0])
    med = Rotor(rotors[rotor_selections[1]], int(ring_settings[1]), message_key[1])
    fast = Rotor(rotors[rotor_selections[2]], int(ring_settings[2]), message_key[2])
    refl = Reflector(reflectors[reflector])
    plugs = Plugboard(plug_list)

    return refl, slow, med, fast, plugs

rotor_selection = input('Rotors: S,M,F: (I, II, III, IV, V, VI, VII, VIII): ')
ring_setting = input('Ring settings: S,M,F: (1 to 26): ')
reflector = input('Reflector: (A, B, C, Beta, Gamma): ')
plug_pairs = input('Plug pairs: (AB, CD, etc): ')
input_text = input('Text: ')
message_key = input('Message key: (ABC): ')

refl, slow, med, fast, plugs = process_inputs(rotor_selection, ring_setting, reflector, plug_pairs, message_key)

machine = Machine(refl, slow, med, fast, plugs)

decrypt = ''
for key in input_text:
    machine.step()
    letter = plugs.plug_shuffle(key)
    returned = machine.encode(letter)
    bulb = plugs.plug_shuffle(returned)
    decrypt += bulb
print(decrypt)