import random
from UnEnigma.Enigma import Enigma
from UniSinkov.UniSinkovTest import UniSinkovTest
import time

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


    def comparePlugs(self, plug1: str, plug2: str):
        return ((plug1 == plug2) or (plug1 == (plug2[1]+plug2[0])))


    def runTrials(self, enig: Enigma, f) -> float:
        
        results = 0
        numTrials = 0
        us = UniSinkovTest()
        for line in f:
            numTrials += 1

            information = line.strip().split()
            enigmaSettings = line[1]
            cipherText = line[2]
            rotorSettings = [int(enigmaSettings[0]), int(enigmaSettings[1:3]), int(enigmaSettings[3]), int(enigmaSettings[4:6]),
                    int(enigmaSettings[6]), int(enigmaSettings[7:9])]
            knownPlugSettings = [enigmaSettings[9:11], enigmaSettings[11:13], enigmaSettings[13:15], enigmaSettings[15:17],
                            enigmaSettings[17:]]
            enig.wipe()
            enig.setRotors(rotorSettings[0], rotorSettings[1], rotorSettings[2], rotorSettings[3], rotorSettings[4], rotorSettings[5])

            lastStr = ""
            proposedPlugs = []
            baseline = us.computeSinkov(enig.encryptString(cipherText))
            alpha = "abcdefghijklmnopqrstuvwxyz"
            for i in range(5):
                currMax = float('-inf')
                best = ""
                a = None
                b = None
                for x in range(len(alpha)):
                    for y in range(x+1, len(alpha+1)):
                        enig.resetSteckerboard()
                        for pair in promote_types:
                            enig.setSteckerboardPlug(pair[0], pair[1])
                        
                        enig.setSteckerboardPlug(alpha[x], alpha[y])

                        s = enig.encryptString(cipherText)
                        score = us.computeSinkov(s)
                        if score > currMax:
                            currMax = score
                            a = alpha.find(x)
                            b = alpha.find(y)
                            best = alpha[x] + alpha[y]
                
                proposedPlugs.append(best)
                alpha = alpha[:a] + alpha[a+1:b] + alpha[b+1:]
            for plug in proposedPlugs:
                for actualPlug in knownPlugSettings:
                    if self.comparePlugs(plug, actualPlug):
                        results += 1
                        break
        
        return results/numTrials



            


if __name__ == "__main__":
    e = Enigma()
    tc = testCases()

    ''' with open("UnEnigma/Tests/ourFuture.txt", "r") as file:
        for line in file:
            with open("UnEnigma/Tests/testPairs.txt", "a") as file2:
                t.generateSettingsFile(line.strip(), e, file2)
    '''
    res = 0
    t = None
    with open("Tests/testPairs.txt", "r") as file:
        t = time.time()
        res = tc.runTrials(e, file)
        print("time elapsed (s): ", time.time() - t)

    print(res)

