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
        with open("../Resources/sample_data/unigram_scores.txt", "r") as file:
            for line in file:
                pair = line.split()
                LanguageRecognition.unigramTable[pair[0]] = float(pair[1])
    
    def loadBigramTable(self):
        with open("../Resources/sample_data/bigram_scores.txt", "r") as file:
            for line in file:
                pair = line.split()
                LanguageRecognition.bigramTable[pair[0]] = float(pair[1])

    def loadTrigramTable(self):
        with open("../Resources/sample_data/trigram_scores.txt", "r") as file:
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


    # Functions to perform statistical tests on a given string.
    '''
        The following 6 functions are all statistical tests to give a string a 'score' in English
        
        A unigram is any character                  (26 total unigrams)
        A bigram is any permutation of 2 characters (26*26 possible bigrams)
        A trigram is any permutation of 3 characters(26*26*26 possible trigrams)

        Sinkov statistics will score a string based on the log(frequencies) of the exact particular n-grams that compose the string
            For example: If a string  has 'th' in its string, it will have a better Sinkov score than a string that has 'xq' in its string
                          'th' is a very common bigram, while 'xq' is almost impossible to appear.

        Index of Coincidence statistic will score a string based on the frequencies of any n-grams within the string 
            For example: "aabbccdd" will have a higher IOC score than  "abcdefgh" because there are more repetitions of letters within the string 
    '''

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

    def tryTestPairs(self,numTrials):

        with open("../Resources/customPlugsTest/readIn1.txt", "r") as f:
            with open("../Resources/customPlugsTest/out2.txt", "w") as o:

                e = Enigma()
                count = 0
                totalStrScore = 0.0
                totalPlugScore = 0.0

                for line in f:
                    
                    count += 1
                    if(count > numTrials): break
                    words = line.strip().split()
                    cipher = words[2]
                    rotorSettings = words[1][:9]

                    e.wipe()
                    e.setRotors(int(rotorSettings[0]), int(rotorSettings[1] + rotorSettings[2]), int(rotorSettings[3]), int(rotorSettings[4] + rotorSettings[5]), int(rotorSettings[6]), int(rotorSettings[7] + rotorSettings[8]))
                    decrypt = e.encryptString(cipher)

                        #Calculate best plugs return the resultPlugs and resultStr
                    resultPlugs, resultStr = self.findBestPlugs( decrypt, rotorSettings, o, cipher)

                        # Score this string score
                    thisStrScore = self.strCompare(   words[0], resultStr )
                    totalStrScore += thisStrScore

                        # Score this plug score
                    thisPlugScore = self.plugCompare( words[1][9:], resultPlugs)
                    totalPlugScore += thisPlugScore
                    o.write("-----> TruePlugs = " + words[1][9:] + "     StringScore: " + str(round(thisStrScore,2)) + "     PlugScore: " + str(round(thisPlugScore,2)))


                o.write("\n\n AVG STR SCORE: " + str((totalStrScore/numTrials)) + " \n AVG PLUG SCORE: " + str(totalPlugScore/numTrials))
                print("\n\n AVG STR SCORE: " + str(totalStrScore/numTrials) + " \n AVG PLUG SCORE: " + str(totalPlugScore/numTrials))

    '''
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

    def strCompare(self, s1: str, s2: str) -> float:
        score = 0.0
        for i in range(len(s1)):
            if(s1[i] == s2[i]): score+=1
        
            # Returns a percentage of the matching characters of s1 that match s2
        return score/len(s1)

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

        with open("../Resources/customPlugsTest/out2.txt","r") as f:
            with open("../Resources/customPlugsTest/hist1.txt","w") as o:

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
                    if(count > numTrials): break
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

        e = Enigma()
        e.setRotors(int(rotorSettings[0]), int(rotorSettings[1] + rotorSettings[2]), int(rotorSettings[3]), int(rotorSettings[4] + rotorSettings[5]), int(rotorSettings[6]), int(rotorSettings[7] + rotorSettings[8]))
        
            # Repeat for 5 plug pairs
        for _ in range(5):

            test = self.sinkovStatisticBigram

            baseLine = test(decrypt)
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
                    score = test(s)

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
                outFile.write("\ncipher -->  Rotor: " + rotorSettings + " --> " + decrypt + " --> Plugs:" + str(plugs) + " --->  " + lastString) 
                return plugs,lastString
            
            #otherwise: add the best pair to the list of plugs, and remove them from the alphabet
            else:
                plugs.append(best)
                alpha = alpha[:bestA] + alpha[bestA+1:bestB] + alpha[bestB+1:]
        

        # When completed with 5 rounds, return plugs
        outFile.write("\ncipher -->  Rotor: " + rotorSettings + " --> " + decrypt + " --> Plugs:" + str(plugs) + " --->  " + lastString )
        return plugs,lastString 


    # Function to create testPairs
    def createTestPairs(self,numTrials):

        with open("../Resources/customPlugsTest/readIn1.txt", "w") as o:
                
                stringsToDecipher = ["thehistoryofallhithertoexistingsocietiesisthehistoryofclassstrugg", "urneymaninawordoppressorandoppressedstoodinconstantoppositiontoon", "lesfreemanandslavepatricianandplebeianlordandserfguildmasterandjo"]
                rotorsConfigs = ["313607105","101522619","714224417"]
                commonLetters="eariotns"
                midLetters = "lcudpmhgbfy"
                rareLetters = "wkvxzjq"

                rand = random.Random()
                rand.seed()
                e = Enigma()
                trials = numTrials


                for count in range(trials):

                    e.wipe()

                        # Pick the string to encrypt
                    if count<33:
                        s = stringsToDecipher[0]
                    elif count < 67: 
                        s = stringsToDecipher[1]
                    else:
                        s=stringsToDecipher[2]

                        # Pick the rotors to encrypt

                    if count%3 == 0:
                        r = rotorsConfigs[0]
                    elif count%3 == 1:
                        r = rotorsConfigs[1]
                    else:
                        r = rotorsConfigs[2]

                    e.setRotors(int(r[0]), int(r[1]+r[2]), int(r[3]) , int(r[4]+r[5]) , int(r[6]), int(r[7]+r[8]))
                    o.write(s + " " + r) 


                        # Pick the 5 stecker pairs
                    selectedLetters = ""
                    
                    for i in range(5):

                        if(i == 0):
                            firstChar = commonLetters
                            secondChar = rareLetters
                        elif(i == 1):
                            firstChar = commonLetters
                            secondChar = midLetters
                        elif(i == 2):
                            firstChar = midLetters
                            secondChar = midLetters
                        elif(i == 3):
                            firstChar = midLetters
                            secondChar = midLetters
                        elif(i == 4):
                            firstChar = midLetters
                            secondChar = rareLetters
                        
                        letter1 = self.pickRandomChar(firstChar, selectedLetters)
                        selectedLetters += letter1
                        letter2 = self.pickRandomChar(secondChar, selectedLetters)
                        selectedLetters +=  letter2

                        e.setSteckerboardPlug(letter1, letter2)
                        o.write(letter1 + letter2)




                    cipher = e.encryptString(s)
                    o.write( " " + cipher + "\n")


    def pickRandomChar(self, s:str, selected:str):

        rand = random.SystemRandom()        
            #Repeat till we find a valid random char
        for char in selected:
            s = s.replace(char, "")

        return s[rand.randint(0,len(s)-1)]


    # program runs from below 
if __name__ == "__main__":
    numTrials = 100
    start = time.time()
    l = LanguageRecognition()
    l.createTestPairs(numTrials)
    l.tryTestPairs(numTrials)
    l.makeHistogram(numTrials)
    print(str((time.time() - start)/numTrials) + " seconds per compute") 
