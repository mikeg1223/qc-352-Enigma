
'''
This class represents an Enigma rotor, and handles operations for setting, 
augmenting, and creating the rotors.
'''
class Rotor:

    # some constants
    PERM = 1
    NOTCH = 2
    
    # basic string array for the alphabet
    baseAlpha = "abcdefghijklmnopqrstuvwxyz"

    # setting the rotor constants
    rotors = [{PERM:"ekmflgdqvzntowyhxuspaibrcj", NOTCH: [16]}, 
              {PERM:"ajdksiruxblhwtmcqgznpyfvoe", NOTCH: [4]},
              {PERM:"bdfhjlcprtxvznyeiwgakmusqo", NOTCH: [21]}, 
              {PERM:"esovpzjayquirhxlnftgkdcmwb", NOTCH: [9]},
              {PERM:"vzbrgityupsdnhlxawmjqofeck", NOTCH: [25]}, 
              {PERM:"jpgvoumfyqbenhzrdkasxlictw", NOTCH: [12, 25]},
              {PERM:"nzjhgrcxmyswboufaivlpekqdt", NOTCH: [12, 25]}, 
              {PERM:"nzjhgrcxmyswboufaivlpekqdt", NOTCH: [12, 25]},
              {PERM:"fkqhtlxocbjspdzramewniuygv", NOTCH: [12, 25]}]


    '''
    This constructor creates a rotor object and requires the specified inputs
    Args:
        first           A boolean values representing wether or not the rotor is the 
                        fastest moving rotor.
        rotorNumber     An integer representing the actual rotor that is being 
                        represented. Indexed from 1 as an argument, but changes 
                        to 0 indexing internally.
        ringSetting     An integer representing the ring setting offset. Indexed 
                        from 0.
    Returns:
        None
    '''
    def __init__(self, first: bool, rotorNumber: int, ringSetting: int):

        # setting variables
        self.isFirst = first
        self.isSet = False
        self.ring = ringSetting
        self.permForward = {}
        self.permBackwards = {}
        self.notch = Rotor.rotors[rotorNumber-1][Rotor.NOTCH]
        self.rotorNumber = rotorNumber
        self.currentRotation = 0

        # incorrect input will not init a rotor
        if rotorNumber < 1 or rotorNumber > 8:
            print("incorrect rotor number for m3")
            return
        
        # initial permutation. This will never be used? Not sure if it's needed really 
        else:
            for _ in range(26):
                self.permForward[chr(_+97)] = Rotor.rotors[self.rotorNumber-1][Rotor.PERM][(_-self.ring+self.currentRotation)%26]
                self.permBackwards[Rotor.rotors[self.rotorNumber-1][Rotor.PERM][(_-self.ring+self.currentRotation)%26]] = chr(_+97)
            self.isSet = True
       

    '''
    This rotate function will change the permutation to account for the new rotor position.
    It will also handle notch data.
    Args:
        None
    Returns:
        ret_value   A boolean value representing whether the notch should kick over the next rotor. 
    '''
    def rotate(self) -> bool:
        self.currentRotation += 1
        self.currentRotation %= 26
        ret_value = False

        # return true if a notch is reached. Signal to turn the next rotor.
        if (self.currentRotation - 1) % 26 == self.notch[0]:
            ret_value = True
        if len(self.notch) == 2 and (self.currentRotation - 1) % 26 == self.notch[1]:
            ret_value = True

        # Set the new permutation. It is the default rotor perm + rotation - ring setting. Also setting inverse perm
        for _ in range(26):
            self.permForward[chr(_+97)] = Rotor.rotors[self.rotorNumber-1][Rotor.PERM][(_-self.ring+self.currentRotation)%26]
            self.permBackwards[Rotor.rotors[self.rotorNumber-1][Rotor.PERM][(_-self.ring+self.currentRotation)%26]] = chr(_+97)
            
        return ret_value


    '''
    This function will reset a rotor to the 'A' position and update the permutation.
    Args:
        None
    Returns:
        None
    '''
    def resetRotorPosition(self):
        self.currentRotation = 0
        for _ in range(26):
            self.permForward[chr(_+97)] = Rotor.rotors[self.rotorNumber-1][Rotor.PERM][(_-self.ring+self.currentRotation)%26]
            self.permBackwards[Rotor.rotors[self.rotorNumber-1][Rotor.PERM][(_-self.ring+self.currentRotation)%26]] = chr(_+97)


    '''
    This function will change the ring setting to a specified value mod 26. 
    The ring setting is indexed from 0. The permutation for the rotor is updated.
    Args:
        input   An integer representing the desired ring position.
    Returns:
        None
    '''
    def setRotorRing(self, input: int):
        if input >= 0:
            self.ring = input % 26
            for _ in range(26):
                self.permForward[chr(_+97)] = Rotor.rotors[self.rotorNumber-1][Rotor.PERM][(_-self.ring+self.currentRotation)%26]
                self.permBackwards[Rotor.rotors[self.rotorNumber-1][Rotor.PERM][(_-self.ring+self.currentRotation)%26]] = chr(_+97)


    '''
    This is the function used to encrypt a letter through this rotor's wiring 
    and position.
    Args:
        input       A character which we wish to encrypt
        isForward   A boolean representing whether this is the forward or 
                    backwards permutation for this rotor
        rot         A boolean representing whether this rotor should rotate 
                    during this encryption. 
    Returns:
        A tuple (cipherText, TurnNextRotor) which is a character and boolean respectively.  
    '''
    def output(self, input: chr, isForward: bool, rot: bool) -> tuple:
        if self.isSet:
            bvalue = False
            if rot:
                bvalue = self.rotate()
            if isForward:
                return (self.permForward[chr((((ord(input)-97))%26)+97)], bvalue)
            return (self.permBackwards[chr((((ord(input)-97))%26)+97)], bvalue)


'''
This class represents an M3 enigma as presented in 
https://people.physik.hu-berlin.de/~palloks/js/enigma/enigma-u_v20_en.html
'''
class Enigma:
    

    '''
    This constructor creates an "empty" enigma object without specified rotors and 
    an empty steckerboard. The reflector we use is static so it is created here.

    Args:
        None
    Returns:
        None
    '''
    def __init__(self):

        # create constants and variables
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


    '''
    This function sets the rotors and their respective ring settings. 
    The ring setting is to the right of each rotor. This changes the flag 
    indicating whether the rotors are set. 
    Args:
        fast        An integer representing the number of the fastest moving rotor
        fastRing    An integer representing the ring setting for the fastest moving rotor
        mid         An integer representing the middle rotor
        midRing     An integer representing the ring setting for the middle rotor
        slow        An integer representing the slowest moving rotor
        slowRing    An integer representing the ring setting for the slow rotor
    Returns:
        None
    '''
    def setRotors(self, fast: int, fastRing: int, mid: int, midRing: int, slow: int, slowRing: int):
        self.rotors["fast"] = Rotor(True, fast, fastRing)
        self.rotors["middle"] = Rotor(False, mid, midRing)
        self.rotors["slow"] = Rotor(False, slow, slowRing)
        self.isSet = True


    '''
    This function sets a steckerBoard plug. 
    Args:
        letter1     A character to be one end of the plug
        letter2     A character to be the other end of the plug
    Returns:
        None
    '''
    def setSteckerboardPlug(self, letter1, letter2):
        self.steckerBoard[letter1] = letter2
        self.steckerBoard[letter2] = letter1

    
    '''
    This function encrypts a single letter by sending it through all the steckerboard, 
    the rotors forward, the reflector, the rotors backwards, and the steckerboard again. 
    It is modeled after the code for the enigma linked in the class definition.
    Args:
        input      A character to be encrypted
    Returns 
        ret_val    A fully encrypted character
    '''
    def encryptLetter(self, input) -> chr:
        if self.isSet:

            # This process is modeled off of the "kodieren" function inside of the javascript code for the enigma applet
            inp = self.steckerBoard[input]
            working_val = self.rotors["fast"].output(inp, True, True)
            working_val = self.rotors["middle"].output((chr((ord(working_val[0])-97-self.rotors["fast"].currentRotation + self.rotors["fast"].ring)%26 + 97)), True, working_val[1])
            working_val = self.rotors["slow"].output((chr((ord(working_val[0])-97-self.rotors["middle"].currentRotation + self.rotors["middle"].ring)%26 + 97)), True, working_val[1])
            working_val = self.reflector[(ord(working_val[0])-97-self.rotors["slow"].currentRotation + self.rotors["slow"].ring)%26]
            working_val = self.rotors["slow"].output((chr((ord(working_val[0]) - 97 + self.rotors["slow"].currentRotation - self.rotors["slow"].ring)%26 + 97)), False, False)
            working_val = self.rotors["middle"].output((chr((ord(working_val[0]) - 97 + self.rotors["middle"].currentRotation - self.rotors["middle"].ring)%26 + 97)), False, False)
            working_val = self.rotors["fast"].output((chr((ord(working_val[0]) -97 + self.rotors["fast"].currentRotation - self.rotors["fast"].ring)%26 + 97)), False, False)

            ret_val = self.steckerBoard[working_val[0]]
            return ret_val

    
    '''
    This function will set all rotor positions back to 'A'
    Args:
        None
    Returns:
        None
    '''
    def resetRotorPositions(self):
        self.rotors["fast"].resetRotorPosition()
        self.rotors["middle"].resetRotorPosition()
        self.rotors["slow"].resetRotorPosition()


    '''
    This function will "remove" the rotors, "empty" the steckerboard, and reset the rotor flag
    Args:
        None
    Returns:
        None
    '''
    def wipe(self):
        self.rotors = {"fast":None, "middle":None, "slow":None }
        self.steckerBoard = {}
        self.isSet = False
        # init the steckerboard to chars that map to themself
        for _ in range(26):
            self.steckerBoard[chr(_+97)] = chr(_+97)


    '''
    This function encrypts a one letter a time and returns the result after 
    resettign the rotor positions.
    Args:
        input       A string to be encrypted
    Returns:
        ret_val     An encrypted string
    '''
    def encryptString(self, input) -> str:
        ret_val = ""
        for _ in input:
            ret_val += self.encryptLetter(_)
        
        self.resetRotorPositions()
        return ret_val



# program runs from below 
if __name__ == "__main__":
    e = Enigma()
    e.setRotors(1, 1, 2, 0, 3, 0)
    s = "abcd"
    out = e.encryptString(s)
    print(out)
    s = out
    out = e.encryptString(s)
    print(out)