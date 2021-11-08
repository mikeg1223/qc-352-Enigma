from Enigma import Enigma
'''
Each file will contain 105,456 possible decrpytions
Write decrpytions in the format:
Rotor1 Ring1 Rotor2 Ring2 Rotor3 Ring3 DECRYPT
'''
def createDecryptFile(filename, x, y, ctext):
    with open(filename, "w") as file:
        for z in range(1,9):
            if z == x or z == y:
                continue
            for a in range(26):
                for b in range(26):
                    for c in range(26):
                        e = Enigma()
                        e.setRotors(x,a,y,b,z,c)
                        file.write(str(x)+" "+str(a)+" "+str(y)+" "+str(b)+" "+str(z)+" "+str(c)+" "+e.encryptString(ctext)+ '\n')



cipherText = "egcvqcsahlfmctzgwwxikupvunrujaqimbxnwjhkwnxnisjaqbmouylcbxdnvdbvf"


'''

fname = "pluglessResults"
ext = ".txt"
currentfile = 0

for x in range(1,9):
    for y in range(1,9):
        if x == y:
            continue
        currentfile += 1
        createDecryptFile(fname+"_"+str(currentfile).zfill(2)+ext, x, y, cipherText)
'''


'''
d = {}

with open("Resources/unplugged_BiSinkov_results.txt", "r") as file:
    for line in file:
        temp = line.split()
        e.setRotors(int(temp[0][0]), int(temp[0][1:3]), int(temp[0][3]), int(temp[0][4:6]), int(temp[0][6]), int(temp[0][7:9]))
        d[temp[0]] = (e.encryptString(cipherText), temp[1])

res = []

for _ in d:
    if d[_][0][-3] =="k" or d[_][0][-2] == "d" or d[_][0][-1] == "b":
        res.append((d[_][0], d[_][1], _)) 

with open("Resources/possibleCribContaining.txt", "w") as file:
    for _ in res:
        file.write(_[2] + " " + _[1] + " " + _[0] + "\n")

'''

'''

res = []

with open("Resources/possibleCribContaining.txt", "r") as file:
    for line in file:
        temp = line.split()
        if (temp[2][-3] == "k" and temp[2][-2] == "d") or (temp[2][-3] == "k" and temp[2][-1] == "b") or (temp[2][-2] == "d" and temp[2][-1] == "b"):
            res.append(line)

with open("Resources/possibleCribContaining2.txt", "w") as file:
    for _ in res:
        file.write(_)
'''



'''
    #This was a method i manually edited 7 times to fill our allKDB_0x.txt files with cribs


fname = "../Resources/pluglessResults/pluglessResults_"
decrypt = ""

def getAllKDB():
    with open("../Resources/all_possible_Crib/allKDB_07.txt", "w") as o:

        count = 0
        for i in range (49,57):

            fileName = fname + str(i).zfill(2) + ".txt"
            with open(fileName, "r") as f:

                for line in f:

                    words = line.split()
                    decrypt = words[6]
                    if( decrypt[62] == "k" or decrypt[63] == "d" or decrypt[64] == "b" ):
                        count = count+1
                        o.write(line)
                        if(count > 100000):
                            print("Done with the page of KDB at this spot:")
                            print("File: " + fileName)
                            print(decrypt)
                            return


getAllKDB()

'''