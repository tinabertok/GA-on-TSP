import random
import numpy as np
import math

# Ustvarimo matriko cen povezav/utezi, kjer za vsak par vozlisc nakljucno izberemo celostevilsko ceno povezave med 0 in maxCena.

def utezi(n, maxCena):
    utezi = np.random.randint(0, maxCena, size=(n, n))
    np.fill_diagonal(utezi, 0)
    return(utezi)
    
cene = utezi(5, 100)

# Izracunamo dolzino dane poti iz cen povezav v matriki utezi.

def dolzinaPoti(pot, utezi):
    dolzina = 0
    for i in range(len(pot) - 1):
        dolzina += utezi.item((pot[i] - 1, pot[i+1] - 1))
    dolzina += utezi.item((pot[len(pot)-1] - 1, pot[0] - 1))
    return(dolzina)

pot = list(range(1, len(cene) + 1))
random.shuffle(pot)   
dolzina = dolzinaPoti(pot, cene)

# Nakljucno ustvari zacetno populacijo velikosti popVelikost. Posamezen predstavnik populacije je neka pot med vsemi vozlisci.
# V slovarju imamo vsako pot podano v paru z njeno dolzino. popVelikost izberemo sami.

def populacija(popVelikost, utezi):
    pot = list(range(1, len(utezi) + 1))
    poti = {}

    for i in range(popVelikost):
        random.shuffle(pot)
        dolzina = dolzinaPoti(pot, utezi)
        poti[i+1] = [pot.copy(), dolzina]
        
    return(poti)

poti = populacija(10, cene)

# Selekcija s turnirjem. Druga opcija bi bila proporcionalna selekcija.
# Iz populacije izberemo nakljucno k kromosomov/elementov/poti. Funkcija vrne par zmagovalec - pot z najkrajso dolzino - in njeno dolzino.
# Število kromosomov(poti) v turnirju - k -  izberemo sami. Potrebno pazljivo izbrati k. Vecji kot je, hitrejsa je konvergenca (to ni nujno dobro).

def turnir(pop, k):
    vozlisca = list(range(1, len(pop) + 1))
    random.shuffle(vozlisca)
    izbranci = vozlisca[:k]
    minimum = math.inf
    pot = []
    print(izbranci)
    
    for i in izbranci:
        if pop[i][1] < minimum:
            minimum = pop[i][1]
            pot = pop[i][0]
            
    return([pot, minimum])

stars = turnir(poti, 4)

# Ordered crossover(OX). Ustvarimo dva potomoca iz dveh starsev z "ordered crossover" metodo križanja.
# a <= b <= len(pot). Stars je neka pot, ki je zmagala na turnirju.
#
# Vsak stars predstavlja neko zaporedje vseh vozlisc. Oba starsa razdelimo na 3 podazporedja: 1. podzaporedje gre od zacetka do vkljucno
# vozlisca na a-tem mestu, 2. od tu naprej do vkljucno b-tega mesta, 3. pa od b+1 mesta naprej do konca. Prvega potomca tvorimo tako, da kopiramo
# 2. podzaporedje prvega starsa na enako pozicijo. Od konca tega podazporedja, torej od b+1 mesta, naprej nadaljujemo z vozlisci drugega starsa,
# v vrstnem redu 3. podzaporedje, 1. podazporedje, 2. podzaporedje. Seveda izkljucimo tista vozlisca, ki so ze vsebovana. Ko pridemo do konca,
# nadaljujemo se od zacetka do a-tega mesta. Enako za drugega potomca, le da vlogi starsev zamenjamo.

def ox(stars1, stars2, a, b):
    dolzina = len(stars1)
    
    ostanek1 = stars2[b:] + stars2[:b]
    for vozl in stars1[a:b]:
        ostanek1.remove(vozl)
    otrok1 = ostanek1[dolzina - b:] + stars1[a:b] + ostanek1[:dolzina - b]
    
    ostanek2 = stars1[b:] + stars1[:b]
    for vozl in stars2[a:b]:
        ostanek2.remove(vozl)
    otrok2 = ostanek2[dolzina - b:] + stars2[a:b] + ostanek2[:dolzina - b]
    
    return(otrok1, otrok2)
            
s1 = list(range(8))
s2 = list(range(8))
random.shuffle(s1)
random.shuffle(s2)
a = 3
b = 5
otroka = ox(s1, s2, a, b)

# Vsako vozlisce z verj verjMutacije mutiramo - zamenjamo polozaj mutiranega vozlisca in nakljucnega vozlisca na poti.
# S tem ohranjamo raznolikost populacije in se poskusamo izogniti prehitri konvergenci, ki nas lahko vodi blizu lokalnega, ne pa globalnega optimuma.

def mutacija(otrok, verjMutacije):
    for i in range(len(otrok)):
        if random.random() <= verjMutacije:
            j = random.randint(0, len(otrok) - 1)
            otrok[i], otrok[j] = otrok[j], otrok[i]
    return(otrok)
            
ot = otroka[0]
mut = mutacija(ot.copy(), 0.05)    
    
# Potrebno se je odlociti ali ze izbranega starsa vrnemo v populacijo iz katere izbiramo v novem turnirju ali ne.
# Z drugimi besedami: ali nas moti, da je kak stars izbran veckrat?
 
    
    
    
    


