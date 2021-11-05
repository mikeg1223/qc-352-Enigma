import BiSinkov
from Enigma.Enigma import Enigma
from UniSinkov.UniSinkovTest import UniSinkovTest
import IOC_bigram


class LanguageRecognition:

    def __init__(self):
        self.tryPlugs()

    def tryPlugs(self):

        cipher="egcvqcsahlfmctzgwwxikupvunrujaqimbxnwjhkwnxnisjaqbmouylcbxdnvdbvf"

        
        with open("../Resources/pluglessResults/pluglessResults_" + "01" + ".txt", "r") as f:

            for line in f:
                alpha = "abcdefghijklmnopqrstuvwxyz"

                line = line.strip()
                words = line.split()
                decrypt = words[6]
                plugs = {}
                us = UniSinkovTest()

                #initialize variables to capture current best plug
                for i in range(5):


                    best = [None,None]
                    maxSoFar = us.computeSinkov(decrypt) #wut? - Matin

                    #iterate x from 'A' to 'Y'
                    for x in range(0, len(alpha)-1):

                        #iterate y from 'X+1' to 'Z'
                        for y in range(x+1, len(alpha)):

                        #re-initialize enigma object with rotors
                            e = Enigma()
                            e.setRotors(int(words[0]), int(words[1]), int(words[2]), int(words[3]), int(words[4]), int(words[5]))

                            #not sure how to iterate through dictionary but I want to set found plugs
                            for z in plugs:
                                e.setSteckerboardPlug(plugs[z][0],plugs[z][1])

                            #set the current plug
                            e.setSteckerboardPlug(alpha[x], alpha[y])

                            #encrypt the cipher with the plugs, see if it's better, and store
                            s = e.encryptString(cipher)
                            score = us.computeSinkov(s)
                            if (score > maxSoFar):
                                a = x
                                b = y
                                maxSoFar = score
                                best = (alpha[x], alpha[y])

                    #add best to plugs
                    plugs[i] = best
                    
                    # remove plugged letters from alphabet
                    alpha = alpha.replace(alpha[a], "")
                    alpha = alpha.replace(alpha[b], "")

                #end i loop

                #and then you would store in a new text file the rotor settings, plugs, and updated decrypt
                with open("Output_LanguageRecognition.txt","w") as o:
                    o.write("Plugs are: " + str(plugs) )


# program runs from below 
if __name__ == "__main__":
    l = LanguageRecognition()