"""
Copyright 2021 by Andrew R. Hansen.
This simulator has been tested against the (very beautiful) simulator here:
https://piotte13.github.io/enigma-cipher/
using the genuine Enigma intercepts and their decrypts found here:
http://wiki.franklinheath.co.uk/index.php/Enigma/Sample_Messages
It can reliably decrypt messages encrypted with Enigma I and M3.  Both are three rotor machines.
It cannot decrypt messages encrypted with the four rotor machine used by the Kriegsmarine.
"""

class Rotor:
    def __init__(self, details, ringsetting = 0, indicated = 'A'):
        self.sequence = details[0]
        self.notch = details[1]
        self.ringsetting = ringsetting
        self.indicated = indicated

        if ringsetting > 0:
            self.sequence = self.set_ringsetting(self.sequence, ringsetting-1)

    def set_ringsetting(self, wiring, setting):
        """
        This was tough to crack.
        The function steps through the rotor from the A position to the Z position and notes the offset between
        the input pin and the output pin.  The result is 26 offsets.
        The function then rotates the offset list rightwards using slice notation so that the offsets now match
        the ringsetting.
        The function then creates a new, blank rotor and creates the output sequence from the rotated wiring.
        The result is an output sequence that can be used for the encryption function.
        :param wiring: The original, published output sequence.
        :param setting: The ringsetting. Note that a setting of 01 in the literature is 00 in this app.
        :return: A new sequence that reflects the rotated wiring inside the rotor.
        """
        offsets = []
        for in_pin in range(26):
            out_pin = ord(wiring[in_pin]) - 65
            offset = out_pin - in_pin
            offsets.append(offset)
        offsets = offsets[-setting:] + offsets[:-setting]
        new_rotor = ''
        for i in range(26):
            index = i + offsets[i]
            if index > 25:
                index = index - 26
            elif index < 0:
                index = index + 26
            new_rotor += chr(index + 65)
        return new_rotor

    def get_position(self):
        self.position = ord(self.indicated) - 65
        return self.position

    def get_indicated(self):
        return self.indicated

    def step(self):
        alpha_index = (ord(self.indicated) - 65)
        alpha_index = ((alpha_index + 1) % 26) + 65
        self.indicated = chr(alpha_index)

class Reflector:
    def __init__(self, sequence):
        self.sequence = sequence

class Plugboard:
    def __init__(self, plugboard):
        self.plugboard = plugboard
        self.test()

    def test(self):
        letters = []
        OK = True
        for plug in self.plugboard:
            if plug[0] in letters or plug[1] in letters:
                print('Error in plug: ' + plug + '. Letter already used.')
                OK = False
            else:
                letters.append(plug[0])
                letters.append(plug[1])
        if OK:
            print('Plugboard settings OK.')

    def plug_shuffle(self, char):
        for plug in self.plugboard:
            if char == plug[0]:
                char = plug[1]
            elif char == plug[1]:
                char = plug[0]
            else:
                char = char
        return char

class Machine:
    def __init__(self, reflector, slow, med, fast, plugboard):
        self.reflector = reflector
        self.slow = slow
        self.med = med
        self.fast = fast
        self.plugboard = plugboard

    def get_indicated(self):
        return (self.slow.get_indicated(), self.med.get_indicated(), self.fast.get_indicated())

    def step(self):
        """
        This function mimics the double stepping of the actual Enigma machine.
        The double step is most easily described as 'When a rotor turns over the rotor to its right also turns over'.
        This is the correct single stepping routine:
        A A U
        A A V
        A B W
        A B X
        In reality, the fast rotor has also double stepped but since it always steps you don't see it.
        Double stepping looks like this:
        A D U
        A D V
        A E W
        B F X
        B F Y
        In this example when the fast rotor shows 'V' it engages the pawl on the middle rotor and on the next step
        ('V' to 'W') on the slow rotor the middle rotor steps from 'D' to 'E'.  This now engages the pawl for the fast
        rotor and on the next step the fast rotor advances from 'A' to 'B' but the pawl that pushes the fast rotor
        also pushes the middle rotor and so the middle rotor also advances from 'E' to 'F'.
        The algorithm is if the fast rotor notch engages then advance the middle rotor and the fast rotor on the next
        step (actually a double step but you dont see it).  If the middle rotor notch engages then advance all three
        rotors (the slow rotor, double step the middle rotor, and normal step the fast rotor).

        :return: Nothing is returned.  The machine state is affected.
        """
        if self.med.get_indicated() in self.med.notch:
            self.slow.step()
            self.med.step()
            self.fast.step()
        elif self.fast.get_indicated() in self.fast.notch:
            self.med.step()
            self.fast.step()
        else:
            self.fast.step()

    def encode(self, letter):
        """
        With all three rotors moving against each other it was too difficult to track the relative offsets between the
        rotors.  Instead I imagined a fixed wiring skeleton that the rotors sit in.  Instead of rotating against each
        other they rotate against the (somewhat) imaginary skeleton.  The skeleton actually reflects the fixed parts
        of the encryption mechanism, being the entry wheel (ETW) and the reflector.  Neither of these rotates so the
        skeleton is an extension of these positions.
        This made it easy to use the rotor position to determine the wiring offset relative to the skeleton and adjust
        for each rotor in turn.
        :param letter:
        :return:
        """
        slow_seq = self.slow.sequence
        med_seq = self.med.sequence
        fast_seq = self.fast.sequence
        refl = self.reflector.sequence

        slow_position = self.slow.get_position()
        med_position = self.med.get_position()
        fast_position = self.fast.get_position()

        wiring_slow = {}
        wiring_med = {}
        wiring_fast = {}
        wiring_refl = {}

        for i in range(26):  # We know it's 26
            wiring_slow[i] = ord(slow_seq[i]) - 65
            wiring_med[i] = ord(med_seq[i]) - 65
            wiring_fast[i] = ord(fast_seq[i]) - 65
            wiring_refl[i] = ord(refl[i]) - 65

        # Encode through fast rotor
        ETW = ord(letter) - 65  # same as skeleton wire
        in_fast = (ETW + fast_position) % 26
        out_fast = wiring_fast[in_fast]
        skel = (out_fast - fast_position)
        if skel < 0:
            skel = 26 + skel

        # Encode through medium rotor
        in_med = (skel + med_position) % 26
        out_med = wiring_med[in_med]
        skel = (out_med - med_position)
        if skel < 0:
            skel = 26 + skel

        # Encode through slow rotor
        in_slow = (skel + slow_position) % 26
        out_slow = wiring_slow[in_slow]
        skel = (out_slow - slow_position)
        if skel < 0:
            skel = 26 + skel

        # Encode through reflector
        refl_out = wiring_refl[skel]
        skel = refl_out

        # Encode back through slow rotor
        in_slow = skel + slow_position
        if in_slow > 25:
            in_slow = in_slow - 26
        for k, v in wiring_slow.items():
            if v == in_slow:
                out_slow = k
        skel = out_slow - slow_position
        if skel < 0:
            skel = 26 + skel

        # Encode back through med rotor
        in_med = skel + med_position
        if in_med > 25:
            in_med = in_med - 26
        for k, v in wiring_med.items():
            if v == in_med:
                out_med = k
        skel = out_med - med_position
        if skel < 0:
            skel = 26 + skel

        # Encode back through fast rotor
        in_fast = skel + fast_position
        if in_fast > 25:
            in_fast = in_fast - 26
        for k, v in wiring_fast.items():
            if v == in_fast:
                out_fast = k
        skel = out_fast - fast_position
        if skel < 0:
            skel = 26 + skel

        # Encode back through ETW
        ETW = skel
        letter = chr(ETW + 65)

        return letter


