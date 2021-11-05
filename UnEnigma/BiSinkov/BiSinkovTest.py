import numpy as np
import  time



class BiSinkovTest:

    biGramTable = {}
    numBigrams = 0
    numChars = 0
    def __init__(self):
        #blah
        pass


    '''
        This function will read in a line of text and compute the Sinkov Statistic for this string,
        based off our biGramTable that we created already.

        Parameters:
            string s -- the decrypt candidate 
        Returns:
            sinkov
    '''
    def computeSinkov(self, s):
        sinkov = 0
        for i in range(1,len(s)):
            bi = str(s[i] + s[i-1])
            if  bi in self.biGramTable:
                sinkov += np.log(self.biGramTable[bi])
            else:
                sinkov += np.log(1/self.numBigrams)


        return sinkov


    '''
            This function does 3 things:
                1. reads through the sample textFile
                2. stores the frequencies in the biGramTable
                3. writes it to an outfile so it can be copy/pasted easily
            
            Parameters:
                - name of the text file

            Returns
                nothing
    ''' 
    def buildBigramTable(self, textFile):

        count = 0
        with open(textFile, 'r', encoding="utf8") as f:
            for line in f: #For each line in the text file
                
                '''
                    DATA PREP:
                        - strip away the trailing whitespace
                        - split up the line into a list of its words
                        - make sure the characters of each word are of the correct format detailed below
                                - Must be convered to lowercase
                                - Must be [a-z] (ascii 97 to 122)
                '''

                line = line.strip()
                line = line.replace(" ", "")
                for char in line:
                    self.numChars = self.numChars+1
                    for i in range(1, len(line)): # Traverse each bigram

                            # Here, we are filtering the characters out by skipping them

                        prevChar = line[i-1].lower()    
                        currChar = line[i].lower()
                        
                        if(ord(currChar)<97 or ord(currChar)>122 or ord(prevChar)<97 or ord(prevChar)>122):
                            continue       

                        
                            #Here, we add this combination of 2 characters into the bigram frequency count
                        count = count+1
                        biGram = prevChar+currChar 

                        if self.biGramTable.__contains__(biGram): # If this exists in the dictionary already
                            self.biGramTable[biGram] = self.biGramTable[biGram]+1   # Increment by 1

                        else:   #Else: this is the first occourence of this bigram
                            self.biGramTable[biGram] = 1    # Start count at 1


        #Normalize the bigram to obtain its probability
        for k in self.biGramTable.keys():
            self.biGramTable[k] = self.biGramTable[k]/(count)

        self.numBigrams = count

    def readBigramTable(self,textFile):
        with open(textFile, "r") as f:

            header = f.readline().strip().split()
            self.numBigrams = int(header[0]) 
            self.numChars = int(header[1])

            for line in f:
                line = line.strip()
                words = line.split(" ")
                self.biGramTable[words[0]] = float(words[1])

    '''
        This function outputs the bigram to a nice format into an outputFile
    '''
    def outputBigramTable(self):

        o = open("sampledBigramMap.txt","w")
        o.write(str(self.numBigrams) + " " + str(self.numChars))
        for b in self.biGramTable:
            o.write ( "\n" + b + " " + str(self.biGramTable[b]) )    

        o.close()


    def sortFunc(self, arg):
        return arg[1]

    def pluglessTest(self):
        
        #Useful variables if we split the work and designate specific files per computer
        score = 0
        l = []

        for count in range(1,3):

            inputFileName = "../../Resources/pluglessResults/pluglessResults_" + str( count ).zfill(2) + ".txt"
            with open(inputFileName,"r") as f:

                score = 0
                for line in f:

                    line = line.strip() #Trim Whitespace if there
                    words = line.split() 

                    '''
                        words[0] = Fast Rotor     words[1] = Fast Rotor Ring 
                        words[2] = Mid rotor      words[3] = Mid rotor ring
                        words[4] = Slow Rotor     words[5] = slow rotor ring
                                        words[6] = decrypt
                    '''

                    score = self.computeSinkov(words[6])

                    if (score < -575):
                        continue

                    rotorConfig = str(words[0]) + str(words[1].zfill(2)) + str(words[2]) + str(words[3].zfill(2)) + str(words[4]) + str(words[5].zfill(2))                    
                    l.append( (rotorConfig, score))

            l.sort(key = lambda x: x[1], reverse=True)
            l = l[:5000]
            print("finished page: ", count)

        with open("BiSinkov_results.txt", "w") as file:
            for result in l:
                file.write(str(result[0])+" "+str(result[1]) + "\n")


# program runs from below 
if __name__ == "__main__":

    t = time.time()
    l = BiSinkovTest()
    #l.buildBigramTable("../../Resources/sample.txt")
    #l.outputBigramTable()
    l.readBigramTable("../../Resources/sampledBigramMap.txt")
    l.pluglessTest()
    print("time: ", time.time() - t)

