import numpy as np



class BiSinkovTest:

    biGramTable = {}
    numBigrams = 0

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
                words = line.split(' ')   

                for word in words: 
                    for i in range(1, len(word)): # Traverse each bigram

                            # Here, we are filtering the characters out by skipping them

                        prevChar = word[i-1].lower()    
                        currChar = word[i].lower()
                        
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


    '''
        This function outputs the bigram to a nice format into an outputFile
    '''
    def outputBigramTable(self):

        o = open("outputBigramMap.txt","w")
        o.write("{")

        for b in self.biGramTable:
            o.write ( "\n \""+b+"\" : "+ str(self.biGramTable[b]) +",")    

        o.write("\n}")
        o.close()

    def pluglessTest(self):
        
        #Useful variables if we split the work and designate specific files per computer
        numLines = 0
        score = 0
        rotorScore = {}
        topScores = {}

        for count in range(1,2):
            inputFileName = "pluglessResult_" + str( count.zfill(2) ) + ".txt"
            with open(inputFileName,"r") as f:

                l = []


                for line in f:

                    numLines+=1     #Used to normalize the data later
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

        l.sort(key = sortFunc, reverse=True)

        with open( str("unplugged_BiSinkov_results_" + str(count).zfill(2) + ".txt"), "w") as file:
            for result in l[:5000]:
                file.write(l[0]+" "+str(l[1]))


    def sortFunc(arg):
        return arg[1]


    def plugTest(self):

        alphabet = "abcdefghijklmnopqrstuvwxyz"
        count=1

        for count in range(1,53):
            inputFileName = "blah" + str(count) + ".txt"
            f = open(inputFileName,"r")

            for c1 in alphabet:
                for c2 in alphabet:

                    for line in f:
                        line = line.strip() #Trim Whitespace if there

                        '''
                            words[0] = Fast Rotor     words[1] = Fast Rotor Ring 
                            words[2] = Mid rotor      words[3] = Mid rotor ring
                            words[4] = Slow Rotor     words[5] = slow rotor ring
                                            words[6] = decrypt
                        '''

                        words = line.split(" ") 
                        score = self.computeSinkov(words[6])


            





# program runs from below 
if __name__ == "__main__":
    l = BiSinkovTest()
    l.buildBigramTable("sample.txt")
    l.outputBigramTable()
    
    l.runTest()

