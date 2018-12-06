import numpy as np
import math

# Ustvari matriko cen povezav, kjer za vsak par vozlisc nakljucno izbere ceno povezave med 0 in maxCena.

def utezi(n, maxCena):
    utezi = maxCena * np.random.random_sample((n, n))
    np.fill_diagonal(utezi, 0)
    return(utezi)

# Izracunamo dolzino dane poti iz cen povezav v matriki utezi.
# Ali nas moti, da so nekatere poti sluačjno večkrat izbrane.

def dolzinaPoti(pot, utezi):
    dolzina = 0
    for i in range(len(pot)-1):
        dolzina += utezi.item((pot[i]-1, pot[i+1]-1))
    dolzina += utezi.item((pot[len(pot)-1]-1, pot[0]-1))
    return(dolzina)
  
poskus = np.array([[1, 55, 5], [3, 7, 8], [16, 14, 5]])
p = [2, 1, 3]
c = dolzinaPoti(p, poskus)

# Nakljucno ustvari zacetno populacijo velikosti popVelikost. Posamezen predstavnik populacije je neka pot med vsemi vozlisci.
# Izracuna se dolzine posameznih poti.
# popVelikost izberemo sami.

def populacija(popVelikost, utezi):
    n = len(utezi)
    pot = np.array(range(1, n+1))
    poti = {}
    for i in range(popVelikost):
        np.random.shuffle(pot)
        d = dolzinaPoti(pot, utezi)
        poti[i+1] = [np.copy(pot), d]
    return(poti)

pop = populacija(4, poskus)

# Turniska selekcija. Število kromosomov v turnirju - k izberemo sami.
# Ali nas moti, da izberemo nekatere starše večkrat?

def turnir(pop, k):
    kljuci = np.arange(1, len(pop)+1)
    izbranci = np.random.choice(kljuci, k, replace=False)
    minimum = math.inf
    pot = 0
    print(izbranci)
    for i in izbranci:
        if pop[i][1] < minimum:
            minimum = pop[i][1]
            pot = pop[i][0]
    return([pot, minimum])

t = turnir(pop, 2)

# Seka se za a in za b, a < b <= len(pot). stars 1 je bolie [i1, i2,... , ilen(pot)]

def OX(stars1, stars2, a, b):
    otrok1 = []*len(stars1)
    otrok2 = []*len(stars1)
    otrok1[a, b] = stars1[a, b]
    otrok2[a, b] = stars2[a, b]
    
    
    
    


