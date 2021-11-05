import numpy as np
import  time

class UniSinkovTest:

    uniGramTable = {}
    numChars = 0
    def __init__(self):
        #blah
        pass


    '''
        This function will read in a line of text and compute the Sinkov Statistic for this string,
        based off our UniGramTable that we created already.

        Parameters:
            string s -- the decrypt candidate 
        Returns:
            sinkov
    '''
    def computeSinkov(self, s):
        sinkov = 0
        for i in range(1,len(s)):
            uni = str( s[i] )
            if  uni in self.uniGramTable:
                sinkov += np.log(self.uniGramTable[uni])
            else:
                sinkov += np.log(1/self.numChars)

        return sinkov


    '''
            This function does 3 things:
                1. reads through the sample textFile
                2. stores the frequencies in the uniGramTable
                3. writes it to an outfile so it can be copy/pasted easily
            
            Parameters:
                - name of the text file

            Returns
                nothing
    ''' 
    def buildUnigramTable(self, textFile):

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

                    for i in range(0, len(line)): # Traverse each unigram

                            # Here, we are filtering the characters out by skipping them
                        currChar = line[i].lower()
                        

                        if(ord(currChar)<97 or ord(currChar)>122 ):
                            continue       

                        
                            #Here, we add this comunination of 2 characters into the unigram frequency count
                        count = count+1

                        if self.uniGramTable.__contains__(currChar): # If this exists in the dictionary already
                            self.uniGramTable[currChar] = self.uniGramTable[currChar]+1   # Increment by 1

                        else:   #Else: this is the first occourence of this unigram
                            self.uniGramTable[currChar] = 1    # Start count at 1


        #Normalize the unigram to obtain its probability
        for k in self.uniGramTable.keys():
            self.uniGramTable[k] = self.uniGramTable[k]/(count)

        self.numChars = count

    def readUnigramTable(self,textFile):

        with open(textFile, "r") as f:

            header = f.readline().strip()

            for line in f:

                line = line.strip()
                words = line.split(" ")

                if len(words) < 2:
                    print(words)
                else:
                    self.uniGramTable[words[0]] = float(words[1])

    '''
        This function outputs the unigram to a nice format into an outputFile
    '''
    def outputUnigramTable(self):

        o = open("sampledUnigramMap.txt","w")
        o.write(str(self.numChars))
        for b in self.uniGramTable:
            o.write ( "\n" + b + " " + str(self.uniGramTable[b]) )    

        o.close()

    def sortFunc(self, arg):
        return arg[1]

    def pluglessTest(self):
        
        #Useful variables if we split the work and designate specific files per computer
        score = 0
        l = []

        for count in range(1,56):
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

        with open("UniSinkov_results.txt", "w") as file:
            for result in l:
                file.write(str(result[0])+" "+str(result[1]) + "\n")


# program runs from below 
if __name__ == "__main__":

    t = time.time()
    l = UniSinkovTest()
    #l.buildUnigramTable("../Resources/sample.txt")
    #l.outputUnigramTable()
    l.readUnigramTable("../../Resources/sampledUnigramMap.txt")
    l.pluglessTest()
    print("time: ", time.time() - t)

