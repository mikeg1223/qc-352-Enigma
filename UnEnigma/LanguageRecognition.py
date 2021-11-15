from Enigma import Enigma
import time
import math
import random

class LanguageRecognition:

    unigramTable = {}
    bigramTable = {}
    trigramTable = {}


    def __init__(self):
        self.loadUnigramTable()
        self.loadBigramTable()
        self.loadTrigramTable()


    # These 3 functions load in the unigram/bigram/trigram tables from the text files which were precomputed

    def loadUnigramTable(self):
        with open(r"C:\Users\micha\Desktop\CSCI 352 - Cryptography\Enigma\qc-352-Enigma\Resources\sample_data\unigram_scores.txt", "r") as file:
            for line in file:
                pair = line.split()
                LanguageRecognition.unigramTable[pair[0]] = float(pair[1])
    
    def loadBigramTable(self):
        with open(r"C:\Users\micha\Desktop\CSCI 352 - Cryptography\Enigma\qc-352-Enigma\Resources\sample_data\bigram_scores.txt", "r") as file:
            for line in file:
                pair = line.split()
                LanguageRecognition.bigramTable[pair[0]] = float(pair[1])

    def loadTrigramTable(self):
        with open(r"C:\Users\micha\Desktop\CSCI 352 - Cryptography\Enigma\qc-352-Enigma\Resources\sample_data\trigram_scores.txt", "r") as file:
            for line in file:
                pair = line.split()
                LanguageRecognition.trigramTable[pair[0]] = float(pair[1])


    # Functions to build out our n-gram tables. Only need to be done once for a sample file.
    '''
        def resetTables(self):
            self.unigramTable = {}
            self.bigramTable = {}
            self.trigramTable = {}

        def createTrigramScoring(self, filename: str):
            outputFileName = "Resources/trigram_scores.txt"
            tgrams = {}
            trigramCount = 0
            with open(filename, "r") as file:
                temp = "no"
                for line in file:
                    line = line.strip()
                    line = line.replace(" ", "")
                    if len(line) == 0: continue
                    if temp+line[0] in tgrams:
                        tgrams[temp+line[0]] += 1
                    else:
                        tgrams[temp+line[0]] = 1
                    if temp[1] + line[:2] in tgrams:
                        tgrams[temp[1] + line[:2] ] += 1
                    else:
                        tgrams[temp[1] + line[:2] ] = 1
                    trigramCount += 2
                    temp = line[-2:]
                    for x in range(len(line)-3):
                        if line[x:x+3] in tgrams:
                            tgrams[line[x:x+3]] +=1
                        else:
                            tgrams[line[x:x+3]] = 1
                        trigramCount += 1

                
                    if line[-3:] in tgrams:
                        tgrams[line[-3:]] +=1
                    else:
                        tgrams[line[-3:]] = 1
                    trigramCount += 1
            
            with open(outputFileName, "a") as file:
                for key in tgrams:
                    file.write(key + " " + "{:.8f}".format(tgrams[key]/trigramCount)+ "\n")
        
        def createBigramScoring(self, filename: str):
            outputFileName = "Resources/bigram_scores.txt"
            bgrams = {}
            bigramCount = 0
            with open(filename, "r") as file:
                temp = "I"
                for line in file:
                    line = line.strip()
                    line = line.replace(" ", "")
                    if len(line) ==0: continue
                    if temp+line[0] in bgrams:
                        bgrams[temp+line[0]] += 1
                    else:
                        bgrams[temp+line[0]] = 1
                    bigramCount += 1
                    temp = line[-1]
                    for x in range(len(line)-2):
                        if line[x:x+2] in bgrams:
                            bgrams[line[x:x+2]] +=1
                        else:
                            bgrams[line[x:x+2]] = 1
                        bigramCount += 1
                    
                    if line[-2:] in bgrams:
                            bgrams[line[-2:]] +=1
                    else:
                        bgrams[line[-2:]] = 1
                    bigramCount += 1

            
            with open(outputFileName, "a") as file:
                for key in bgrams:
                    file.write(key + " " + "{:.8f}".format(bgrams[key]/bigramCount)+ "\n")

        def createUnigramScoring(self, filename: str) -> float:
            outputFileName = "Resources/unigram_scores.txt"
            ugrams = {}
            unigramCount = 0
            with open(filename, "r") as file:
                for line in file:
                    line = line.strip()
                    line = line.replace(" ", "")
                    for x in line:
                        if x in ugrams:
                            ugrams[x] +=1
                        else:
                            ugrams[x] = 1
                        unigramCount += 1
            
            with open(outputFileName, "a") as file:
                for key in ugrams:
                    file.write(key + " " + "{:.8f}".format(ugrams[key]/unigramCount)+ "\n")
    '''

    # Functions to create franksteinstein tests
    '''
        def createFrankensteinKDB(self):

            with open("../Resources/frankenstein_samples/Frankenstein.txt","r") as f:
                with open("../Resources/frankenstein_samples/Frankenstein_KDB.txt", "w") as o:
                    for line in f:

                        s = ""
                        s += line.strip()
                        if(len(s) >= 62 ):
                            s = s[:62]
                            s += "kdb"
                            o.write(s + "\n")
                            
        def createFrankensteinTests(self):
            enig = Enigma()


            with open("../Resources/frankenstein_samples/Frankenstein_KDB.txt") as f:
                with open("../Resources/frankenstein_samples/Frankenstein_KDB_tests.txt", "w") as o:
                    for line in f:

                        enig.wipe()

                        alpha = "abcdefghijklmnopqrstuvwxyz"
                        commonLetters="eariotns"


                        rotors = []
                        rings = []
                        plugs = []

                            # Gen rotors
                        for _ in range (3):
                            rotors.append(random.randint(1,8))

                        while rotors[0] == rotors[1] or rotors[0] == rotors[2] or rotors[1] == rotors[2]:
                            rotors = []
                            for _ in range (3):
                                rotors.append(random.randint(1,8))

                            # Gen rings
                        for _ in range(3):
                            rings.append(random.randint(0,25))
                        
                            # set rotors
                        enig.setRotors(rotors[0], rings[0], rotors[1], rings[1], rotors[2], rings[2])


                            # Set steckers
                        plugString =""
                        for i in range(5):
                            if(i < 2):
                                # Fix common letters  array : first
                                firstCommon = random.randint(0, len(commonLetters)-1)
                                first = alpha.find(commonLetters[firstCommon] )
                                commonLetters = commonLetters[:firstCommon] + commonLetters[firstCommon+1:]
                                
                                
                                # Fix alpha
                                c1 = alpha[first]
                                alpha = alpha[:first] + alpha[first+1:]
                                
                                #Fix common letters: second
                                secondCommon = random.randint(0, len(commonLetters)-1)
                                second = alpha.find(commonLetters[secondCommon] )
                                commonLetters = commonLetters[:secondCommon] + commonLetters[secondCommon+1:]

                                #Fix alpha
                                c2 = alpha[second]
                                alpha = alpha[:second] + alpha[second+1:]
                            else:
                                first = random.randint(0, len(alpha)-1)
                                c1 = alpha[first]
                                alpha = alpha[:first] + alpha[first+1:]
                                second = random.randint(0, len(alpha)-1)
                                c2 = alpha[second]
                                alpha = alpha[:second] + alpha[second+1:]

                            if ord(c1) < ord(c2):
                                c1, c2 = c2, c1
                            plugs.append((c1, c2))
                            plugString += (c1 + c2)
                            enig.setSteckerboardPlug(c1,c2)

                        orig = line.strip()
                        cipher = enig.encryptString(orig)
                        rotorSettings = str(rotors[0]) + str(rings[0]).zfill(2) + str(rotors[1]) + str(rings[1]).zfill(2) + str(rotors[2]) + str(rings[2]).zfill(2)
                        o.write(orig + " " + rotorSettings + plugString + " " + cipher + "\n")
    ''' 

    # Functions to perform statistical tests on a given string.

    def indexOfCoincidenceUnigram(self, input: str) -> float:
        
        length = len(input)
        output = 0
        d = {}
        for x in input:
            if x in d:
                d[x] += 1
            else:
                d[x] = 1
        
        for key in d:
            output += d[key] * (d[key] - 1)
        output /= length*(length-1)

        return output  

    def indexOfCoincidenceBigram(self, input: str) -> float:
        bigramCount = len(input) -1
        output = 0
        d = {}
        for x in range(len(input)-1):
            if input[x: x+2] in d:
                d[input[x: x+2]] += 1
            else:
                d[input[x: x+2]] = 1

        
        for key in d:
            output += d[key] * (d[key] - 1)
        output /= bigramCount*(bigramCount-1)

        return output

    def indexOfCoincidenceTrigram(self, input: str) -> float:
        trigramCount = len(input) - 2
        output = 0
        d = {}
        for x in range(len(input)-2):
            if input[x: x+3] in d:
                d[input[x: x+3]] += 1
            else:
                d[input[x: x+3]] = 1

        for key in d:
            output += d[key] * (d[key] - 1)
        output /= trigramCount*(trigramCount-1)

        return output
    
    def sinkovStatisticUnigram(self, input: str) -> float:

        output = 0

        for x in input:
            output += math.log(self.unigramTable[x])

        return output
            
    def sinkovStatisticBigram(self, input: str) -> float:

        output = 0

        for x in range(len(input) - 1):
            if input[x:x+2] in LanguageRecognition.bigramTable:
                output += math.log(LanguageRecognition.bigramTable[input[x:x+2]])
            else:
                output += math.log(0.0004) #1/3 of random dist, same proportion as frq(q) to 1/26

        return output
                
    def sinkovStatisticTrigram(self, input: str) -> float:

        output = 0

        for x in range(len(input) - 2):
            if input[x:x+3] in LanguageRecognition.trigramTable:
                output += math.log(LanguageRecognition.trigramTable[input[x:x+3]])
            else:
                output += math.log(0.0004) #1/3 of random dist, same proportion as frq(q) to 1/26

        return output


    # Functions for testing our statistics
    '''

        def tryTestPairs(self,numTrials):

            with open("../Resources/frankenstein_samples/Frankenstein_KDB_tests.txt", "r") as f:
                with open("../Resources/frankenstein_samples/test_out.txt", "w") as o:

                    e = Enigma()
                    count = 0
                    totalPlugScore = 0.0
                    commonLetters="eariotns"
                    midLetters = "lcudpmhgbfy"
                    rareLetters = "wkvxzjq"
                    plugConfigAry = [0,0,0,0,0,0]
                    numPerfect = 0

                    for line in f:
                        
                        count += 1
                        if(count > numTrials): break
                        words = line.strip().split()
                        cipher = words[2]
                        rotorSettings = words[1][:9]

                        e.wipe()
                        e.setRotors(int(rotorSettings[0]), int(rotorSettings[1] + rotorSettings[2]), int(rotorSettings[3]), int(rotorSettings[4] + rotorSettings[5]), int(rotorSettings[6]), int(rotorSettings[7] + rotorSettings[8]))
                        decrypt = e.encryptString(cipher)

                            # Calculate best plugs return the resultPlugs and resultStr
                        resultPlugs, resultStr = self.tryCommonFirst_findBestPlugs( decrypt, rotorSettings, cipher)


                        num_Common = 0
                        num_Mid = 0
                        num_Rare = 0
                        num_Common_Mid =0
                        num_Mid_rare = 0
                        num_Common_rare = 0

                        for plug in resultPlugs:
                            if plug[0] in commonLetters:
                                if plug[1] in commonLetters:
                                    num_Common += 1
                                elif plug[1] in midLetters:
                                    num_Common_Mid +=1
                                elif plug[1] in rareLetters:
                                    num_Common_rare += 1

                            if plug[0] in midLetters:
                                if plug[1] in commonLetters:
                                    num_Common_Mid +=1
                                elif plug[1] in midLetters:
                                    num_Mid +=1
                                elif plug[1] in rareLetters:
                                    num_Mid_rare += 1

                            if plug[0] in rareLetters:
                                if plug[1] in commonLetters:
                                    num_Common_rare += 1
                                elif plug[1] in midLetters:
                                    num_Mid_rare +=1
                                elif plug[1] in rareLetters:
                                    num_Rare += 1


                            # Score this plug score
                        thisPlugScore = self.plugCompare( words[1][9:], resultPlugs)
                        totalPlugScore += thisPlugScore
                        
                        if (thisPlugScore == 1.0):
                            numPerfect += 1
                            plugConfigAry[0] += num_Common
                            plugConfigAry[1] += num_Common_Mid
                            plugConfigAry[2] += num_Common_rare
                            plugConfigAry[3] += num_Mid
                            plugConfigAry[4] += num_Mid_rare
                            plugConfigAry[5] += num_Rare

                        plugConfig = str(num_Common) + str(num_Common_Mid) + str(num_Common_rare) + "-" + str(num_Mid) + str(num_Mid_rare) + "-" + str(num_Rare) 

                        
                        o.write("-----> TruePlugs = " + words[1][9:] + "  PlugConfig: " +  plugConfig  + "     PlugScore: " + str(round(thisPlugScore,2)))

                    for i in range(6):
                        if(numPerfect > 0):
                            plugConfigAry[i] /= numPerfect

                    o.write("\n\nPlug Config Ary (normalized): " + str(plugConfigAry))
                    o.write("\n\nAVG PLUG SCORE: " + str(totalPlugScore/numTrials))

        def tryIOC(self):

            with open("IOC_unigram/IC_uni_output.txt","r") as f:
                with open("Output_LangRec_OnTop5000IOC.txt","w") as o:

                    count = 0

                    for line in f:

                        count+=1
                        if(count>5): return

                        line = line.strip()
                        words = line.split()
                        decrypt = words[2]
                        rotorSettings = words[0] 

                        self.findBestPlugs( decrypt, rotorSettings, o)

        def tryCribs(self):

                fname = "../Resources/all_possible_Crib/allKDB_"
                oname = "../Resources/tryPlugs_on_cribs/output_"

                for pageNum in range(1,2):

                    fileName = fname + str(pageNum).zfill(2) + ".txt"
                    outName = oname + str(pageNum).zfill(2) + ".txt"

                    with open(fileName, "r") as f:
                        with open(outName, "w" ) as o:

                            for line in f:
                                
                                line = line.strip()
                                words = line.split()

                                decrypt = words[6]
                                rotorSettings = str(words[0]) + str(words[1]) + str(words[2])+ str(words[3]) + str(words[4]) + str(words[5]) 

                                self.findBestPlugs( decrypt, rotorSettings, o)
    '''
    
    
    def tryResults(self):

        fname = "../Resources/pluglessIOCandBiSinkov/results_"
        oname = "../Resources/actualTests/pluglessResults_"

        for pageNum in range(1,5):

            with open(fname+str(pageNum).zfill(2)+".txt", "r") as f:
                with open(oname+str(pageNum).zfill(2)+".txt", "w") as o:

                    for line in f:

                            # Extract the rotor settings and decrypt
                        words = line.strip().split()
                        decrypt = words[1]
                        rotorSettings = words[0]


                            # Calculate best plugs return the resultPlugs and resultStr
                        resultStr = self.tryCommonFirst_findBestPlugs( decrypt, rotorSettings)
                        o.write(resultStr)

    def plugCompare(self, truePlugs: str, calcPlugs: list ):
        score = 0.0

        for pair in calcPlugs:

            #Note: The reason for find()%2 ==0 is to ensure we correctly confirm that this plug was paired:
            # For example:        ABCD             the plugs are [AB] and [CD]
            #       But without confirming, we might find that BC is a plug and score that (incorrectly)
                    # Check for this exact plug pairing in the string
            if (truePlugs.__contains__(pair) and truePlugs.find(pair[0])%2 == 0): score += 2 
                     # plug pairing in reverse. AB = BA
            elif truePlugs.__contains__( str(pair[1] + pair[0]) ) and (truePlugs.find(pair[1])%2 == 0): score += 2  

        return score/10

    def makeHistogram(self, numTrials:int ):

        with open("../Resources/frankenstein_samples/test_out.txt","r") as f:
            with open("../Resources/frankenstein_samples/Frankenstein_hist1.txt","w") as o:

                f.readline()
                count =0
                histAry = {
                    0.0:0,
                    0.2:0,
                    0.4:0,
                    0.6:0,
                    0.8:0,
                    1.0:0
                }

                for line in f:
                    count = count+1
                    if(count >= numTrials): break
                    words = line.strip().split()
                    val = float(words[-1])
                    histAry[val] = histAry[val] + 1
                
                for val in histAry:
                    o.write("\n" + str(val) + "[" + str(histAry[val]) + "]: " )
                    for _ in range(histAry[val]):
                        o.write( "+")


        '''
                # Code to compute string score histograms
                        histAry = { }

                        for line in f:
                            count = count+1
                            if(count > numTrials): break
                            line = line.strip()
                            words = line.split()
                            value = round(float(words[-3]),2)
                            if value in histAry: histAry[value] = histAry[value]+1
                            else: histAry[value] =1

                        val = -0.01
                        while(val <= 1.00):
                            val = round(val + .01,2)
                            if val in histAry:
                                o.write("\n" + str(val) + "[" + str(histAry[val]) + "]: " )
                                for _ in range(histAry[val]):
                                    o.write( "+")
        '''
    
    # Function to determine the 5 best plugs for a given string.

    def findBestPlugs(self, decrypt, rotorSettings, outFile, cipher="egcvqcsahlfmctzgwwxikupvunrujaqimbxnwjhkwnxnisjaqbmouylcbxdnvdbvf"):

        alpha = "abcdefghijklmnopqrstuvwxyz"
        plugs = []
        lastString = ""
        testString = decrypt[:62]
        test = self.sinkovStatisticBigram
        baseLine = test(testString)

        e = Enigma()
        e.setRotors(int(rotorSettings[0]), int(rotorSettings[1] + rotorSettings[2]), int(rotorSettings[3]), int(rotorSettings[4] + rotorSettings[5]), int(rotorSettings[6]), int(rotorSettings[7] + rotorSettings[8]))
        
            # Repeat for 5 plug pairs
        for _ in range(5):


            maxSoFar = baseLine

            # Iterate x from 'A' to 'Y'
            for x in range(len(alpha)-1):

                # Iterate y from 'x+1' to 'Z'
                for y in range(x+1,len(alpha)):
                        
                    # Reset enigma object 
                    e.resetSteckerboard()
                    e.resetRotorPositions()

                    # Set the plugs we already found
                    for pair in plugs:
                        e.setSteckerboardPlug(pair[0],pair[1])

                    # Set plugs for this trial
                    e.setSteckerboardPlug(alpha[x], alpha[y])

                    s = e.encryptString(cipher)
                    score = test(s[:62])

                        # If we found a new best plug on this trial
                    if (score > maxSoFar):
                        maxSoFar = score
                        bestA = x
                        bestB = y
                        best = alpha[x] + alpha[y]
                        lastString = s

            
            # If we couldn't find a single improvement among any steckerboard pairs
            # End the simulation now, no need to get all 5 plug pairs
            if(maxSoFar <= baseLine):
                #outFile.write("\ncipher -->  Rotor: " + rotorSettings + " --> " + decrypt + " --> Plugs:" + str(plugs) + " --->  " + lastString) 
                return None, None
            
            #otherwise: add the best pair to the list of plugs, and remove them from the alphabet
            else:
                plugs.append(best)
                alpha = alpha[:bestA] + alpha[bestA+1:bestB] + alpha[bestB+1:]
        

        # When completed with 5 rounds, return plugs
        outFile.write("\ncipher -->  Rotor: " + rotorSettings + " --> " + decrypt + " --> Plugs:" + str(plugs) + " --->  " + lastString )
        return plugs,lastString 

    def tryCommonFirst_findBestPlugs(self, decrypt, rotorSettings):

        cipher="egcvqcsahlfmctzgwwxikupvunrujaqimbxnwjhkwnxnisjaqbmouylcbxdnvdbvf"
        alpha = "abcdefghijklmnopqrstuvwxyz"
        commonLetters="etnorias"
        lastString =""
        plugs = []
        test = self.sinkovStatisticBigram


            # We cut off the last 3 letters so we can handle the fact that 'kdb' is not a good bigram
        testString = decrypt[:62]

        e = Enigma()
        e.setRotors(int(rotorSettings[0]), int(rotorSettings[1] + rotorSettings[2]), int(rotorSettings[3]), int(rotorSettings[4] + rotorSettings[5]), int(rotorSettings[6]), int(rotorSettings[7] + rotorSettings[8]))
        
            # Repeat 5 times for 5 plug pairs
        for i in range(5):

            baseLine = test(testString)
            maxSoFar = baseLine

            # For first trial, look for best 1 plug
            if(i<1):
                # Iterate x from across list of common letters
                for x in range(len(commonLetters)-1):

                    for y in range(x+1,len(commonLetters)):
                            
                        # Reset enigma object 
                        e.resetSteckerboard()
                        e.resetRotorPositions()

                        # Set the plugs we already found
                        
                        for pair in plugs:
                            e.setSteckerboardPlug(pair[0],pair[1])

                        # Set plugs for this trial
                        e.setSteckerboardPlug(commonLetters[x], commonLetters[y])

                        s = e.encryptString(cipher)
                        score = test(s[:62])

                            # If we found a new best plug on this trial
                        if (score > maxSoFar):
                            maxSoFar = score
                            bestA = x
                            bestB = y
                            best = commonLetters[x] + commonLetters[y]
                            lastString = s

            # Else, look for best any plugs
            else:

                # Iterate x from 'A' to 'Y'
                for x in range(len(alpha)-1):

                    # Iterate y from 'x+1' to 'Z'
                    for y in range(x+1,len(alpha)):
                            
                        # Reset enigma object 
                        e.resetSteckerboard()
                        e.resetRotorPositions()

                        # Set the plugs we already found
                        for pair in plugs:
                            e.setSteckerboardPlug(pair[0],pair[1])

                        # Set plugs for this trial
                        e.setSteckerboardPlug(alpha[x], alpha[y])

                            # Re-encrypt the cipher with new plugs
                        s = e.encryptString(cipher)
                        score = test(s[:62])

                            # If we found a new best plug on this trial
                        if (score > maxSoFar):
                            maxSoFar = score
                            bestA = x
                            bestB = y
                            best = alpha[x] + alpha[y]
                            lastString = s

            
            

            # If we haven't improved, this is a junk string and we can stop now
            if(maxSoFar <= baseLine):
                outString = ("\nRotor: " + rotorSettings + " --> " + decrypt + " --> Plugs:" + str(plugs) + " --->  " + lastString) 
                return outString 


            #otherwise: add the best pair to the list of plugs, and remove them from the alphabet
            plugs.append(best)
            
            # if first trial, we need to remove letters from alphabet in a tricky way
            if(i < 1):
                # Remove them from alphabet first
                alpha = alpha.replace(commonLetters[bestA],"")
                alpha = alpha.replace(commonLetters[bestB],"")
                
                # Remove them from commonLetters (only useful if we decide to assume MORE than one common-common paring)
                commonLetters = commonLetters[:bestA] + commonLetters[bestA+1:bestB] + commonLetters[bestB+1:]

            #otherwise, it is more direct
            else: alpha = alpha[:bestA] + alpha[bestA+1:bestB] + alpha[bestB+1:]
        

        # When completed with 5 rounds, return plugs
        outString = ("\nRotor: " + rotorSettings + " --> " + decrypt + " --> Plugs:" + str(plugs) + " --->  " + lastString )
        return outString


    # Functions to thin the field of our 6 mill decrypts
    def getIOCwithinARange(self):
        fname = "../Resources/pluglessResults/pluglessResults_"

        for pageNum in range(1,57):
            with open(fname+str(pageNum).zfill(2)+".txt") as f:
                with open("../Resources/pluglessIOCandBiSinkov/results_"+str(pageNum).zfill(2) +".txt","w") as o:
                    for line in f:
                        words = line.strip().split()
                        decrypt = words[6]
                        IOCscore = self.indexOfCoincidenceUnigram(decrypt) 
                        if(IOCscore > 0.041) and (IOCscore < 0.053) :
                            biSinkovscore = self.sinkovStatisticBigram(decrypt)
                            if(biSinkovscore > -482) and (biSinkovscore < -435):
                                rotorConfig = str(words[0]) + str(words[1]).zfill(2) + str(words[2]) + str(words[3]).zfill(2) + str(words[4]) + str(words[5]).zfill(2)
                                o.write(rotorConfig + " " + decrypt + "\n")

    def testPluglessScoreAverages(self):

        with open("../Resources/frankenstein_samples/Frankenstein_KDB_tests.txt", "r") as f:

            e = Enigma()
            count = 0
            meanUniIOC = 0.048
            meanBiIOC = 0.0024
            meanbiSinkov = -454.2403667697373
            totalBiSinkov = 0
            totalUniIOC = 0
            totalBiIOC = 0

            for line in f:
                
                count += 1
                if(count > 100): break
                words = line.strip().split()
                cipher = words[2]
                rotorSettings = words[1][:9]
                e.setRotors(int(rotorSettings[0]), int(rotorSettings[1] + rotorSettings[2]), int(rotorSettings[3]), int(rotorSettings[4] + rotorSettings[5]), int(rotorSettings[6]), int(rotorSettings[7] + rotorSettings[8]))
                decrypt = e.encryptString(cipher)
                totalBiSinkov += pow( meanbiSinkov - self.sinkovStatisticBigram(decrypt),2)
                totalUniIOC += pow(meanUniIOC - self.indexOfCoincidenceUnigram(decrypt),2)
                totalBiIOC += pow(meanBiIOC - self.indexOfCoincidenceBigram(decrypt),2)

            totalBiSinkov /= 100
            totalUniIOC /= 100
            totalBiIOC /= 100



            print("\nVar for bisinkov successfull decrypt = " + str(totalBiSinkov) )
            print("\nVar for uni IOC for successfull decrypt = " + str(totalUniIOC) )
            print("\nVar for bi IOC successfull decrypt = " + str(totalBiIOC) )


    def betterFindBestPlugs(self, decrypt: str, rotorSettings: str, f,cipher: str) -> list:

        alpha = "abcdefghijklmnopqrstuvwxyz"
        plugs = []
        lastString = ""

        e = Enigma()
        e.setRotors(int(rotorSettings[0]), int(rotorSettings[1] + rotorSettings[2]), int(rotorSettings[3]), int(rotorSettings[4] + rotorSettings[5]), int(rotorSettings[6]), int(rotorSettings[7] + rotorSettings[8]))
        
            # Repeat for 5 plug pairs
        for _ in range(5):

            # test = self.sinkovStatisticBigram

            baseLine = f(decrypt)
            maxSoFar = baseLine

            # Iterate x from 'A' to 'Y'
            for x in range(len(alpha)-1):

                # Iterate y from 'x+1' to 'Z'
                for y in range(x+1,len(alpha)):
                        
                    # Reset enigma object 
                    e.resetSteckerboard()
                    e.resetRotorPositions()

                    # Set the plugs we already found
                    for pair in plugs:
                        e.setSteckerboardPlug(pair[0],pair[1])

                    # Set plugs for this trial
                    e.setSteckerboardPlug(alpha[x], alpha[y])

                    s = e.encryptString(cipher)
                    score = f(s)

                        # If we found a new best plug on this trial
                    if (score > maxSoFar):
                        maxSoFar = score
                        bestA = x
                        bestB = y
                        best = alpha[x] + alpha[y]
                        lastString = s

            
            #otherwise: add the best pair to the list of plugs, and remove them from the alphabet
            else:
                plugs.append(best)
                alpha = alpha[:bestA] + alpha[bestA+1:bestB] + alpha[bestB+1:]
        
        return plugs



    # program runs from below 
if __name__ == "__main__":
    start = time.time()
    l = LanguageRecognition()
    l.tryResults()
    end = time.time()
    print(str(end- start) + " seconds in total") 
