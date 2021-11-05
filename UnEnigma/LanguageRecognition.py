import BiSinkov
from Enigma.Enigma import Enigma
from BiSinkov.BiSinkovTest import BiSinkovTest
from UniSinkov.UniSinkovTest import UniSinkovTest
import IOC_bigram
import time

class LanguageRecognition:

    def __init__(self):
        self.tryPlugs()

    def tryPlugs(self):


        with open("../Resources/test.txt", "r") as f:

        #with open("../Resources/pluglessResults/pluglessResults_" + "01" + ".txt", "r") as f:
            with open("Output_LanguageRecognition.txt","w") as o:

                for line in f:

                    alpha = "abcdefghijklmnopqrstuvwxyz"

                    line = line.strip()
                    words = line.split()
                    decrypt = words[6]
                    cipher = words[7]

                    plugs = []
                    lastString = ""
                    us = UniSinkovTest()

                    #initialize variables to capture current best plug
                    for i in range(5):

                        maxSoFar = us.computeSinkov(decrypt) 

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
                        str(words[0])+" " + str(words[1])+" "+str(words[2]) + " " + str(words[3]) + " " + str(words[4]) + " " + str(words[5] + " " )
                        + decrypt + " " + str(plugs) + " " + lastString + "\n"
                    ) 

        
                #and then you would store in a new text file the rotor settings, plugs, and updated decrypt


# program runs from below 
if __name__ == "__main__":
    start = time.time()
    l = LanguageRecognition()
    print(time.time() - start)