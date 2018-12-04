# GA-on-TSP
Applying a genetic algorithm to the traveling salesman problem


GENETSKI ALGORITEM je močno orodje za reševanje NLP problemov in iskanje bližnjih rešitev veliko kombinatoričnih problemov. V GA imamo populacijo možnih rešitev (tj. fenotipi). Vsaka možna rešitev ima množico lastnosti(tj. njeni kromosomi ali genotipi), ki je lahko mutiramo in spreminjamo. Rešitve so ponavadi predstavljeni v binarni obliki niza, se pravi z 0 in 1.  

Evolucija se začne z populacijo slučajno generiranih individualistov, in je iterativni proces, kjer je populacija v vsaki iteraciji poimenovana generacija. V vsaki generaciji, je ocenjen FITNESS vsakega individualista. Fitness je običajno vrednost objektivne funkcije pri reševanju optimizacijskega problema. Bolj primerni individualisti so stohastično izbrani iz trenutne populacije in genom vsakega individualista je modificiran (mutiran), da ustvarijo novo generacijo. Ta nova generacija je nato uporabljena za naslednjo iteracijo algoritma. Ponavadi algoritem določi ali je bilo proizvedenih število maksimalnih generacij proizvedeno, ali če je bil fitness level dosežen za to populacijo. 

GA potrebuje:
* genetsko reprezentacijo zaloga vrednosti rešitev
* fitness funkcijo, ki oceni zalogo vrednosti rešitev (to je funkcija, ki primerja kako blizu je zasnova rešitev dejanskim ciljem)


Glavna lastnost, zaradi katere so te genetske predstavitve priročne je, da se njihovi deli zlahka poravnajo zaradi svoje določene velikosti, kar olajša preproste križne operacije(crossover operations). Lahko se uporabijo tudi spremenljive predstavitve dolžine, v tem primeru pa je izvajanje bolj zapleteno. Drevesne predstavitve se proučujejo v genetskem programiranju in predstavljajo grafične oblike v evolucijskem načrtovanju; v programu za izražanje genov je raziskana mešanica obeh linearnih kromosomov in drevesa.


Imamo populacije z različnim številom kromosomov (npr. 16, 32…). Za te kromosome uporabimo
permutacijsko kodiranje(to je permutacija mest na TSP). TSP rešujemo na povezanem grafu(vsa
vozlišča so povezana med sabo) z evklidskimi povezavami (navadne povezave).
Po brisanju ali dodajanju novega mesta je potrebno ustvariti nove kromosome in ponovno zagnati
celoten genetski algoritem.
Izbiramo lahko crossoverje in tipe mutacij.

Crossover: imamo že podano katere naj uporabimo (OC, PMC, CC,…).

Mutacije :
* Normalna slučajna (nekaj mest je izbranih in zamenjanih)
* Slučajna, ki izboljša (izbrano je par naključnih mest, ki se zamenjajo samo če izboljšajo
situacijo(increase fitness)
* Sistematična, ki izboljša (mesta so izbrana sistematično, zamenjana le, če izboljšajo situacijo(increase fitness)
* Brez mutacije


NAVODILA

Pri problemu TSP moramo upoštevati, da veljavna rešitev predstavla pot v kateri je vsaka lokacija vključena natanko enkrat. Če pot vsebuje eno lokacijo večkrat, ali kakšno lokacijo popolnoma izpusti, potem rešitev ni veljavna. Prav zato mora naš genetski algoritem zadoščati tem pogojem, ki jih dosežemo z mutacijo in križnimi metodami. 

Kromosomi -> urejeni seznami, se pravi poti \
Različne variacije crossoverjev: \
* order crossover \
* partially mapped crossover \ 
* cycle crossover  \
* … \
Različne velikosti populacije \
Nekaj testnih grafov generiramo sami, nekaj jih je na internetu. \

LITERATURA:

* C. Blum, A. Roli, Metaheuristics in Combinatorial Optimization: Overview and Conceptual
Comparison, online
* S. Luke, Essentials of Metaheuristics: a set of undergraduate lecture notes, online
* Z. Michalewicz, Genetic algorithms + data structures = evolution programs, Springer. Chapter 9
* Z. Michalewicz, D. B. Fogel, How to solve it: modern heuristics, Springer. Chapter 8
* M. Affenzeller, Genetic algorithms and genetic programming: modern concepts and practical
applications, CRC press. Chapter 8

DODATNI VIRI
* http://www.obitko.com/tutorials/genetic-algorithms/tsp-example.php
* https://github.com/maoaiz/tsp-genetic-python
* https://towardsdatascience.com/evolution-of-a-salesman-a-complete-genetic-algorithm-tutorial-for-python-6fe5d2b3ca35
* https://gist.github.com/turbofart/3428880
