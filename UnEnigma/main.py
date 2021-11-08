from Enigma import Enigma
import time

from Tests.plugDetectorTests import testCases as tcs
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
e = Enigma()
d = {}

with open("Resources/unplugged_IOC_unigram_results.txt", "r") as file:
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

if __name__ == "__main__":
    e = Enigma()
    tc = tcs()

    '''with open("UnEnigma/Tests/ourFuture.txt", "r") as file:
        for line in file:
            with open("UnEnigma/Tests/testPairs.txt", "a") as file2:
                t.generateSettingsFile(line.strip(), e, file2)
   '''
    res = 0
    t = None
    with open("UnEnigma/Tests/testPairs.txt", "r") as file:
        t = time.time()
        res = tc.runTrials(e, file)
        print("time elapsed (s): ", time.time() - t)

    print(res)
    