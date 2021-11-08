import BiSinkov
from Enigma import Enigma
from BiSinkov.BiSinkovTest import BiSinkovTest
from UniSinkov.UniSinkovTest import UniSinkovTest
import IOC_bigram
import time

class LanguageRecognition:

    def __init__(self):
        #its empty because thats what the Rock said it should be
        pass

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

# program runs from below 
if __name__ == "__main__":
    start = time.time()
    l = LanguageRecognition()
    #l.tryIOC
    l.tryCribs()
    print(time.time() - start)