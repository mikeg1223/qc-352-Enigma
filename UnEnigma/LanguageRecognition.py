import BiSinkov
from Enigma import Enigma
from BiSinkov.BiSinkovTest import BiSinkovTest
from UniSinkov.UniSinkovTest import UniSinkovTest
import IOC_bigram
import time
import math

class LanguageRecognition:

    unigramTable = {}
    bigramTable = {}
    trigramTable = {}
    UNIGRAM_TABLE_LOADED = False
    BIGRAM_TABLE_LOADED = False
    TRIGRAM_TABLE_LOADED = False

    def __init__(self):
        self.loadUnigramTable()
        self.loadBigramTable()
        self.loadTrigramTable()


    # These 3 functions load in the unigram/bigram/trigram tables from the text files which were precomputed

    def loadUnigramTable(self):
        with open("../Resources/unigram_scores.txt", "r") as file:
            for line in file:
                pair = line.split()
                LanguageRecognition.unigramTable[pair[0]] = float(pair[1])
        LanguageRecognition.UNIGRAM_TABLE_LOADED = True
    
    def loadBigramTable(self):
        with open("../Resources/bigram_scores.txt", "r") as file:
            for line in file:
                pair = line.split()
                LanguageRecognition.bigramTable[pair[0]] = float(pair[1])
        LanguageRecognition.BIGRAM_TABLE_LOADED = True

    def loadTrigramTable(self):
        with open("../Resources/trigram_scores.txt", "r") as file:
            for line in file:
                pair = line.split()
                LanguageRecognition.trigramTable[pair[0]] = float(pair[1])
        LanguageRecognition.TRIGRAM_TABLE_LOADED = True

    def resetTables(self):
        self.unigramTable = {}
        self.bigramTable = {}
        self.trigramTable = {}

    # The following 3 functions are used to compute the scoring for different bigrams and trigrams, and write them to outFiles.
    # When done once for a sample, they don't need to be performed again unless to re-compute.

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

    '''
        This function is the driver of LanguageRecognition
        It runs the algorithm to solve for the best plugs 1 by 1 by using language recognition statistics.
        The choice of statistic used can be changed 
    '''

    def findBestPlugs(self, decrypt, rotorSettings, outFile, cipher="egcvqcsahlfmctzgwwxikupvunrujaqimbxnwjhkwnxnisjaqbmouylcbxdnvdbvf"):

        alpha = "abcdefghijklmnopqrstuvwxyz"
        plugs = []
        lastString = ""

        e = Enigma()
        e.setRotors(int(rotorSettings[0]), int(rotorSettings[1] + rotorSettings[2]), int(rotorSettings[3]), int(rotorSettings[4] + rotorSettings[5]), int(rotorSettings[6]), int(rotorSettings[7] + rotorSettings[8]))
        
        baseLine = self.sinkovStatisticBigram(decrypt)

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
                    score = self.sinkovStatisticBigram(s)

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
                outFile.write("cipher -->  Rotor: " + rotorSettings + " --> " + decrypt + " --> Plugs:" + str(plugs) + " --->  " + lastString + "\n") 
                return 
            
            #otherwise: add the best pair to the list of plugs, and remove them from the alphabet
            else:
                plugs.append(best)
                alpha = alpha[:bestA] + alpha[bestA+1:bestB] + alpha[bestB+1:]
        

        # When completed with 5 rounds, return plugs
        outFile.write("cipher -->  Rotor: " + rotorSettings + " --> " + decrypt + " --> Plugs:" + str(plugs) + " --->  " + lastString + "\n") 


        '''
        These methods are just used to run the findBestPlugs() function on different files.
        We stored files with different formats so they need to be read in differently.
        Each one of these functions is tailored to a different input feed
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

    def tryTestPairs(self):

        with open("Tests/testPairs.txt","r") as f:
            with open("Tests/output_testPairs.txt","w") as o:

                e = Enigma()
                count = 0
                for line in f:
                    
                    count += 1
                    if(count > 5): return
                    line = line.strip()
                    words = line.split()
                    cipher = words[2]
                    rotorSettings = words[1][:9]

                    e.wipe()
                    e.setRotors(int(rotorSettings[0]), int(rotorSettings[1] + rotorSettings[2]), int(rotorSettings[3]), int(rotorSettings[4] + rotorSettings[5]), int(rotorSettings[6]), int(rotorSettings[7] + rotorSettings[8]))
                    decrypt = e.encryptString(cipher)

                    self.findBestPlugs( decrypt, rotorSettings, o, cipher)

    def hillClimbing(self,input: str):
        pass

# program runs from below 
if __name__ == "__main__":
    start = time.time()
    l = LanguageRecognition()
    l.tryTestPairs()
    print(str((time.time() - start)/5) + " seconds per compute") 
