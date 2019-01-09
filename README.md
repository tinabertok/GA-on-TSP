# GA on TSP
Applying a genetic algorithm to the traveling salesman problem

## GA 
**Genetski algoritem**  je močno orodje za reševanje NLP problemov in iskanje bližnjih rešitev veliko kombinatoričnih problemov. V GA imamo populacijo možnih rešitev (tj. fenotipi). Vsaka možna rešitev ima množico lastnosti(tj. njeni kromosomi ali genotipi), ki je lahko mutiramo in spreminjamo. Rešitve so ponavadi predstavljeni v binarni obliki niza, se pravi z 0 in 1.  



## SLOVARČEK

* *Populacija* = množica kromosomov(poti)
* *Kromosom* = pot
* *Gen* = povezava 
* *Starši in otroci* = poti


## POSTOPEK 

Na začetku moramo naš problem potujočega trgovca predstaviti z grafom v obliki n x n matrike cen povezav. Graf smo generirali tako, da smo naključno izbrali celoštevilsko ceno povezave.

Nato smo morali definirati ciljno funkcijo oz. fitness function, ki je v našem primeru predstavljala dolžino najcenejše poti.

Naključno smo ustvarili neko začetno populacijo določene velikosti. Vsak element populacije predstavlja neko pot, ki obišče vsa vozlišča grafa. Populacijo smo predstavili s slovarjem, v katerem so ključi poti, vrednosti pa njihove dolžine. 

V nadaljevanju izberemo starše, ki jih damo v paritveni bazen. Za selekcijo imamo dve možnosti, in sicer selekcijo s turnirjem ter proporcionalno selekcijo. 
Paritveni bazen bomo gradili turnirsko. To pomeni, da bomo iz populacije naključno izbrali k kromosomov oz. poti. Naša funkcija (selekcija) nam bo vrnila zmagovalca kot pot z najkrajšo dolžino in pripadajočo dolžino. Torej bomo za n staršev v bazenu imeli n turnirjev. Število kromosomov v turnirju (k) izberemo sami, vendar moramo biti predvidni. Večji kot je k, hitrejša bo konvergenca, kar pa ni nujno dobro. Najboljše starše (tiste, ki so največkrat zmagali) bomo dali v paritveni bazen.

Za ustvarjanje otrok bomo uporabili različna križanja staršev (poti) iz paritvenega bazena. 

Različne variacije crossoverjev: 
* *order crossover* 
* *partially mapped crossover* 
* *cycle crossover*  
* … 

Tako bomo dobili otroke, ki so že izboljšani primeri poti. Da pa ohranjamo diverziteto v populaciji, si moramo med temi otroci izbrati določen procent, ki ga bomo mutirali z SWAP mutacijo (zamenjali bomo dve vozlišči v poti). Vsako vozlišče z neko verjetnostjo mutiramo, torej zamenjamo položaj mutiranega vozlišča z nekim naključnim vozliščem na poti. S tem postopkom se tudi poskušamo izgoniti prehitri konvergenci, ki bi nas lahko vodila do lokalnega, ne pa globalnega optimuma. 


Naš algoritem bomo preizkusili na različnih velikostih populacije in rezultate primerjali. 
Testne grafe, ki jih bomo generirali sami, bomo nato tudi primerjali s tistimi, ki smo jih našli na internetu. 

## LITERATURA:

* C. Blum, A. Roli, Metaheuristics in Combinatorial Optimization: Overview and Conceptual
Comparison, online
* S. Luke, Essentials of Metaheuristics: a set of undergraduate lecture notes, online
* Z. Michalewicz, Genetic algorithms + data structures = evolution programs, Springer. Chapter 9
* Z. Michalewicz, D. B. Fogel, How to solve it: modern heuristics, Springer. Chapter 8
* M. Affenzeller, Genetic algorithms and genetic programming: modern concepts and practical
applications, CRC press. Chapter 8

### DODATNI VIRI
* http://www.obitko.com/tutorials/genetic-algorithms/tsp-example.php
* https://github.com/maoaiz/tsp-genetic-python
* https://towardsdatascience.com/evolution-of-a-salesman-a-complete-genetic-algorithm-tutorial-for-python-6fe5d2b3ca35
* https://gist.github.com/turbofart/3428880
* https://arxiv.org/ftp/arxiv/papers/1203/1203.3097.pdf
* https://hrcak.srce.hr/file/163313
* http://www.mnkjournals.com/ijlrst_files/Download/Vol%201%20Issue%202/303-%20Naveen.pdf
* http://www.iro.umontreal.ca/~dift6751/ga_tsp_tr.pdf
