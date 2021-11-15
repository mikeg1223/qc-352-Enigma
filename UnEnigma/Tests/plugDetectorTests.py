import random
from Enigma import Enigma
from LanguageRecognition import LanguageRecognition
import time

class testCases:

    def __init__(self):
        self.langRec = LanguageRecognition()


    def generateSettingsFile(self, s: str, enig: Enigma, f) -> str:
        count = 0
        ret_String = ""
        while count < 10:
            enig.wipe()
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


    def testOriginalHillClimbMethod(self, enig: Enigma, f) -> float:
        
        results = 0
        numTrials = 0
        us = UniSinkovTest()
        for line in f:
            numTrials += 1

            information = line.strip().split()
            enigmaSettings = information[1]
            cipherText = information[2]
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
                for x in range(len(alpha)-1):
                    for y in range(x+1, len(alpha)):
                        enig.resetSteckerboard()
                        for pair in proposedPlugs:
                            enig.setSteckerboardPlug(pair[0], pair[1])

                        
                        enig.setSteckerboardPlug(alpha[x], alpha[y])

                        s = enig.encryptString(cipherText)
                        score = us.computeSinkov(s)
                        if score > currMax:
                            currMax = score
                            a = x
                            b = y
                            best = alpha[x] + alpha[y]
                
                proposedPlugs.append(best)
                alpha = alpha[:a] + alpha[a+1:b] + alpha[b+1:]
            for plug in proposedPlugs:
                for actualPlug in knownPlugSettings:
                    if self.comparePlugs(plug, actualPlug):
                        results += 1
                        break
        
        return results/numTrials


    # see the improvement at each step of IOC and Sinkov for the 'grams
    def testScoreImprovementsThroughTrials(self, enig: Enigma, f, lr: LanguageRecognition):
        count = 0
        steps = []
        totals = []

        functions = [lr.indexOfCoincidenceUnigram, lr.indexOfCoincidenceBigram, lr.indexOfCoincidenceTrigram,
                     lr.sinkovStatisticUnigram, lr.sinkovStatisticBigram, lr.sinkovStatisticTrigram]
        
        # 0 - ciphertext, 1 - unplugged dec, 2 - one plug dec, etc
        # order of 0's: Unigram IOC, Bigram IOC, Trigram IOC, Unigram Sinkov, Bigram Sinkov, Trigram Sinkov
        for _ in range(7):
            steps.append([0,0,0,0,0,0])

        for _ in range(7):
            totals.append([0,0,0,0,0,0])
        
        # +1 if the scores improve for unplugged and then plug 1 through 5. 
        # same order as steps for the tests: UI, BI, TI, US, BS, TS
        wasImproved = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]

        for line in f:
            count += 1
            enig.wipe()
            line = line.strip()
            information = line.split()
            enigmaSettings = information[1]
            cipherText = information[2]
            knownRotors = [int(enigmaSettings[0]), int(enigmaSettings[3]), int(enigmaSettings[6])]
            knownRings = [int(enigmaSettings[1:3]), int(enigmaSettings[4:6]), int(enigmaSettings[7:9])]
            knownPlugSettings = [enigmaSettings[9:11], enigmaSettings[11:13], enigmaSettings[13:15], enigmaSettings[15:17],
                                    enigmaSettings[17:]]
            enig.setRotors(knownRotors[0], knownRings[0], knownRotors[1], knownRings[1], knownRotors[2], knownRings[2])

            for _ in range(6):
                steps[0][_] = functions[_](cipherText)
                totals[0][_] += steps[0][_]

            # unplugged
            for _ in range(6):
                enig.resetRotorPositions()
                steps[1][_] = functions[_](enig.encryptString(cipherText))
                totals[1][_] += steps[1][_]
                if steps[1][_] - steps[0][_] > 0:
                    wasImproved[0][_] += 1
            
            # 1 plug:
            for x in range(5):
                enig.resetRotorPositions()
                enig.resetSteckerboard()
                enig.setSteckerboardPlug(*knownPlugSettings[x])
                for y in range(6):
                    steps[2][y] = functions[y](enig.encryptString(cipherText))
                    totals[2][y] += steps[2][y]
                    if steps[2][y] - steps[1][y] > 0:
                        wasImproved[1][y] += 1
            

            # 2 plugs:
            for x in range(4):
                for y in range(x+1,5):
                    enig.resetRotorPositions()
                    enig.resetSteckerboard()
                    enig.setSteckerboardPlug(*knownPlugSettings[x])
                    enig.setSteckerboardPlug(*knownPlugSettings[y])
                    for z in range(6):
                        steps[3][z] = functions[z](enig.encryptString(cipherText))
                        totals[3][z] += steps[3][z]
                        if steps[3][z] - steps[2][z] > 0:
                            wasImproved[2][z] += 1
            
            
            # 3 plugs:
            for a in range(3):
                for b in range(a+1, 4):
                    for c in range(b+1, 5):
                        enig.resetRotorPositions()
                        enig.resetSteckerboard()
                        enig.setSteckerboardPlug(*knownPlugSettings[a])
                        enig.setSteckerboardPlug(*knownPlugSettings[b])
                        enig.setSteckerboardPlug(*knownPlugSettings[c])
                        for y in range(6):
                            steps[4][y] = functions[y](enig.encryptString(cipherText))
                            totals[4][y] += steps[4][y]
                            if steps[4][y] - steps[3][y] > 0:
                                wasImproved[3][y] += 1
            

            # 4 plugs:
            for a in range(2):
                for b in range(a+1, 3):
                    for c in range(b+1, 4):
                        for d in range(c+1, 5):
                            enig.resetRotorPositions()
                            enig.resetSteckerboard()
                            enig.setSteckerboardPlug(*knownPlugSettings[a])
                            enig.setSteckerboardPlug(*knownPlugSettings[b])
                            enig.setSteckerboardPlug(*knownPlugSettings[c])
                            enig.setSteckerboardPlug(*knownPlugSettings[d])
                            for y in range(6):
                                steps[5][y] = functions[y](enig.encryptString(cipherText))
                                totals[5][y] += steps[5][y]
                                if steps[5][y] - steps[4][y] > 0:
                                    wasImproved[4][y] += 1
            

            # all plugs:
            enig.resetRotorPositions()
            enig.resetSteckerboard()
            for _ in knownPlugSettings:
                enig.setSteckerboardPlug(*_)
            for y in range(6):
                steps[6][y] = functions[y](enig.encryptString(cipherText))
                totals[6][y] += steps[6][y]
                if steps[6][y] - steps[5][y] > 0:
                    wasImproved[5][y] += 1

        plugName = ["cipherText", "none", "one", "two", "three", "four", "five"]
        testName = ["Unigram IOC", "Bigram IOC", "Trigram IOC", "Unigram Sinkov", "Bigram Sinkov", "Trigram Sinkov"]

        # normalizing the results
        for x in range(len(wasImproved)):
            for y in range(len(wasImproved[x])):
                wasImproved[x][y] /= count
        
        for x in range(len(wasImproved[1])):
            wasImproved[1][x] /= 5
        
        for x in range(len(wasImproved[2])):
            wasImproved[2][x] /= 10
        
        for x in range(len(wasImproved[3])):
            wasImproved[3][x] /= 10
        
        for x in range(len(wasImproved[4])):
            wasImproved[4][x] /= 5
        
        for x in range(len(totals)):
            for y in range(len(totals[x])):
                totals[x][y] /= count

        for x in range(len(totals[2])):
            totals[2][x] /= 5

        for x in range(len(totals[3])):
            totals[3][x] /= 10
        
        for x in range(len(totals[4])):
            totals[4][x] /= 10
        
        for x in range(len(totals[5])):
            totals[5][x] /= 5

        for x in range(len(totals)):
            print(plugName[x], " plugs", "Test Results           P(better score)" , "\n ___________________________________________", )
            for y in range(len(totals[x])):
                if x == 0:
                    print(testName[y], " ", totals[x][y])
                else:
                    print(testName[y], " ", totals[x][y], " ", wasImproved[x-1][y])
            print("\n")


    def testScoreVarienceThroughTrials(self, enig: Enigma, f, lr: LanguageRecognition):
        count = 0
        totals = []

        functions = [lr.indexOfCoincidenceUnigram, lr.indexOfCoincidenceBigram, lr.indexOfCoincidenceTrigram,
                     lr.sinkovStatisticUnigram, lr.sinkovStatisticBigram, lr.sinkovStatisticTrigram]
        
        # 0 - ciphertext, 1 - unplugged dec, 2 - one plug dec, etc
        # order of 0's: Unigram IOC, Bigram IOC, Trigram IOC, Unigram Sinkov, Bigram Sinkov, Trigram Sinkov
        for _ in range(7):
            totals.append([0,0,0,0,0,0])

        means = [[0.03851383766038299, 0.0014744485351965888, 5.671894873885871e-05,-255.44619883833647,-503.7947181843265, -541.2713446819237],
                [0.048486198302156114, 0.002835849617626333, 0.0002348217681214902, -228.80141111761088, -458.77495975681035, -546.9276782511042],
                [0.051320603203003766,0.003439037740998043, 0.0003750988527416976, -222.2195651123471, -444.27664667663146, -544.2822260786331],
                [0.054510873648711454, 0.004229413288313244, 0.0006023698444590284, -214.75125604528617, -426.22262111853996, -538.3314738609599],
                [0.058057009639345535, 0.0052480056893026575, 0.0009606266399656008, -206.396483916423, -404.00562572285975, -527.2340122816859],
                [0.06195901117490209, 0.006540707304762179, 0.0015081216890610225, -197.15524872575634, -376.9450412932546, -508.4975632188219],
                [0.06621687825533423, 0.008158273426569784, 0.002322136756688445, -187.02755047329327, -344.2868867967599, -478.8912464243628]]

        for line in f:
            count += 1
            enig.wipe()
            line = line.strip()
            information = line.split()
            enigmaSettings = information[1]
            cipherText = information[2]
            knownRotors = [int(enigmaSettings[0]), int(enigmaSettings[3]), int(enigmaSettings[6])]
            knownRings = [int(enigmaSettings[1:3]), int(enigmaSettings[4:6]), int(enigmaSettings[7:9])]
            knownPlugSettings = [enigmaSettings[9:11], enigmaSettings[11:13], enigmaSettings[13:15], enigmaSettings[15:17],
                                    enigmaSettings[17:]]
            enig.setRotors(knownRotors[0], knownRings[0], knownRotors[1], knownRings[1], knownRotors[2], knownRings[2])

            for _ in range(6):
                totals[0][_] += (functions[_](cipherText)-means[0][_])**2

            # unplugged
            for _ in range(6):
                enig.resetRotorPositions()
                totals[1][_] += (functions[_](enig.encryptString(cipherText)) - means[1][_])**2
            
            # 1 plug:
            for x in range(5):
                enig.resetRotorPositions()
                enig.resetSteckerboard()
                enig.setSteckerboardPlug(*knownPlugSettings[x])
                for y in range(6):
                    totals[2][y] += (functions[y](enig.encryptString(cipherText))-means[2][y])**2
            

            # 2 plugs:
            for x in range(4):
                for y in range(x+1,5):
                    enig.resetRotorPositions()
                    enig.resetSteckerboard()
                    enig.setSteckerboardPlug(*knownPlugSettings[x])
                    enig.setSteckerboardPlug(*knownPlugSettings[y])
                    for z in range(6):
                        totals[3][z] += (functions[z](enig.encryptString(cipherText)) - means[3][z])**2
            
            
            # 3 plugs:
            for a in range(3):
                for b in range(a+1, 4):
                    for c in range(b+1, 5):
                        enig.resetRotorPositions()
                        enig.resetSteckerboard()
                        enig.setSteckerboardPlug(*knownPlugSettings[a])
                        enig.setSteckerboardPlug(*knownPlugSettings[b])
                        enig.setSteckerboardPlug(*knownPlugSettings[c])
                        for y in range(6):
                            totals[4][y] += (functions[y](enig.encryptString(cipherText))-means[4][y])**2
            

            # 4 plugs:
            for a in range(2):
                for b in range(a+1, 3):
                    for c in range(b+1, 4):
                        for d in range(c+1, 5):
                            enig.resetRotorPositions()
                            enig.resetSteckerboard()
                            enig.setSteckerboardPlug(*knownPlugSettings[a])
                            enig.setSteckerboardPlug(*knownPlugSettings[b])
                            enig.setSteckerboardPlug(*knownPlugSettings[c])
                            enig.setSteckerboardPlug(*knownPlugSettings[d])
                            for y in range(6):
                                totals[5][y] += (functions[y](enig.encryptString(cipherText)) - means[5][y])**2
            

            # all plugs:
            enig.resetRotorPositions()
            enig.resetSteckerboard()
            for _ in knownPlugSettings:
                enig.setSteckerboardPlug(*_)
            for y in range(6):
                totals[6][y] += (functions[y](enig.encryptString(cipherText)) - means[6][y])

        plugName = ["cipherText", "none", "one", "two", "three", "four", "five"]
        testName = ["Unigram IOC", "Bigram IOC", "Trigram IOC", "Unigram Sinkov", "Bigram Sinkov", "Trigram Sinkov"]

        # normalizing the results
        
        for x in range(len(totals)):
            for y in range(len(totals[x])):
                totals[x][y] /= count
            
        for x in range(len(totals[2])):
            totals[2][x] /= 5

        for x in range(len(totals[3])):
            totals[3][x] /= 10
        
        for x in range(len(totals[4])):
            totals[4][x] /= 10
        
        for x in range(len(totals[5])):
            totals[5][x] /= 5

        for x in range(len(totals)):
            print(plugName[x]+" plugs", "    Variance" , "\n ___________________________________________", )
            for y in range(len(totals[x])):
                    print(testName[y], " ", totals[x][y])
            print("\n")

            


if __name__ == "__main__":


    e = Enigma()
    tc = testCases()
    l = LanguageRecognition()
    l.loadUnigramTable()
    l.loadBigramTable()
    l.loadTrigramTable()


    with open("UnEnigma/Tests/testPairs.txt", "r") as file:
        t = time.time()
        tc.testScoreVarienceThroughTrials(e, file, l)
        print(time.time() - t)


    '''
    with open("UnEnigma/Tests/testPairs.txt", "r") as file:
        t = time.time()
        tc.testScoreImprovementsThroughTrials(e, file, l)
        print(time.time() -t)

    '''

    '''
    with open("UnEnigma/Tests/ourFuture.txt", "r") as file:
        for line in file:
            with open("UnEnigma/Tests/testPairs.txt", "a") as file2:
                tc.generateSettingsFile(line.strip(), e, file2)
    '''


    '''
    res = 0
    t = None
    with open("Tests/testPairs.txt", "r") as file:
        t = time.time()
        res = tc.testOriginalHillClimbMethod(e, file)
        print("time elapsed (s): ", time.time() - t)

    print(res)
    '''

