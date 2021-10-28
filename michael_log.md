####  10/26/2021

---

Assignment was given. We need to decrypt a message provide by the professor, and encrypted with the German Enigma machine.

Materials:

* 3 out of 8 possible rotors
* 5 different plug positions $\leq$ ((26 C 2) C 5)
* Initial rotor positions of AAA
* Type-B reflector

Current known weaknesses:

* Letters do not map to themselves
* At any given point, there are 13 substitution pairs
* 16 letters go unpermuted.

Possible routes of attack:

* Generate all possible decryptions and use language recognition
* Look at the decrypts sans plug board, there are 16 letters unaffected

I read the Introduction to Cryptography with Coding Theory chapters 2.7 and 14.1. I learned about the popular attack methods, for example: using the starting 6 characters to generate groups of cycles. I learned about the construction of an Enigma Machine, being the rotors, rings, reflector, and plug board. 

To do: 

* Read about Rejewski's attack methods.
* Re-watch the imitation game.
* Start working on the language recognition program.

