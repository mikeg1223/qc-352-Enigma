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
        pass



    def loadUnigramTable(self):
        with open("Resources/unigram_scores.txt", "r") as file:
            for line in file:
                pair = line.split()
                LanguageRecognition.unigramTable[pair[0]] = float(pair[1])
        LanguageRecognition.UNIGRAM_TABLE_LOADED = True


    
    def loadBigramTable(self):
        with open("Resources/bigram_scores.txt", "r") as file:
            for line in file:
                pair = line.split()
                LanguageRecognition.bigramTable[pair[0]] = float(pair[1])
        LanguageRecognition.BIGRAM_TABLE_LOADED = True


    def loadTrigramTable(self):
        with open("Resources/trigram_scores.txt", "r") as file:
            for line in file:
                pair = line.split()
                LanguageRecognition.trigramTable[pair[0]] = float(pair[1])
        LanguageRecognition.TRIGRAM_TABLE_LOADED = True


    def resetTables(self):
        self.unigramTable = {}
        self.bigramTable = {}
        self.trigramTable = {}


    def tryIOC(self):

        with open("IOC_unigram/IC_uni_output.txt") as f:
        #with open("../Resources/test.txt", "r") as f:
        #with open("../Resources/possibleCribContaining.txt", "r") as f:
        #with open("../Resources/pluglessResults/pluglessResults_" + "01" + ".txt", "r") as f:
            with open("Output_LangRec_OnTop5000IOC.txt","w") as o:

                for line in f:
                    
                    alpha = "abcdefghijklmnopqrstuvwxyz"
                    cipher = "egcvqcsahlfmctzgwwxikupvunrujaqimbxnwjhkwnxnisjaqbmouylcbxdnvdbvf"

                    line = line.strip()
                    words = line.split()
                    decrypt = words[2]

                    plugs = []
                    lastString = ""
                    us = UniSinkovTest()

                    baseLine = us.computeSinkov(decrypt) 

                    #initialize variables to capture current best plug
                    for i in range(5):

                        maxSoFar = baseLine

                        #iterate x from 'A' to 'Y'
                        for x in alpha:

                            #iterate y from 'X+1' to 'Z'
                            for y in alpha:
                                    
                            #re-initialize enigma object with rotors
                                e = Enigma()
                                e.setRotors(int(words[0][0]), int(words[0][1]+words[0][2]), int(words[0][3]), int(words[0][4]+words[0][5]), int(words[0][6]), int(words[0][7] + words[0][8]))

                                #not sure how to iterate through dictionary but I want to set found plugs
                                for pair in plugs:
                                    e.setSteckerboardPlug(pair[0],pair[1])

                                #set the current plug
                                e.setSteckerboardPlug(x, y)

                                #encrypt the cipher with the plugs, see if it's better, and store
                                s = e.encryptString(cipher)
                                score = us.computeSinkov(s)
                                if (score > maxSoFar):
                                    a = alpha.find(x)
                                    b = alpha.find(y)
                                    maxSoFar = score
                                    best = x + y
                                    lastString = s

                        #add best to plugs
                        plugs.append(best)

                        # remove plugged letters from alphabet
                        alpha = alpha[:a] + alpha[a+1:b] + alpha[b+1:]

                    # write output for this line
                    o.write(
                        str(words[0])+" "+ decrypt + " " + str(plugs) + " " + lastString + "\n"
                    ) 

        
                #and then you would store in a new text file the rotor settings, plugs, and updated decrypt

    def tryCribs(self):

            fname = "../Resources/all_possible_Crib/allKDB_"
            oname = "../Resources/tryPlugs_on_cribs/output_"

            for i in range(1,2):

                fileName = fname + str(i).zfill(2) + ".txt"
                outName = oname + str(i).zfill(2) + ".txt"

                with open(fileName, "r") as f:
                    with open(outName, "w" ) as o:

                        count = 0

                        for line in f:
                            
                            if(count > 5): return
                            count = count+1
                            
                            alpha = "abcdefghijklmnopqrstuvwxyz"
                            cipher = "egcvqcsahlfmctzgwwxikupvunrujaqimbxnwjhkwnxnisjaqbmouylcbxdnvdbvf"

                            line = line.strip()
                            words = line.split()
                            decrypt = words[6]

                            plugs = []
                            lastString = ""
                            us = UniSinkovTest()

                            
                            baseLine = us.computeSinkov(decrypt)

                            #initialize variables to capture current best plug
                            for i in range(5):

                                maxSoFar = baseLine
                                #iterate x from 'A' to 'Y'
                                for x in alpha:

                                    #iterate y from 'X+1' to 'Z'
                                    for y in alpha:
                                            
                                    #re-initialize enigma object with rotors
                                        e = Enigma()
                                        e.setRotors(int(words[0]), int(words[1]), int(words[2]), int(words[3]), int(words[4]), int(words[5]))

                                        #not sure how to iterate through dictionary but I want to set found plugs
                                        for pair in plugs:
                                            e.setSteckerboardPlug(pair[0],pair[1])

                                        #set the current plug
                                        e.setSteckerboardPlug(x, y)

                                        #encrypt the cipher with the plugs, see if it's better, and store
                                        s = e.encryptString(cipher)
                                        score = us.computeSinkov(s)
                                        if (score > maxSoFar):
                                            a = alpha.find(x)
                                            b = alpha.find(y)
                                            maxSoFar = score
                                            best = x + y
                                            lastString = s

                                #add best to plugs
                                plugs.append(best)

                                # remove plugged letters from alphabet
                                alpha = alpha[:a] + alpha[a+1:b] + alpha[b+1:]

                            # write output for this line
                            o.write(
                                str(words[0])+" "+ decrypt + " " + str(plugs) + " " + lastString + "\n"
                            ) 


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
        for x in range(len(input)-2):
            if input[x: x+2] in d:
                d[input[x: x+2]] += 1
            else:
                d[input[x: x+2]] = 1

        if input[-2:] in d:
                d[input[-2:]] += 1
        else:
            d[input[-2:]] = 1
        
        for key in d:
            output += d[key] * (d[key] - 1)
        output /= bigramCount*(bigramCount-1)

        return output

    def indexOfCoincidenceTrigram(self, input: str) -> float:
        trigramCount = len(input) - 2
        output = 0
        d = {}
        for x in range(len(input)-3):
            if input[x: x+3] in d:
                d[input[x: x+3]] += 1
            else:
                d[input[x: x+3]] = 1
        
        if input[-3:] in d:
                d[input[-3:]] += 1
        else:
            d[input[-3:]] = 1

        for key in d:
            output += d[key] * (d[key] - 1)
        output /= trigramCount*(trigramCount-1)

        return output

    
    def sinkovStatisticUnigram(self, input: str) -> float:
        if not LanguageRecognition.UNIGRAM_TABLE_LOADED: self.loadUnigramTable()
        output = 0
        for x in input:
            if x in self.unigramTable:
                output += math.log(self.unigramTable[x])
            else:
                output += math.log(0.001) # less than exp frq for Q
        return output
            
    
    
    def sinkovStatisticBigram(self, input: str) -> float:
        if not LanguageRecognition.BIGRAM_TABLE_LOADED: self.loadBigramTable()
        output = 0
        for x in range(len(input) - 2):
            if input[x:x+2] in LanguageRecognition.bigramTable:
                output += math.log(LanguageRecognition.bigramTable[input[x:x+2]])
            else:
                output += math.log(0.0004) #1/3 of random dist, same proportion as frq(q) to 1/26
        if input[-2:] in LanguageRecognition.bigramTable:
            output += math.log(LanguageRecognition.bigramTable[input[-2:]])
        else:
            output += math.log(0.0004) #1/3 of random dist, 1/26^2,same proportion as frq(q) to 1/26
        return output
                

    
    def sinkovStatisticTrigram(self, input: str) -> float:
        if not LanguageRecognition.TRIGRAM_TABLE_LOADED: self.loadTrigramTable()
        output = 0
        for x in range(len(input) - 3):
            if input[x:x+3] in LanguageRecognition.trigramTable:
                output += math.log(LanguageRecognition.trigramTable[input[x:x+3]])
            else:
                output += math.log(0.0004) #1/3 of random dist, same proportion as frq(q) to 1/26
        if input[-3:] in LanguageRecognition.trigramTable:
            output += math.log(LanguageRecognition.trigramTable[input[-3:]])
        else:
            output += math.log(0.000002) #1/3 of random dist, 1/26^3, same proportion as frq(q) to 1/26
        return output


    def hillClimbing(input: str):
        pass

# program runs from below 
if __name__ == "__main__":
    l = LanguageRecognition()
    
    '''
    l.createUnigramScoring("Resources/Frankenstein.txt")
    l.createBigramScoring("Resources/Frankenstein.txt")
    l.createTrigramScoring("Resources/Frankenstein.txt")
    '''