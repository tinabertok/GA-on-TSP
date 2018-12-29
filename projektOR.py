import random
import numpy as np
import math
import time
import matplotlib.pyplot as plt
from cycler import cycler

plt.rcParams['axes.prop_cycle'] = cycler(color='k')

# Prebere .txt datoteko dobljeno iz elib.zib.de, kjer so podatki iz TSPLIB - knjiznica z nekaterimi problemi potujocega trgovca in
# optimumi reseni s Concord TSP solverjem. Izbrali smo 3 probleme, in sicer ulysses22.txt, berlin52.txt in kroal100.txt. Vrne
# seznam s koordinatami mest.

# readFile("berlin52.txt")

def preberi(mapa):
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
    
# Izracuna razdalje za GEO lokacije. Formula dobljena s strani: https://www.iwr.uni-heidelberg.de/groups/comopt/software/TSPLIB95/TSPFAQ.html

# podatki pri probemu ulysses22 so podani v GEO lokacijah
    
def mestaGeo(mesta):
    n = len(mesta)
    utezi = np.zeros((n, n))
    RRR = 6378.388
    
    for i in range(n):
        deg = int(mesta[i][0])
        m = mesta[i][0] - deg
        mesta[i][0] = math.pi * (deg + 5 * m/3) / 180
        
        deg = int(mesta[i][1])
        m = mesta[i][1] - deg
        mesta[i][1] = math.pi * (deg + 5 * m/3) / 180
     
    for i in range(n): 
        for j in range(i+1, n):
            q1 = math.cos(mesta[i][1] - mesta[j][1])
            q2 = math.cos(mesta[i][0] - mesta[j][0])
            q3 = math.cos(mesta[i][0] + mesta[j][0])
            utezi[i][j] = int(RRR * math.acos(0.5 * ((1 + q1) * q2 - (1 - q1) * q3) ) + 1)
            utezi[j][i] = utezi[i][j]
            
    return(utezi)
    
# Vrne najkrajso pot podano v .txt datoteki dobljeni iz TSPLIB.
# ulysses22 dolzina 7013
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
# Stevilo kromosomov(poti) v turnirju - k -  izberemo sami. Potrebno pazljivo izbrati k. Vecji kot je, hitrejsa je konvergenca (to ni nujno dobro).

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
    
    return(otrok1, otrok2)



#drugi crossover postopek, vhodna podatka sta dva starša
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
	otrok2 = [0]*l
	otrok1[rez_c:rez_d]=izrez1
	otrok2[rez_c:rez_d]=izrez2
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
	
	return(otrok1, otrok2)

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

def potomci(utezi, populacija, verjMutacije, kTurnir, crossover):
    potomci = {}
    for i in range(int(len(populacija)/2)):
        stars1 = turnir(populacija, kTurnir)
        stars2 = turnir(populacija, kTurnir)
        
        if crossover == "OX":
            otroka = OX(stars1, stars2)
        elif crossover == "PMX":
            otroka = PMX(stars1, stars2)
        elif crossover == "CX":
            otroka = CX(stars1, stars2)
        else:
            otroka = nakljucno(stars1, stars2)
        
        otrok1 = mutacija(otroka[0], verjMutacije)
        otrok2 = mutacija(otroka[1], verjMutacije)
        
        potomci[2*i+1] = otrok1, dolzinaPoti(otrok1, utezi)
        potomci[2*(i+1)] = otrok2, dolzinaPoti(otrok2, utezi)
    return(potomci)

# Vrne najkrajso pot izmed danih vozlisc.
def najkrajsaPot(nasledniki):
    minimum = math.inf
    pot = []
    for i in nasledniki:
        if nasledniki[i][1] < minimum:
            minimum = nasledniki[i][1]
            pot = nasledniki[i][0]
            
    return(pot)

# Izvede se genetski algoritem.
def gaTsp(stGeneracij, utezi, populacija, verjMutacije, kTurnir, crossover):
    nasledniki = populacija
    for _ in range(stGeneracij):
        nasledniki = potomci(utezi, nasledniki, verjMutacije, kTurnir, crossover)
    return(najkrajsaPot(nasledniki))

# Narise graf poti.
def narisi(pot, lokacije):
    plt.figure()
    for stMest in range(len(pot)):
        if stMest != 0:
            sedanje = pot[stMest]
            a2, b2 = a1, b1
            a1, b1 = lokacije[sedanje-1][0], lokacije[sedanje-1][1]
            plt.plot([a1, a2], [b1, b2])
        else:
            prejsnje = pot[len(pot)-1]
            sedanje = pot[0]
            a2, b2 = lokacije[prejsnje-1][0], lokacije[prejsnje-1][1]
            a1, b1 = lokacije[sedanje-1][0], lokacije[sedanje-1][1]
            plt.plot([a1, a2], [b1, b2])
        plt.scatter(lokacije[sedanje-1][0], lokacije[sedanje-1][1])
    plt.show()

# Risanje grafov, parameter kGraf doloca, na vsake koliko se narise graf.   
def gaTspGraf(stGeneracij, utezi, populacija, verjMutacije, kTurnir, crossover, kGraf, koordinate):
    nasledniki = populacija
    for i in range(stGeneracij):
        nasledniki = potomci(utezi, nasledniki, verjMutacije, kTurnir, crossover)

        if (i+1)%kGraf == 0:
            plt.figure()
            pot = najkrajsaPot(nasledniki)
            narisi(pot, koordinate)
            
    return(najkrajsaPot(nasledniki))
    
# Pri danih ponovitvah genetskega algoritma izracuna povprecno dobljeno dolzino najkrajse poti. Zraven pa se najkrajso pot v vseh ponovitvah, ter njeno dolzino.

def povprecje(ponovitve, stGeneracij, utezi, populacija, verjMutacije, kTurnir, crossover):
    vsota = 0
    najkrajsaPot = []
    najkrajsaDolzina = math.inf
    
    for _ in range(ponovitve):
        trenutnaPot = gaTsp(stGeneracij, utezi, populacija, verjMutacije, kTurnir, crossover)
        dolzinaTrenutne = dolzinaPoti(trenutnaPot, utezi)
        vsota += dolzinaTrenutne
        
        if dolzinaTrenutne < najkrajsaDolzina:
            najkrajsaDolzina = dolzinaTrenutne
            najkrajsaPot = trenutnaPot

    return([vsota/ponovitve, [najkrajsaPot, najkrajsaDolzina]])

# Nakljucno izbrano krizanje.

def nakljucno(stars1, stars2):
    R = [OX, PMX, CX]
    return random.choice(R)(stars1, stars2)

# ==================================================================================================================================

# zazeni main z ukazom v konzoli: main()
    
def main():

    # primerjava rezultatov pri razlicnih vrednostih parametrov za problem ulysses22
    # ostala primera: berlin52 in kroa100
    
    data = "kroa100.txt"
    dataPot = "kroa100opt.txt"
    
    lokacije = preberi(data)
    razdalje = mesta(lokacije) ## nastavi na mestaGeo ce uporabljas ulysses22
    najkrajsa = najkrajsaConcord(dataPot)
    
    narisi(najkrajsa, lokacije)
    
    print("Najkrajša pot iz datoteke " + data + " je: \n \n" + str(najkrajsa) + "\n\nin njena dolžina je: " + str(dolzinaPoti(najkrajsa, razdalje)) + ". \n")
    
    # OX
    # spremeni vrednost CO na PMX, CX ali nakljucno, da dobis rezultate za ostala krizanja
    
    CO = "OX"
    
    #fiksno
    st_ponovitev = 20
    k_turnir = 5
    
    #spremenljivke
    st_generacij = [50, 200]
    verj_mutacije = [0, 0.015, 0.04]
    pop_velikost = [10, 20, 50]
    
    pop = populacija(100, razdalje)
    rezultat = gaTsp(1000, razdalje, pop, 0.005, k_turnir, "OX")
    narisi(rezultat, lokacije)
    print(dolzinaPoti(rezultat, razdalje))
    
# =============================================================================
#     for g in st_generacij:
#         for v in verj_mutacije:
#             for p in pop_velikost:
#                 print("\n--------------------------------------------------------------\n")
#                 print("Število generacij: " + str(g) + ", verjetnost mutacije: " + str(v) + ", velikost populacije: " + str(p))
#                 pop = populacija(p, razdalje)
#                 start_time = time.time()
#                 rezultat = povprecje(st_ponovitev, g, razdalje, pop, v, k_turnir, CO)
#                 print("Pretečeni čas:\n")
#                 print("--- %s seconds ---" % (time.time() - start_time))
#                 print("\nPovprečna pot v " + str(st_ponovitev) + " ponovitvah algoritma je " + str(rezultat[0]) + ".\n")
#                 print("Dolžina najkrajše najdene poti v " + str(st_ponovitev) + " ponovitvah algoritma je: " + str(rezultat[1][1]) + ".")
# =============================================================================
    
    ## Opazimo, da se z vecanjem stevila generacij in velikosti populacije resitve izboljsujejo. Seveda pa z vecanjem teh parametrov povecujemo
    ## tudi cas, ki ga algoritem potrebuje za izracun. Kar se tice verjetnosti mutacije pa pri vrednosti 0.015 dobimo najboljse rezultate. 
    ## Pomislek: mutacija pomembna, za ohranjanje raznolikosti resitev, vendar pa moramo paziti,da ne mutiramo prevelikega deleza populacije, 
    ## saj s tem izgubljamo nase zgrajene resitve.
    ## Pri - Število generacij: 200, verjetnost mutacije: 0.015, velikost populacije: 50 - je najkrajsa dobljena pot dolga 7087, ce to primerjamo
    ## z optimumo 7013 je to zelo blizu.
    ## Ko podobno testiramo na berlin 52, je dolzina najkrajse poti pri - Število generacij: 200, verjetnost mutacije: 0.015, velikost populacije: 50 - 
    ## enaka 9642, kar je ze bolj oddaljeno od optimuma pri 7544.