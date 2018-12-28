import random
import numpy as np
import math
import time

# Prebere .txt datoteko dobljeno iz elib.zib.de, kjer so podatki iz TSPLIB - knjiznica z nekaterimi problemi potujocega trgovca in
# optimumi reseni s Concord TSP solverjem. Izbrali smo 3 probleme, in sicer ulysses22.txt, berlin52.txt in kroal100.txt. Vrne
# seznam s koordinatami mest.

# readFile("berlin52.txt")

def readFile(mapa):
    with open(mapa) as lokacije:
        koordinate = []
        i = 0
        for vrstica in lokacije:
            if i < 3:
                i += 1
                continue
            elif i == 3:
                dimenzija = int(vrstica.split()[1])
                i += 1
                continue
            elif i < 6:
                i += 1
                continue
            elif i-6 < dimenzija:
                koordinate.append([float(i) for i in vrstica.split()[1:]])
                i += 1
                continue
    return(koordinate) 

# Mnozica mesto je seznam koordinat mest - (x, y). Fja vrne matriko evklidskih razdalj med mesti.

def mesta(mesta):
    n = len(mesta)
    utezi = np.zeros((n, n))
    
    for i in range(n):
        for j in range(i+1, n):
            utezi[i][j] = ((mesta[i][0] - mesta[j][0])**2 + (mesta[i][1] - mesta[j][1])**2)**(1/2)
            utezi[j][i] = utezi[i][j]
            
    return(utezi)
    
# Vrne najkrajso pot podano v .txt datoteki dobljeni iz TSPLIB.
# ulysses22 [1, 14, 13, 12, 7, 6, 15, 5, 11, 9, 10, 19, 20, 21, 16, 3, 2, 17, 22, 4, 18, 8]
# dolzina = 75.66514947135613
# kroa100 dolzina = 21285.44318157108
# berlin52 dolzina = 7544.365901904087
    
def najkrajsaConcord(najkrajsaPot):
    with open(najkrajsaPot) as mesta:
        koordinate = []
        i = 0
        for vrstica in mesta:
            if i < 3:
                i += 1
                continue
            elif i == 3:
                dimenzija = int(vrstica.split()[2])
                i += 1
                continue
            elif i < 5:
                i += 1
                continue
            elif i-5 < dimenzija:
                koordinate.append(int(vrstica))
                i += 1
                continue
    return(koordinate) 

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

def OX(stars1, stars2):
    dolzina = len(stars1)
    
    rez_a = random.randint(1,len(stars1))
    rez_b = random.randint(rez_a,len(stars1)) #funkcija vzame rez_a in rez_b v odnosu rez_a <= rez_b
    
    ostanek1 = stars2[rez_b:] + stars2[:rez_b]
    for vozl in stars1[rez_a:rez_b]:
        ostanek1.remove(vozl)
    otrok1 = ostanek1[dolzina - rez_b:] + stars1[rez_a:rez_b] + ostanek1[:dolzina - rez_b]
    
    ostanek2 = stars1[rez_b:] + stars1[:rez_b]
    for vozl in stars2[rez_a:rez_b]:
        ostanek2.remove(vozl)
    otrok2 = ostanek2[dolzina - rez_b:] + stars2[rez_a:rez_b] + ostanek2[:dolzina - rez_b]
    
    return(rez_a, rez_b, otrok1, otrok2)



#drugi crossover postopek, vhodna podatka sta dva starša in dva reza c in d
#prvemu otroku prepišemo vrednosti prvega starša med obema rezoma
#vsaka vrednost i iz izreza drugega starša, ki ni v izrezu prvega, dobi svoj istoležeči par v prvem staršu. Če je ta par že vsebovan v izrezu drugega,
#tej vrednosti zopet poiščemo par iz prvega starša in to počnemo dokler dobljeni istoležeči par v drugem staršu ne leži izven izreza. 
#Takrat na njegovo mesto (v drugem staršu) zapišemo vrednost i.
#Na koncu postopka vsa prazna mesta v otroku zapolnimo z istoležečimi vrednostmi iz drugega starša.

def PMX(stars1, stars2):
	l=len(stars1)
	rez_c = random.randint(1,len(stars1))
	rez_d = random.randint(rez_c,len(stars1)) #funkcija vzame rez_c in rez_d v odnosu rez_c <= rez_d
    
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
	return(rez_c, rez_d, otrok1)

#algoritem deluje tudi za robne vrednosti, torej ko je rez_c=0, rez_d=ln oziroma, kadar sta oba reza enaka. 
#problem se pojavi pri definiranju otroka, kot seznam ničel, v primeru da je kateri od elementov v starših ničeln. Ali nas to moti?



#postopek cycle crossover sprejme za vhodne podatke dva starša, ki ju poveže v slovar, starš1 predstavlja ključe, starš2 pa vrednosti.
#najprej poiščemo vse cikle med staršema in ju shranimo v množico A. Nato otroka ustvarimo tako, da na primer prvemu otroku dodamo po vrsti 
#vsak sodi cikel iz prvega starša in vsak lihi iz drugega, pri drugem otroku pa delamo ravno obratno.

def CX(stars1, stars2):
	slovar={key:value for key, value in zip(list(stars1), list(stars2))}
	l=len(stars1)
	otrok1=[0]*l
	otrok2=[0]*l
	cikli=[]
	cikel=[]
	A=[]
	for i in slovar.keys():
		if i not in cikli:
			cikel=[i]
			naslednji=slovar[i]
			while naslednji not in cikel:
				cikel.append(naslednji)
				naslednji=slovar[naslednji]
			A = A + [cikel]
			cikli = cikli + cikel
	for C in A:
		for j in C:
			u=stars1.index(j)
			if A.index(C) % 2==0:
				otrok1[u]=j
				otrok2[u]=stars2[u]
			else:
				otrok2[u]=j
				otrok1[u]=stars2[u]
	return(otrok1, otrok2)

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

def potomci(utezi, populacija, verjMutacije, kTurnir, crossover):
    potomci = {}
    for i in range(int(len(populacija)/2)):
        stars1 = turnir(populacija, kTurnir)
        stars2 = turnir(populacija, kTurnir)
        
        otroka = crossover(stars1, stars2)
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

def ga_tsp(stGeneracij, utezi, populacija, verjMutacije, kTurnir, crossover):
    nasledniki = populacija
    for _ in range(stGeneracij):
        nasledniki = potomci(utezi, nasledniki, verjMutacije, kTurnir, crossover)
    return(najboljsa_pot(nasledniki))

def povprecje(ponovitve, stGeneracij, utezi, populacija, verjMutacije, kTurnir, crossover):
    vsota = 0
    for _ in range(ponovitve):
        vsota += dolzinaPoti(ga_tsp(stGeneracij, utezi, populacija, verjMutacije, kTurnir, crossover), utezi)
    return(vsota/ponovitve)



#funkcija, ki nakljuèno izbere križanje

def nakljucno_krizanje(stars1, stars2):
    R = [OX, PMX, CX]
    return random.choice(R)(stars1, stars2)

##########################################################################################################################################

# =============================================================================
# cene = utezi(5, 100)
# poti = populacija(10, cene)
# k = 4
# mut = 0.02
# p = ga_tsp(1000 , cene, poti, mut, k, OX)
# 
# primer = [[60, 200], [180, 200], [80, 180], [140, 180], [20, 160], [100, 160], [200, 160], [140, 140], [40, 120], [100, 120], [180, 100], [60, 80], [120, 80], [180, 60], [20, 40], [100, 40], [200, 40], [20, 20], [60, 20], [160, 20]]
# ce = mesta(primer)
# #print(dolzinaPoti(ga_tsp(100, ce, po, 0.015, 5, OX), ce))
# #print(povprecje(100, 100, ce, po, 0.015, 5, OX))
# 
# def main():
# 
#     ########## Primerjava velikosti populacije
#     po = populacija(10, ce)
#     print("Povprečna pot 100 ponovitev algoritma na populacij velikosti 10 in čas izvedbe 100 ponovitev:")
#     start_time = time.time()
#     print(povprecje(100, 100, ce, po, 0.015, 5, OX))
#     print("--- %s seconds ---" % (time.time() - start_time))
#     
#     po = populacija(20, ce)
#     print("Povprečna pot 100 ponovitev algoritma na populacij velikosti 20 in čas izvedbe 100 ponovitev:")
#     start_time = time.time()
#     print(povprecje(100, 100, ce, po, 0.015, 5, OX))
#     print("--- %s seconds ---" % (time.time() - start_time))
#     
#     po = populacija(50, ce)
#     print("Povprečna pot 100 ponovitev algoritma na populacij velikosti 50 in čas izvedbe 100 ponovitev:")
#     start_time = time.time()
#     print(povprecje(100, 100, ce, po, 0.015, 5, OX))
#     print("--- %s seconds ---" % (time.time() - start_time))
# 
#     ########### Primerjava crossoverjev
#     print("Povprečna pot 100 ponovitev algoritma na populacij velikosti 10 in čas izvedbe 100 ponovitev pri razlicnih krizanjih")
#     po = populacija(10, ce)
#     print("Urejeno krizanje (OX):")
#     start_time = time.time()
#     print(povprecje(100, 100, ce, po, 0.015, 5, OX))
#     print("--- %s seconds ---" % (time.time() - start_time))
# 
#     po = populacija(10, ce)
#     print("Delno mapirano krizanje (PMX):")
#     start_time = time.time()
#     print(povprecje(100, 100, ce, po, 0.015, 5, PMX))
#     print("--- %s seconds ---" % (time.time() - start_time))
# 
#     po = populacija(10, ce)
#     print("Ciklicno krizanje (CX):")
#     start_time = time.time()
#     print(povprecje(100, 100, ce, po, 0.015, 5, CX))
#     print("--- %s seconds ---" % (time.time() - start_time))
# 
#     print("Povprečna pot 100 ponovitev algoritma na populacij velikosti 20 in čas izvedbe 100 ponovitev pri razlicnih krizanjih")
#     po = populacija(20, ce)
#     print("Urejeno krizanje (OX):")
#     start_time = time.time()
#     print(povprecje(100, 100, ce, po, 0.015, 5, OX))
#     print("--- %s seconds ---" % (time.time() - start_time))
# 
#     po = populacija(20, ce)
#     print("Delno mapirano krizanje (PMX):")
#     start_time = time.time()
#     print(povprecje(100, 100, ce, po, 0.015, 5, PMX))
#     print("--- %s seconds ---" % (time.time() - start_time))
# 
#     po = populacija(20, ce)
#     print("Ciklicno krizanje (CX):")
#     start_time = time.time()
#     print(povprecje(100, 100, ce, po, 0.015, 5, CX))
#     print("--- %s seconds ---" % (time.time() - start_time))
# 
#     
#     print("Povprečna pot 100 ponovitev algoritma na populacij velikosti 50 in čas izvedbe 100 ponovitev pri razlicnih krizanjih")
#     po = populacija(50, ce)
#     print("Urejeno krizanje (OX):")
#     start_time = time.time()
#     print(povprecje(100, 100, ce, po, 0.015, 5, OX))
#     print("--- %s seconds ---" % (time.time() - start_time))
# 
#     po = populacija(50, ce)
#     print("Delno mapirano krizanje (PMX):")
#     start_time = time.time()
#     print(povprecje(100, 100, ce, po, 0.015, 5, PMX))
#     print("--- %s seconds ---" % (time.time() - start_time))
# 
#     po = populacija(50, ce)
#     print("Ciklicno krizanje (CX):")
#     start_time = time.time()
#     print(povprecje(100, 100, ce, po, 0.015, 5, CX))
#     print("--- %s seconds ---" % (time.time() - start_time))
# 
# 
#     ####### Primerjava verjetnosti mutacije
#     
#     print("Povprečna pot 100 ponovitev algoritma na populacij velikosti 10 in čas izvedbe 100 ponovitev pri razlicnih verjetnostih mutacije")
#     #populacija velikosti 10, OX
#     po = populacija(10, ce)
#     print("Verjetnost mutacije 1%:")
#     start_time = time.time()
#     print(povprecje(100, 100, ce, po, 0.01, 5, OX))
#     print("--- %s seconds ---" % (time.time() - start_time))
# 
#     po = populacija(10, ce)
#     print("Verjetnost mutacije 1,5%:")
#     start_time = time.time()
#     print(povprecje(100, 100, ce, po, 0.015, 5, OX))
#     print("--- %s seconds ---" % (time.time() - start_time))
# 
#     po = populacija(10, ce)
#     print("Verjetnost mutacije 2%:")
#     start_time = time.time()
#     print(povprecje(100, 100, ce, po, 0.02, 5, OX))
#     print("--- %s seconds ---" % (time.time() - start_time))
# 
#     #populacije velikosti 10, PMX
#     po = populacija(10, ce)
#     print("Verjetnost mutacije 1%:")
#     start_time = time.time()
#     print(povprecje(100, 100, ce, po, 0.01, 5, PMX))
#     print("--- %s seconds ---" % (time.time() - start_time))
# 
#     po = populacija(10, ce)
#     print("Verjetnost mutacije 1,5%")
#     start_time = time.time()
#     print(povprecje(100, 100, ce, po, 0.015, 5, PMX))
#     print("--- %s seconds ---" % (time.time() - start_time))
# 
#     po = populacija(10, ce)
#     print("Verjetnost mutacije 2%:")
#     start_time = time.time()
#     print(povprecje(100, 100, ce, po, 0.02, 5, PMX))
#     print("--- %s seconds ---" % (time.time() - start_time))
# 
#     #populacija velikosti 10, CX
#     po = populacija(10, ce)
#     print("Verjetnost mutacije 1%:")
#     start_time = time.time()
#     print(povprecje(100, 100, ce, po, 0.01, 5, CX))
#     print("--- %s seconds ---" % (time.time() - start_time))
# 
#     po = populacija(10, ce)
#     print("Verjetnost mutacije 1,5%:")
#     start_time = time.time()
#     print(povprecje(100, 100, ce, po, 0.015, 5, CX))
#     print("--- %s seconds ---" % (time.time() - start_time))
# 
#     po = populacija(10, ce)
#     print("Verjetnost mutacije 2%:")
#     start_time = time.time()
#     print(povprecje(100, 100, ce, po, 0.02, 5, CX))
#     print("--- %s seconds ---" % (time.time() - start_time))
# 
#     
#     #populacije velikosti 20, OX
# 
#     po = populacija(20, ce)
#     print("Verjetnost mutacije 1%:")
#     start_time = time.time()
#     print(povprecje(100, 100, ce, po, 0.01, 5, OX))
#     print("--- %s seconds ---" % (time.time() - start_time))
# 
#     po = populacija(20, ce)
#     print("Verjetnost mutacije 1,5%:")
#     start_time = time.time()
#     print(povprecje(100, 100, ce, po, 0.015, 5, OX))
#     print("--- %s seconds ---" % (time.time() - start_time))
# 
#     po = populacija(20, ce)
#     print("Verjetnost mutacije 2%:")
#     start_time = time.time()
#     print(povprecje(100, 100, ce, po, 0.02, 5, OX))
#     print("--- %s seconds ---" % (time.time() - start_time))
# 
# 
#     #populacije velikosti 20, PMX
# 
#     po = populacija(20, ce)
#     print("Verjetnost mutacije 1%:")
#     start_time = time.time()
#     print(povprecje(100, 100, ce, po, 0.01, 5, PMX))
#     print("--- %s seconds ---" % (time.time() - start_time))
# 
#     po = populacija(20, ce)
#     print("Verjetnost mutacije 1,5%")
#     start_time = time.time()
#     print(povprecje(100, 100, ce, po, 0.015, 5, PMX))
#     print("--- %s seconds ---" % (time.time() - start_time))
# 
#     po = populacija(20, ce)
#     print("Verjetnost mutacije 2%:")
#     start_time = time.time()
#     print(povprecje(100, 100, ce, po, 0.02, 5, PMX))
#     print("--- %s seconds ---" % (time.time() - start_time))
# 
#     #populacija velikosti 20, CX
# 
#     po = populacija(20, ce)
#     print("Verjetnost mutacije 1%:")
#     start_time = time.time()
#     print(povprecje(100, 100, ce, po, 0.01, 5, CX))
#     print("--- %s seconds ---" % (time.time() - start_time))
# 
#     po = populacija(20, ce)
#     print("Verjetnost mutacije 1,5%:")
#     start_time = time.time()
#     print(povprecje(100, 100, ce, po, 0.015, 5, CX))
#     print("--- %s seconds ---" % (time.time() - start_time))
# 
#     po = populacija(20, ce)
#     print("Verjetnost mutacije 2%:")
#     start_time = time.time()
#     print(povprecje(100, 100, ce, po, 0.02, 5, CX))
#     print("--- %s seconds ---" % (time.time() - start_time))
#     
#     #populacije velikosti 50, OX
# 
#     po = populacija(50, ce)
#     print("Verjetnost mutacije 1%:")
#     start_time = time.time()
#     print(povprecje(100, 100, ce, po, 0.01, 5, OX))
#     print("--- %s seconds ---" % (time.time() - start_time))
# 
#     po = populacija(50, ce)
#     print("Verjetnost mutacije 1,5%:")
#     start_time = time.time()
#     print(povprecje(100, 100, ce, po, 0.015, 5, OX))
#     print("--- %s seconds ---" % (time.time() - start_time))
# 
#     po = populacija(50, ce)
#     print("Verjetnost mutacije 2%:")
#     start_time = time.time()
#     print(povprecje(100, 100, ce, po, 0.02, 5, OX))
#     print("--- %s seconds ---" % (time.time() - start_time))
# 
# 
#     #populacije velikosti 50, PMX
# 
#     po = populacija(50, ce)
#     print("Verjetnost mutacije 1%:")
#     start_time = time.time()
#     print(povprecje(100, 100, ce, po, 0.01, 5, PMX))
#     print("--- %s seconds ---" % (time.time() - start_time))
# 
#     po = populacija(50, ce)
#     print("Verjetnost mutacije 1,5%")
#     start_time = time.time()
#     print(povprecje(100, 100, ce, po, 0.015, 5, PMX))
#     print("--- %s seconds ---" % (time.time() - start_time))
# 
#     po = populacija(50, ce)
#     print("Verjetnost mutacije 2%:")
#     start_time = time.time()
#     print(povprecje(100, 100, ce, po, 0.02, 5, PMX))
#     print("--- %s seconds ---" % (time.time() - start_time))
# 
#     #populacija velikosti 50, CX
# 
#     po = populacija(50, ce)
#     print("Verjetnost mutacije 1%:")
#     start_time = time.time()
#     print(povprecje(100, 100, ce, po, 0.01, 5, CX))
#     print("--- %s seconds ---" % (time.time() - start_time))
# 
#     po = populacija(50, ce)
#     print("Verjetnost mutacije 1,5%:")
#     start_time = time.time()
#     print(povprecje(100, 100, ce, po, 0.015, 5, CX))
#     print("--- %s seconds ---" % (time.time() - start_time))
# 
#     po = populacija(50, ce)
#     print("Verjetnost mutacije 2%:")
#     start_time = time.time()
#     print(povprecje(100, 100, ce, po, 0.02, 5, CX))
#     print("--- %s seconds ---" % (time.time() - start_time))
# 
# =============================================================================