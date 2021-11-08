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



---

#### 10/31/21

---

I created a set of 10,000 test cases for my enigma to get a sense of how long a decryption would take. The results at this point have an arithmetic mean of 0.014 s. This seems a little too slow, so I will try to improve on this. 

To do:

* Create "quick and dirty" attacks

* Start working on decryptions

* Improve the Enigma Time

  

---

#### 11/1/21

---

Went over python basics with George to aid in his programming. I generated plugless decryptions using my Enigma. An issue was spotted, I have not implemented double stepping so I need to do that for the Enigma. 

To do:

* Create "quick and dirty" attacks

* Start working on decryptions

* Implement double stepping

* Improve the Enigma time

  

---

#### 11/2/21

---

Improved the timing on our decryptions by switching methodologies in the Enigma. Estimated new time to decrypt is 0.002 s. I changed from recreating a hashmap for each letter at every step, to using string manipulations and finding functions. This changed the remapping from O(n) to O(1) on each rotor turn. I also implemented double stepping for the Enigma. The professor mentioned using tricks such as "if we see a q, and the next letter isn't u... toss it"

To do:

* Create "quick and dirty" attacks
* work on decryptions



---

#### 11/3/21

---

Found an error in my implementation of the Enigma... again. I added an extra rotor somehow? I duplicated the 7th rotor and it was taking the index 7 from the 8th rotor so we were gaining the same decryptions twice with "different" rotor settings in the plugless decryptions. I fixed the error. I also ran 10000 trials on the enigma to see it's average speed. Looks like we are operating at 0.0003 s not 0.002 like previously thought. 

To do:

* Create "quick and dirty" attacks
* work on decryptions

---

#### 11/4/21 

----

I  took a break today. I'm so behind on other schoolwork. 

To do:

* Create "quick and dirty" attacks
* work on decryptions



---

#### 11/5/21

---

I met with George and Matin in bayside to discuss our project. George designed a hill climbing algorithm and we will be implementing it soon. We discussed strategy going forward. I made sure to mention the crib the professor gave us again and how we can possibly use it for decryption: if we see a string ending in one of the letters we can consider the other letters steckered. Maybe. There is the possibility that it is steckered going in, out, or both. Three scenarios to consider. 

To do:

* Create "quick and dirty" attacks
* work on decryptions



---

#### 11/6/21

---

George and Matin finished the hill climbing algorithm. We tested it and it found 4 of the 5 proper plugs on a chosen plaintext and key example. I started coding up a test set for the algorithm to get a sense of it's accuracy. I randomly generated 14000 setting for the enigma, and used the communist manifesto as the plaintext. I encrypted sections of the text using the settings. Next is to make the testing function and run it. 

To do:

* Create "quick and dirty" attacks
* work on decryptions
* Create test case function



---

#### 11/7/21

---

I finished the test case algorithm. It ran for several hours since the hill climbing algorithm is very slow. On our set of 14000 settings and plaintext pairs we had a mean of 2.1 correct plugs found. Not great, but, if we accept this as true for all possibilities we can reduce the search space by a factor of 2^13. 26C2 * 24C2 * 22C2 * 20C2 * 18C2  --> 5C2 * 22C2 * 20C2 * 18C2

Something worth noting, is that for many of the cases, even though 2 proper plugs were found, some of the incorrect plugs had 1 end in a proper spot. Can we use this? Maybe we can see the plugs as "proper" and use other methods to test if there is a better end for one side of each plug. 

To do:

* Create "quick and dirty" attacks
* work on decryptions
