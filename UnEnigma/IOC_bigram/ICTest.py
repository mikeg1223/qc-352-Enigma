import numpy as np
import  time



class ICBigram:

    def computeIndexOfCoincedence(self, s):

        occurences = {}
        icValue = 0
        numChars = len(s)

        #Count all the bigrams and put it into the dict
        for i in range(1,len(s)):
            
            biGram = s[i-1] + s[i]
            if biGram in occurences:
                occurences[biGram] = occurences[biGram] + 1
            else:
                occurences[biGram] = 1

        for k in occurences.keys():
            icValue = icValue + occurences[k]*(occurences[k]-1)

        # Normalize by total number of 
        icValue = icValue / (numChars * (numChars - 1))
        return icValue

    def sortFunc(self, arg):
        return arg[1]

    def pluglessTest(self):
        
        l = []

        for count in range(1,57):

            inputFileName = "../../Resources/pluglessResults/pluglessResults_" + str( count ).zfill(2) + ".txt"
            
            with open(inputFileName,"r") as f:

                for line in f:
                    score = 0

                    line = line.strip() #Trim Whitespace if there
                    words = line.split() 

                    '''
                        words[0] = Fast Rotor     words[1] = Fast Rotor Ring 
                        words[2] = Mid rotor      words[3] = Mid rotor ring
                        words[4] = Slow Rotor     words[5] = slow rotor ring
                                        words[6] = decrypt
                    '''
                    score = self.computeIndexOfCoincedence(words[6])

                    rotorConfig = str(words[0]) + str(words[1].zfill(2)) + str(words[2]) + str(words[3].zfill(2)) + str(words[4]) + str(words[5].zfill(2))                    
                    
                    l.append( (rotorConfig, score))

            l.sort(key = lambda x: x[1],reverse=True)
            l = l[:5000]
            print("finished page: ", count)

        with open("IC_bi_output.txt", "w") as file:
            for result in l:
                file.write(str(result[0])+" "+str(result[1]) + "\n")

            


# program runs from below 
if __name__ == "__main__":

    t = time.time()
    l = ICBigram()
    l.pluglessTest()
    print("time: ", time.time() - t)
