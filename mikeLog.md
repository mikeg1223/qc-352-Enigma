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

---

#### 10/27/2021

---

Research was done for several hours. We collected 4 papers, and are awaiting arrival of two others.

I read some of the Genetic Algorithm attacks on enigma. I also discusses weaknesses of the Enigma with George for quite a while. I created a proposed UML design for our class architecture, this way we can divide the work on actually building the Enigma. 

Proposed Ideas:

* Use statistical analysis to find which language recognition method is the most efficient. 
* Weight the methods using a the normalization of the results. Use the norm of the vector of all results as the proposed result.

To do:

* Read the rest of the Genetic Algorithms article, and then read the other three. 
* Start implementing the classes in the UML design.

Finished:

* Watch The Imitation Game
* Create a UML design
* Survey existing research



---

#### 10/28/2021 

---

Note from professor: Throw out decryptions' that have strings of illogical formats, like xpv in a row. The key space is less than DES so brute forcing is possible. Ideally we will be looking at thousands of decrypt's by sight. We've been given a crib. What is it?

To do:

* Finish reading the articles.
* Start implementing the UML design
* Find the crib

---

#### 10/29/21

---

We are fairly certain that the crib we have is going to be the word "The" at the start of the message. 

Started working on creating the Rotor and Enigma classes from the UML design. Met up with George and Matin to work in person and chat about the processes for the program. We discussed our attack methods for decryption and shortcuts we can take. 

To do:

* Finish the articles
* Finish the class designs

Finished:

* Find the crib

---

#### 10/30/21 

---

Completed the rotor and enigma classes. They work the same as the applet now. The next step is to start creating the main file which will generate decrypts to allow George and Matin time to work on the Language Recognition software. Still need to discuss "quick and dirty" attacks.

To do:

* Create "quick and dirty" attacks
* Start the main classes processes for generation decryptions\

Finished:

* The Rotor class
* The Enigma class
