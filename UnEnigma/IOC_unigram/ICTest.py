import numpy as np
import  time



class ICUnigram:

    def computeIndexOfCoincedence(self, s):

        occurences = {
            'a':0, 'd':0, 'g':0, 'j':0, 'm':0, 'p':0, 's':0, 'v':0, 'y':0, 
            'b':0, 'e':0, 'h':0, 'k':0, 'n':0, 'q':0, 't':0, 'w':0, 'z':0, 
            'c':0, 'f':0, 'i':0, 'l':0, 'o':0, 'r':0, 'u':0, 'x':0 
        }

        numChars = len(s)
        icValue = 0
        
        # Count all the bigrams and put it into the dict
        for i in s:
            occurences[i] = occurences[i] + 1

        # Compute the summation
        for k in occurences.keys():
            icValue = icValue + occurences[k]* (occurences[k] -1 )

        # Normalize by total number of 
        icValue = icValue/ (numChars * (numChars - 1))
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

        with open("IC_uni_output.txt", "w") as file:
            for result in l:
                file.write(str(result[0])+" "+str(result[1]) + "\n")

            
# program runs from below 
if __name__ == "__main__":

    t = time.time()
    l = ICUnigram()
    l.pluglessTest()
    print("time: ", time.time() - t)







