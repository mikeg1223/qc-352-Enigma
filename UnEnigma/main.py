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

fname = "pluglessResults"
ext = ".txt"
currentfile = 0

for x in range(1,9):
    for y in range(1,9):
        if x == y:
            continue
        currentfile += 1
        createDecryptFile(fname+"_"+str(currentfile).zfill(2)+ext, x, y, cipherText)
        
