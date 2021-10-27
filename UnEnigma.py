ciphertext = "egcvqcsahlfmctzgwwxikupvunrujaqimbxnwjhkwnxnisjaqbmouylcbxdnvdbvf"

# This code is based off of Daniel Palloks Enigma Machine
# The link to his work can be found here:
# https://people.physik.hu-berlin.de/~palloks/js/enigma/enigma-u_v20_en.html
# The program is written in Javascript, so this is my rough translation into Python

# Pallok's code allows you to customize the Enigma set up, the model, and various other features
# This program will have the following FIXED features

# Model: M3
# Rotors: AAA

# Declaration of Variables

#These are variables assigned to each object in 
models= 12, ukws= 12, wheels= 42, etws = 3
model = "M3", ukwhash = 108, w1st = 1, wlast=8
walze = []