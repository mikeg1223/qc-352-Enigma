class Rotor:
    PERM = 1
    NOTCH = 2
    baseAlpha = "abcdefghijklmnopqrstuvwxyz"
    rotor1Setting = {PERM:"ekmflgdqvzntowyhxuspaibrcj", NOTCH: (16)}
    rotor2Setting = {PERM:"ajdksiruxblhwtmcqgznpyfvoe", NOTCH: (4)}
    rotor3Setting = {PERM:"bdfhjlcprtxvznyeiwgakmusqo", NOTCH: (21)}
    rotor4Setting = {PERM:"esovpzjayquirhxlnftgkdcmwb", NOTCH: (9)}
    rotor5Setting = {PERM:"vzbrgityupsdnhlxawmjqofeck", NOTCH:(25)}
    rotor6Setting = {PERM:"jpgvoumfyqbenhzrdkasxlictw", NOTCH:(12, 25)}
    rotor7Setting = {PERM:"nzjhgrcxmyswboufaivlpekqdt", NOTCH:(12, 25)}
    rotor8Setting = {PERM:"fkqhtlxocbjspdzramewniuygv", NOTCH:(12, 25)}
    def Rotor(self, first: bool, rotorNumber: int, ringSetting):
        self.isFirst = first
        self.isSet = False
        self.ring = ringSetting
        self.permForward = {}
        self.permBackwards = {}
        self.notch = 0
        self.rotorNumber = rotorNumber
        self.currentRotation = 0
        if rotorNumber < 1 or rotorNumber > 8:
            print("incorrect rotor number for m3")
            return
        elif rotorNumber == 1:
            for _ in range(26):
                self.permForward[chr(_+97)] = Rotor.rotor1Setting[Rotor.PERM][(_+self.ring)%26]
                self.permBackwards[Rotor.rotor1Setting[Rotor.PERM][(_+self.ring)%26]] = chr(_+97)
                self.notch = Rotor.rotor1Setting[Rotor.NOTCH]
                
        elif rotorNumber == 2:
            for _ in range(26):
                self.permForward[chr(_+97)] = Rotor.rotor2Setting[Rotor.PERM][(_+self.ring)%26]
                self.permBackwards[Rotor.rotor2Setting[Rotor.PERM][(_+self.ring)%26]] = chr(_+97)
                self.notch = Rotor.rotor2Setting[Rotor.NOTCH]

        elif rotorNumber == 3:
            for _ in range(26):
                self.permForward[chr(_+97)] = Rotor.rotor3Setting[Rotor.PERM][(_+self.ring)%26]
                self.permBackwards[Rotor.rotor3Setting[Rotor.PERM][(_+self.ring)%26]] = chr(_+97)
                self.notch = Rotor.rotor3Setting[Rotor.NOTCH]

        elif rotorNumber == 4:
            for _ in range(26):
                self.permForward[chr(_+97)] = Rotor.rotor4Setting[Rotor.PERM][(_+self.ring)%26]
                self.permBackwards[Rotor.rotor4Setting[Rotor.PERM][(_+self.ring)%26]] = chr(_+97)
                self.notch = Rotor.rotor4Setting[Rotor.NOTCH]

        elif rotorNumber == 5:
            for _ in range(26):
                self.permForward[chr(_+97)] = Rotor.rotor5Setting[Rotor.PERM][(_+self.ring)%26]
                self.permBackwards[Rotor.rotor5Setting[Rotor.PERM][(_+self.ring)%26]] = chr(_+97)
                self.notch = Rotor.rotor5Setting[Rotor.NOTCH]

        elif rotorNumber == 6:
            for _ in range(26):
                self.permForward[chr(_+97)] = Rotor.rotor6Setting[Rotor.PERM][(_+self.ring)%26]
                self.permBackwards[Rotor.rotor6Setting[Rotor.PERM][(_+self.ring)%26]] = chr(_+97)
                self.notch = Rotor.rotor6Setting[Rotor.NOTCH]

        elif rotorNumber == 7:
            for _ in range(26):
                self.permForward[chr(_+97)] = Rotor.rotor7Setting[Rotor.PERM][(_+self.ring)%26]
                self.permBackwards[Rotor.rotor7Setting[Rotor.PERM][(_+self.ring)%26]] = chr(_+97)
                self.notch = Rotor.rotor7Setting[Rotor.NOTCH]

        elif rotorNumber == 8:
            for _ in range(26):
                self.permForward[chr(_+97)] = Rotor.rotor8Setting[Rotor.PERM][(_+self.ring)%26]
                self.permBackwards[Rotor.rotor8Setting[Rotor.PERM][(_+self.ring)%26]] = chr(_+97)
                self.notch = Rotor.rotor8Setting[Rotor.NOTCH]


    def rotate(self) -> bool:
        self.currentRotation += 1
        self.currentRotation %= 26
        ret_value = False
        if (self.currentRotation - 1) % 26 == self.notch[1]:
            ret_value = True
        if len(self.notch) == 2 and (self.currentRotation - 1) % 26 == self.notch[2]:
            ret_value = True
        
        if self.rotorNumber == 1:
            for _ in range(26):
                self.permForward[chr(_+97)] = Rotor.rotor1Setting[Rotor.PERM][(_+self.ring+self.currentRotation)%26]
                self.permBackwards[Rotor.rotor1Setting[Rotor.PERM][(_+self.ring+self.currentRotation)%26]] = chr(_+97)
                self.notch = Rotor.rotor1Setting[Rotor.NOTCH]

        if self.rotorNumber == 2:
            for _ in range(26):
                self.permForward[chr(_+97)] = Rotor.rotor2Setting[Rotor.PERM][(_+self.ring+self.currentRotation)%26]
                self.permBackwards[Rotor.rotor2Setting[Rotor.PERM][(_+self.ring+self.currentRotation)%26]] = chr(_+97)
                self.notch = Rotor.rotor2Setting[Rotor.NOTCH]
        
        if self.rotorNumber == 3:
            for _ in range(26):
                self.permForward[chr(_+97)] = Rotor.rotor3Setting[Rotor.PERM][(_+self.ring+self.currentRotation)%26]
                self.permBackwards[Rotor.rotor3Setting[Rotor.PERM][(_+self.ring+self.currentRotation)%26]] = chr(_+97)
                self.notch = Rotor.rotor3Setting[Rotor.NOTCH]

        if self.rotorNumber == 4:
            for _ in range(26):
                self.permForward[chr(_+97)] = Rotor.rotor4Setting[Rotor.PERM][(_+self.ring+self.currentRotation)%26]
                self.permBackwards[Rotor.rotor4Setting[Rotor.PERM][(_+self.ring+self.currentRotation)%26]] = chr(_+97)
                self.notch = Rotor.rotor4Setting[Rotor.NOTCH]
        
        if self.rotorNumber == 5:
            for _ in range(26):
                self.permForward[chr(_+97)] = Rotor.rotor5Setting[Rotor.PERM][(_+self.ring+self.currentRotation)%26]
                self.permBackwards[Rotor.rotor5Setting[Rotor.PERM][(_+self.ring+self.currentRotation)%26]] = chr(_+97)
                self.notch = Rotor.rotor5Setting[Rotor.NOTCH]

        if self.rotorNumber == 6:
            for _ in range(26):
                self.permForward[chr(_+97)] = Rotor.rotor6Setting[Rotor.PERM][(_+self.ring+self.currentRotation)%26]
                self.permBackwards[Rotor.rotor6Setting[Rotor.PERM][(_+self.ring+self.currentRotation)%26]] = chr(_+97)
                self.notch = Rotor.rotor6Setting[Rotor.NOTCH]

        if self.rotorNumber == 7:
            for _ in range(26):
                self.permForward[chr(_+97)] = Rotor.rotor7Setting[Rotor.PERM][(_+self.ring+self.currentRotation)%26]
                self.permBackwards[Rotor.rotor7Setting[Rotor.PERM][(_+self.ring+self.currentRotation)%26]] = chr(_+97)
                self.notch = Rotor.rotor7Setting[Rotor.NOTCH]

        if self.rotorNumber == 8:
            for _ in range(26):
                self.permForward[chr(_+97)] = Rotor.rotor8Setting[Rotor.PERM][(_+self.ring+self.currentRotation)%26]
                self.permBackwards[Rotor.rotor8Setting[Rotor.PERM][(_+self.ring+self.currentRotation)%26]] = chr(_+97)
                self.notch = Rotor.rotor8Setting[Rotor.NOTCH]        


    def output(self, input: chr, isForward: bool, rot: bool) -> tuple:
        if rot:
            bvalue = self.rotate()
        if isForward:
            return (self.permForward[chr((((ord(input)-97)+ self.ring)%26)+97)], bvalue)
        return (self.permBackwards[chr((((ord(input)-97)+ self.ring)%26)+97)], bvalue)



class Enigma:
    
    def Enigma(self):
        self.baseAlpha = "abcdefghijklmnopqrstuvwxyz"
        self.reflector = {}
        self.isSet = False
        reflector = "yruhqsldpxngokmiebfzcwvjat"
        for _ in range(26):
            self.reflector[_] = reflector[_]
        self.rotors = {"first":None, "second":None, "third":None }

