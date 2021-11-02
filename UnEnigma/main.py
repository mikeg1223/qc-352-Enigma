from Enigma import Enigma
import time

cipherText = "egcvqcsahlfmctzgwwxikupvunrujaqimbxnwjhkwnxnisjaqbmouylcbxdnvdbvf"

e = Enigma()

e.setRotors(1, 0, 2, 0, 3, 0)

'''
total = 0
for _ in range(10000):
    t = time.time()
    e.encryptString(cipherText)
    total += time.time()-t

total /= 1000

print("average decryption time over 10000 trials:", total)
'''

table = {}
rots = [_+1 for _ in range(8)]
ringPos = [_ for _ in range(26)]

with open("storeDecrypts.txt", 'w') as file:
    for x in rots:
        for y in rots:
            for z in rots:
                for a in ringPos:
                    for b in ringPos:
                        for c in ringPos:
                            e.setRotors(x,a,y,b,z,c)
                            file.write(e.encryptString(cipherText))
                            
