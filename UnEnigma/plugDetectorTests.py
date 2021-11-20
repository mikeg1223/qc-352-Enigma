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


    '''def testOriginalHillClimbMethod(self, enig: Enigma, f) -> float:
        
        results = 0
        numTrials = 0
        #us = UniSinkovTest()
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
    '''

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

        means = [[0.03851383766038299, 0.0014744485351965888, 5.671894873885871e-05,-255.44619883833647, -636.7057647373646, -994.9783990048187],
                [0.048486198302156114, 0.002835849617626333, 0.0002348217681214902, -228.80141111761088, -536.1167062887033, -870.1761838420836 ],
                [0.051320603203003766,0.003439037740998043, 0.0003750988527416976, -222.2195651123471, -508.5138642429462, -825.9992712843441],
                [0.054510873648711454, 0.004229413288313244, 0.0006023698444590284, -214.75125604528617, -476.00785864733507, -768.7663177848387],
                [0.058057009639345535, 0.0052480056893026575, 0.0009606266399656008, -206.396483916423, -438.1594222998891, -695.3194748604253],
                [0.06195901117490209, 0.006540707304762179, 0.0015081216890610225, -197.15524872575634, -394.4654350388413, -601.7992391755156],
                [0.06621687825533423, 0.008158273426569784, 0.002322136756688445, -187.02755047329327, -344.35892374260027, -483.5556386675069]]

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
                totals[6][y] += (functions[y](enig.encryptString(cipherText)) - means[6][y]) ** 2

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


    def scoreAllRotorsWithIOC(self):
        lr = LanguageRecognition()
        topsinkov = []
        for _ in range(1, 57):
            with open(r"C:\Users\micha\Desktop\CSCI 352 - Cryptography\Enigma\qc-352-Enigma\Resources\pluglessResults\pluglessResults_"+str(_).zfill(2)+".txt", "r") as file:
                for line in file:
                    line = line.strip().split()
                    key = ""
                    for _ in range(len(line) - 1):
                        key += line[_] + " "
                    sinkovstats = lr.sinkovStatisticUnigram(line[-1])
                    score = abs(sinkovstats - (-228.80141111761088))
                    topsinkov.append((key, line[-1], score))
                topsinkov.sort(key = lambda x: x[2])
                if _ > 3:
                    topsinkov = topsinkov[:400000]

        with open("top100000.txt", "w") as file:
            for _ in range(100000):
                file.write(topsinkov[_][0] + "\t" + topsinkov[_][1] + "\t" + str(topsinkov[_][2])+ "\n")
        with open("second100000.txt", "w") as file:
            for _ in range(100000, 200000):
                file.write(topsinkov[_][0] + "\t" + topsinkov[_][1] + "\t" + str(topsinkov[_][2])+ "\n")
        with open("third100000.txt", "w") as file:
            for _ in range(200000, 300000):
                file.write(topsinkov[_][0] + "\t" + topsinkov[_][1] + "\t" + str(topsinkov[_][2])+ "\n")
        with open("last100000.txt", "w") as file:
            for _ in range(300000, 400000):
                file.write(topsinkov[_][0] + "\t" + topsinkov[_][1] + "\t" + str(topsinkov[_][2])+ "\n")
                    
                    
    def scoreEncryptedMessages(self):
        count = 0
        scoreUnigramIOC = 0
        scoreBigramIOC = 0
        scoreTrigramIOC = 0
        scoreUnigramSinkov = 0
        scoreBigramSinkov = 0
        scoreTrigramSinkov = 0

        with open(r"C:\Users\micha\Desktop\CSCI 352 - Cryptography\Enigma\qc-352-Enigma\UnEnigma\Tests\testPairs.txt", "r") as file:
            for line in file:
                line = line.strip().split()
                count += 1
                scoreUnigramIOC += self.langRec.indexOfCoincidenceUnigram(line[-1])
                scoreBigramIOC += self.langRec.indexOfCoincidenceBigram(line[-1])
                scoreTrigramIOC += self.langRec.indexOfCoincidenceTrigram(line[-1])
                scoreUnigramSinkov += self.langRec.sinkovStatisticUnigram(line[-1])
                scoreBigramSinkov += self.langRec.sinkovStatisticBigram(line[-1])
                scoreTrigramSinkov += self.langRec.sinkovStatisticTrigram(line[-1])

        print("Encryped Scores \n ____________________________________")
        print("Unigram IOC\t", scoreUnigramIOC/count)
        print("Bigram IOC\t", scoreBigramIOC/count)
        print("Trigram IOC\t", scoreTrigramIOC/count)
        print("Unigram Sinkov\t", scoreUnigramSinkov/count)
        print("Bigram Sinkov\t", scoreBigramSinkov/count)
        print("Trigram Sinkov\t", scoreTrigramSinkov/count)
            


if __name__ == "__main__":


    e = Enigma()
    tc = testCases()
    tc.scoreEncryptedMessages()

    '''
    tc.scoreAllRotorsWithIOC()

    countFast1 = {"1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0}
    countMid1 = {"1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0}
    countSlow1 = {"1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0}
    with open("top100000.txt", "r") as file:
        count = 0
        for line in file:
            if count > 1000:
                break
            count += 1
            line = line.strip().split()
            countFast1[line[0]] += 1
            countMid1[line[2]] += 1
            countSlow1[line[4]] += 1
    
    print("rotor configurations for top 1000")
    print("fast: ", countFast1)
    print("middle: ", countMid1)
    print("slow: ", countSlow1, "\n")

    countFast2 = {"1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0}
    countMid2 = {"1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0}
    countSlow2 = {"1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0}
    
    with open("second100000.txt", "r") as file:
        for line in file:
            line = line.strip().split()
            countFast2[line[0]] += 1
            countMid2[line[2]] += 1
            countSlow2[line[4]] += 1

    print("rotor configuration stats for 100001 - 200000")
    print("fast: ", countFast2)
    print("middle: ", countMid2)
    print("slow: ", countSlow2, "\n")

    countFast3 = {"1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0}
    countMid3 = {"1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0}
    countSlow3 = {"1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0}
    
    with open("third100000.txt", "r") as file:
        for line in file:
            line = line.strip().split()
            countFast3[line[0]] += 1
            countMid3[line[2]] += 1
            countSlow3[line[4]] += 1

    print("rotor configuration stats for 200001 - 300000")
    print("fast: ", countFast2)
    print("middle: ", countMid2)
    print("slow: ", countSlow2, "\n")


    countFast4 = {"1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0}
    countMid4 = {"1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0}
    countSlow4 = {"1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0}
    
    with open("last100000.txt", "r") as file:
        for line in file:
            line = line.strip().split()
            countFast4[line[0]] += 1
            countMid4[line[2]] += 1
            countSlow4[line[4]] += 1

    print("rotor configuration stats for 300001 - 400000")
    print("fast: ", countFast4)
    print("middle: ", countMid4)
    print("slow: ", countSlow4, "\n")

    countFast = {"1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0}
    countMid = {"1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0}
    countSlow = {"1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0}
    
    for _ in countFast:
        countFast[_] = countFast1[_] + countFast2[_] + countFast3[_] + countFast4[_]
        countMid[_] = countMid1[_] + countMid2[_] + countMid3[_] + countMid4[_]
        countSlow[_] = countSlow1[_] + countSlow2[_] + countSlow3[_] + countSlow4[_]
    
    print("rotor configuration stats for 1 - 400000")
    print("fast: ", countFast)
    print("middle: ", countMid)
    print("slow: ", countSlow, "\n")
        
    '''


    '''
    with open("UnEnigma/Tests/testPairs.txt", "r") as file:
        t = time.time()
        tc.testScoreImprovementsThroughTrials(e, file, tc.langRec)
        print(time.time() -t)

    with open("UnEnigma/Tests/testPairs.txt", "r") as file:
        t = time.time()
        tc.testScoreVarienceThroughTrials(e, file, tc.langRec)
        print(time.time() - t)

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

