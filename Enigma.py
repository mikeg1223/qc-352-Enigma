class Rotor:
    PERM = 1
    NOTCH = 2
    
    baseAlpha = "abcdefghijklmnopqrstuvwxyz"

    rotors = [{PERM:"ekmflgdqvzntowyhxuspaibrcj", NOTCH: [16]}, 
              {PERM:"ajdksiruxblhwtmcqgznpyfvoe", NOTCH: [4]},
              {PERM:"bdfhjlcprtxvznyeiwgakmusqo", NOTCH: [21]}, 
              {PERM:"esovpzjayquirhxlnftgkdcmwb", NOTCH: [9]},
              {PERM:"vzbrgityupsdnhlxawmjqofeck", NOTCH: [25]}, 
              {PERM:"jpgvoumfyqbenhzrdkasxlictw", NOTCH: [12, 25]},
              {PERM:"nzjhgrcxmyswboufaivlpekqdt", NOTCH: [12, 25]}, 
              {PERM:"nzjhgrcxmyswboufaivlpekqdt", NOTCH: [12, 25]},
              {PERM:"fkqhtlxocbjspdzramewniuygv", NOTCH: [12, 25]}]

    def __init__(self, first: bool, rotorNumber: int, ringSetting: int):
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
        else:
            for _ in range(26):
                self.permForward[chr(_+97)] = Rotor.rotors[rotorNumber-1][Rotor.PERM][(_+self.ring)%26]
                self.permBackwards[Rotor.rotors[rotorNumber-1][Rotor.PERM][(_+self.ring)%26]] = chr(_+97)
                self.notch = Rotor.rotors[rotorNumber-1][Rotor.NOTCH]
            self.isSet = True
       

    def rotate(self) -> bool:
        self.currentRotation += 1
        self.currentRotation %= 26
        ret_value = False
        if (self.currentRotation - 1) % 26 == self.notch[0]:
            ret_value = True
        if len(self.notch) == 2 and (self.currentRotation - 1) % 26 == self.notch[1]:
            ret_value = True

        for _ in range(26):
                self.permForward[chr(_+97)] = Rotor.rotors[self.rotorNumber-1][Rotor.PERM][(_+self.ring+self.currentRotation)%26]
                self.permBackwards[Rotor.rotors[self.rotorNumber-1][Rotor.PERM][(_+self.ring)%26]] = chr(_+97)
                self.notch = Rotor.rotors[self.rotorNumber-1][Rotor.NOTCH] 

        return ret_value


    def output(self, input: chr, isForward: bool, rot: bool) -> tuple:
        bvalue = False
        if rot:
            bvalue = self.rotate()
        if isForward:
            #return (self.rotors[self.rotorNumber - 1][Rotor.PERM][(self.currentRotation + self.ring+ord(input)-97) %26])
            return (self.permForward[chr((((ord(input)-97)+ self.ring)%26)+97)], bvalue)
        return (self.permBackwards[chr((((ord(input)-97)+ self.ring)%26)+97)], bvalue)



class Enigma:
    
    def __init__(self):
        self.baseAlpha = "abcdefghijklmnopqrstuvwxyz"
        self.reflector = {}
        self.isSet = False
        refl = "yruhqsldpxngokmiebfzcwvjat"
        for _ in range(26):
            self.reflector[_] = refl[_]
        self.rotors = {"fast":None, "middle":None, "slow":None }
        self.steckerBoard = {}
        # init the steckerboard to chars that map to themself
        for _ in range(26):
            self.steckerBoard[chr(_+97)] = chr(_+97)

    def setRotors(self, fast: int, fastRing: int, mid: int, midRing: int, slow: int, slowRing: int):
        self.rotors["fast"] = Rotor(True, fast, fastRing)
        self.rotors["middle"] = Rotor(False, mid, midRing)
        self.rotors["slow"] = Rotor(False, slow, slowRing)

    def setSteckerboardPlug(self, letter1, letter2):
        self.steckerBoard[letter1] = letter2
        self.steckerBoard[letter2] = letter1

    def encryptLetter(self, input):
        inp = self.steckerBoard[input]
        working_val = self.rotors["fast"].output(inp, True, True)
        working_val = self.rotors["middle"].output(working_val[0], True, working_val[1])
        working_val = self.rotors["slow"].output(working_val[0], True, working_val[1])
        working_val = self.reflector[ord(working_val[0])-97]
        working_val = self.rotors["slow"].output(working_val, False, False)
        working_val = self.rotors["middle"].output(working_val[0], False, False)
        working_val = self.rotors["fast"].output(working_val[0], False, False)
        ret_val = self.steckerBoard[working_val[0]]
        return ret_val

    def encryptString(self, input) -> str:
        ret_val = ""
        for _ in input:
            ret_val += self.encryptLetter(_)
        return ret_val



e = Enigma()
e.setRotors(1, 0, 2, 0, 3, 0)
s = "abcd"
out = e.encryptString(s)
print(out)