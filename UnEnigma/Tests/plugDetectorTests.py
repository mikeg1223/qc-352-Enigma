import random
from Enigma import Enigma

class testCases:

    def __init__(self):
        pass


    def generateSettingsFile(self, s: str, enig: Enigma, f) -> str:
        count = 0
        ret_String = ""
        while count < 10:
            alpha = "abcdefghijklmnopqrstuvwxyz"
            rotors = []
            rings = []
            plugs = []
            for _ in range (3):
                rotors.append(random.randint(1,8))

            while rotors[0] == rotors[1] or rotors[0] == rotors[2] or rotors[1] == rotors[2]:
                rotors = []
                for _ in range (3):
                    rotors.append(random.randint(1,8))
            for _ in range(3):
                rings.append(random.randint(0,25))
            enig.setRotors(rotors[0], rings[0], rotors[1], rings[1], rotors[2], rings[2])
            for _ in range(5):
                first = random.randint(0, len(alpha)-1)
                c1 = alpha[first]
                alpha = alpha[:first] + alpha[first+1:]
                second = random.randint(0, len(alpha)-1)
                c2 = alpha[second]
                alpha = alpha[:second] + alpha[second+1:]
                if ord(c1) < ord(c2):
                    c1, c2 = c2, c1
                plugs.append((c1, c2))
                enig.setSteckerboardPlug(c1,c2)
            
            plugs.sort(key = lambda x: (x[0], x[1]))
            rotorsString = ""
            for _ in range(3):
                rotorsString += str(rotors[_])+str(rings[_]).zfill(2)
            plugString = ""
            for _ in plugs:
                plugString += _[0] + _[1]

            ret_String += s + " " + rotorsString + plugString + " " + enig.encryptString(s) + "\n"
            count += 1
        f.write(ret_String)
            





ls = []
count = 0
e = Enigma()
t = testCases()

with open("UnEnigma/Tests/ourFuture.txt", "r") as file:
    for line in file:
        with open("UnEnigma/Tests/testPairs", "a") as file2:
            t.generateSettingsFile(line.strip(), e, file2)
