import random
import numpy as np
import math

# Ustvarimo matriko cen povezav/utezi, kjer za vsak par vozlisc nakljucno izberemo celostevilsko ceno povezave med 0 in maxCena.

def utezi(n, maxCena):
    utezi = np.random.randint(0, maxCena, size=(n, n))
    np.fill_diagonal(utezi, 0)
    return(utezi)

# Izracunamo dolzino dane poti iz cen povezav v matriki utezi.

def dolzinaPoti(pot, utezi):
    dolzina = 0
    for i in range(len(pot) - 1):
        dolzina += utezi.item((pot[i] - 1, pot[i+1] - 1))
    dolzina += utezi.item((pot[len(pot)-1] - 1, pot[0] - 1))
    return(dolzina)

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

# Selekcija s turnirjem. Druga opcija bi bila proporcionalna selekcija.
# Iz populacije izberemo nakljucno k kromosomov/elementov/poti. Funkcija vrne par zmagovalec - pot z najkrajso dolzino - in njeno dolzino.
# Število kromosomov(poti) v turnirju - k -  izberemo sami. Potrebno pazljivo izbrati k. Vecji kot je, hitrejsa je konvergenca (to ni nujno dobro).

# Spremenil, da fja vrne samo pot, ne pa par (pot, dolzina). Ce se spreminjamo nazaj, je potrebno spremeniti kodo tudi v fji potomoci. Gasper

def turnir(populacija, kTurnir):
    vozlisca = list(range(1, len(populacija) + 1))
    random.shuffle(vozlisca)
    izbranci = vozlisca[:kTurnir]
    minimum = math.inf
    pot = []
    
    for i in izbranci:
        if populacija[i][1] < minimum:
            minimum = populacija[i][1]
            pot = populacija[i][0]
            
    return(pot)

# Ordered crossover(OX). Ustvarimo dva potomoca iz dveh starsev z "ordered crossover" metodo križanja.
# a <= b <= len(pot). Stars je neka pot, ki je zmagala na turnirju.
#
# Vsak stars predstavlja neko zaporedje vseh vozlisc. Oba starsa razdelimo na 3 podazporedja: 1. podzaporedje gre od zacetka do vkljucno
# vozlisca na a-tem mestu, 2. od tu naprej do vkljucno b-tega mesta, 3. pa od b+1 mesta naprej do konca. Prvega potomca tvorimo tako, da kopiramo
# 2. podzaporedje prvega starsa na enako pozicijo. Od konca tega podazporedja, torej od b+1 mesta, naprej nadaljujemo z vozlisci drugega starsa,
# v vrstnem redu 3. podzaporedje, 1. podazporedje, 2. podzaporedje. Seveda izkljucimo tista vozlisca, ki so ze vsebovana. Ko pridemo do konca,
# nadaljujemo se od zacetka do a-tega mesta. Enako za drugega potomca, le da vlogi starsev zamenjamo.

def ox(stars1, stars2, rez_a, rez_b):
    dolzina = len(stars1)
    
    ostanek1 = stars2[rez_b:] + stars2[:rez_b]
    for vozl in stars1[rez_a:rez_b]:
        ostanek1.remove(vozl)
    otrok1 = ostanek1[dolzina - rez_b:] + stars1[rez_a:rez_b] + ostanek1[:dolzina - rez_b]
    
    ostanek2 = stars1[rez_b:] + stars1[:rez_b]
    for vozl in stars2[rez_a:rez_b]:
        ostanek2.remove(vozl)
    otrok2 = ostanek2[dolzina - rez_b:] + stars2[rez_a:rez_b] + ostanek2[:dolzina - rez_b]
    
    return(otrok1, otrok2)



#drugi crossover postopek, vhodna podatka sta dva starša in dva reza c in d
#prvemu otroku prepišemo vrednosti prvega starša med obema rezoma
#vsaka vrednost i iz izreza drugega starša, ki ni v izrezu prvega, dobi svoj istoležeči par v prvem staršu. Če je ta par že vsebovan v izrezu drugega,
#tej vrednosti zopet poiščemo par iz prvega starša in to počnemo dokler dobljeni istoležeči par v drugem staršu ne leži izven izreza. 
#Takrat na njegovo mesto (v drugem staršu) zapišemo vrednost i.
#Na koncu postopka vsa prazna mesta v otroku zapolnimo z istoležečimi vrednostmi iz drugega starša.

def PMX(stars1, stars2, rez_c, rez_d):
	l=len(stars1)
	izrez1 = stars1[rez_c:rez_d]
	izrez2 = stars2[rez_c:rez_d]
	otrok1 = [0]*l
	otrok1[rez_c:rez_d]=izrez1
	u=0
	v=0
	for i in izrez2:
		if i not in izrez1:
			u=stars2.index(i)
			par_u=stars1[u]
			while par_u in izrez2:
				v=stars2.index(par_u)
				par_u=stars1[v]
			mesto=stars2.index(par_u)
			otrok1[mesto]=i
	for j in range(l):
		if otrok1[j]==0:
		       otrok1[j]=stars2[j]
	return(otrok1)

#popolnoma enak postopek ponovimo še za pridobitev drugega otroka, pri čemer le zamenjamo oba starša:

def PMX(stars1, stars2, rez_c, rez_d):
	l=len(stars1)
	izrez1 = stars1[rez_c:rez_d]
	izrez2 = stars2[rez_c:rez_d]
	otrok2 = [0]*l
	otrok2[rez_c:rez_d]=izrez2
	u=0
	v=0
	for i in izrez1:
		if i not in izrez2:
			u=stars1.index(i)
			par_u=stars2[u]
			while par_u in izrez1:
				v=stars1.index(par_u)
				par_u=stars2[v]
			mesto=stars1.index(par_u)
			otrok2[mesto]=i
	for j in range(l):
		if otrok2[j]==0:
		       otrok2[j]=stars1[j]
	return(otrok2)

# Vsako vozlisce z verjetnostjo verjMutacije mutiramo - zamenjamo polozaj mutiranega vozlisca in nakljucnega vozlisca na poti.
# S tem ohranjamo raznolikost populacije in se poskusamo izogniti prehitri konvergenci, ki nas lahko vodi blizu lokalnega, ne pa globalnega optimuma.

def mutacija(otrok, verjMutacije):
    for i in range(len(otrok)):
        if random.random() <= verjMutacije:
            j = random.randint(0, len(otrok) - 1)
            otrok[i], otrok[j] = otrok[j], otrok[i]
    return(otrok)

# Ustvarimo naslednjo generacijo tako, da izbiramo po 2 starsa iz populacije, ki ju nato krizamo, da dobimo 2 potomca.
# Oba potomca nato mutiramo. Ponavljamo dokler ni mnozica potomcev enako velika kot populacija.

# Potrebno se je odlociti ali ze izbranega starsa vrnemo v populacijo iz katere izbiramo v novem turnirju ali ne.
# Z drugimi besedami: ali nas moti, da je kak stars izbran veckrat?
# Prav tako moramo razmisliti ali bomo upostevali "elitism" - da se dolocen delez najkrajsih poti v populaciji avtomaticno prenese naprej.

def potomci(utezi, populacija, verjMutacije, rez_a, rez_b, kTurnir):
    potomci = {}
    for i in range(int(len(populacija)/2)):
        stars1 = turnir(populacija, kTurnir)
        stars2 = turnir(populacija, kTurnir)
        
        otroka = ox(stars1, stars2, rez_a, rez_b)
        otrok1 = mutacija(otroka[0], verjMutacije)
        otrok2 = mutacija(otroka[1], verjMutacije)
        
        potomci[2*i+1] = otrok1, dolzinaPoti(otrok1, utezi)
        potomci[2*(i+1)] = otrok2, dolzinaPoti(otrok2, utezi)
    return(potomci)

# Genetski algoritem na problemu potujocega trgovca

# Trenutno fja naredi fiksno v naprej doloceno stevilo ponovitev izbiranje potomcev.
# Potrebno razmisliti tudi o kakem drugem zaustavitvenem kriteriju.


#izbranci so vozlisca, izmed njih izberemo najbolso pot
def najboljsa_pot(nasledniki):
    minimum = math.inf
    pot = []
    for i in nasledniki:
        if nasledniki[i][1] < minimum:
            minimum = nasledniki[i][1]
            pot = nasledniki[i][0]
            
    return(pot)

def ga_tsp(ponovitve, utezi, populacija, verjMutacije, rez_a, rez_b, kTurnir):
    nasledniki = populacija
    for _ in range(ponovitve):
        nasledniki = potomci(utezi, nasledniki, verjMutacije, rez_a, rez_b, kTurnir)
        resitev = najboljsa_pot(nasledniki)
        
    return(resitev)



##########################################################################################################################################

cene = utezi(5, 100)
poti = populacija(10, cene)
k = 4
a= 3
b = 5
mut = 0.02
p = ga_tsp(1000 , cene, poti, mut, a, b, k)
  
