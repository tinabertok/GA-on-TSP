#!/usr/bin/env python
# coding: utf-8

# In[1]:


import projektOR as pr
import matplotlib.pyplot as plt


# In[2]:


data = "kroa100.txt"
dataPot = "kroa100opt.txt"
    
lokacije = pr.preberi(data)
razdalje = pr.mesta(lokacije)
najkrajsa = pr.najkrajsaConcord(dataPot)


# In[3]:


pr.dolzinaPoti(najkrajsa, razdalje)
pr.narisi(najkrajsa, lokacije)


# In[4]:


pr.dolzinaPoti(najkrajsa, razdalje)


# Preizkusimo vrednosti različnih parametrov za primer "kroa100", pri crossover metodi OX

# In[5]:


CO = "OX"
k_turnir = 5
verj_mutacije = 0.005


# Zgornji argumenti ostajajo fiksni, menjamo le število generacij (100, 1000) in velikost populacije (20, 100):

# In[6]:


st_generacij = 1000


# In[7]:


pop_velikost = 20
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# In[8]:


pop_velikost = 100
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# In[9]:


st_generacij = 100


# In[10]:


pop_velikost = 20
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# In[11]:


pop_velikost = 100
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# Enak postopek naredimo še za primer "ulysses22":

# In[14]:


data = "ulysses22.txt"
dataPot = "ulysses22opt.txt"
    
lokacije = pr.preberi(data)
razdalje = pr.mestaGeo(lokacije)
najkrajsa = pr.najkrajsaConcord(dataPot)


# In[19]:


pr.narisi(najkrajsa, lokacije)


# In[20]:


pr.dolzinaPoti(najkrajsa, razdalje)


# In[15]:


CO = "OX"
k_turnir = 5
verj_mutacije = 0.005


# In[16]:


st_generacij = 1000


# In[17]:


pop_velikost = 20
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# In[18]:


pop_velikost = 100
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# In[21]:


st_generacij = 100


# In[22]:


pop_velikost = 20
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# In[23]:


pop_velikost = 100
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# Različne parametre preizkusimo tudi na tretjem problemu "berlin52", kjer dodamo še vsa tri možna križanja in algoritme ponavljamo po 20-krat:

# In[24]:


data = "berlin52.txt"
dataPot = "berlin52opt.txt"
    
lokacije = pr.preberi(data)
razdalje = pr.mesta(lokacije)
najkrajsa = pr.najkrajsaConcord(dataPot)


# In[25]:


pr.narisi(najkrajsa, lokacije)


# In[26]:


pr.dolzinaPoti(najkrajsa, razdalje)


# In[27]:


st_ponovitev = 20
k_turnir = 5


# Fiksna v tem primeru ostajata zgornja dva argumenta, spreminjamo pa verjetnost mutacije (0, 0.005, 0.04), velikost populacije (20, 100), število generacij (100, 1000) in vrsto metode križanja (CX, PMX, OX):

# Začnemo z metodo CX:

# In[28]:


CO = "CX"
verj_mutacije = 0
st_generacij = 100


# In[29]:


pop_velikost = 20
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# In[30]:


pop_velikost = 100
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# In[31]:


CO = "CX"
verj_mutacije = 0
st_generacij = 1000


# In[32]:


pop_velikost = 20
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# In[33]:


pop_velikost = 100
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# Verjetnost mutacije spremenimo na 0.005 in postopek ponovimo:

# In[34]:


CO = "CX"
verj_mutacije = 0.005
st_generacij = 100


# In[35]:


pop_velikost = 20
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# In[36]:


pop_velikost = 100
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# In[37]:


CO = "CX"
verj_mutacije = 0.005
st_generacij = 1000


# In[38]:


pop_velikost = 20
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# In[39]:


pop_velikost = 100
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# Vzamemo še tretjo verjetnost mutacije, in sicer 0.04:

# In[40]:


CO = "CX"
verj_mutacije = 0.004
st_generacij = 100


# In[41]:


pop_velikost = 20
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# In[42]:


pop_velikost = 100
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# In[43]:


CO = "CX"
verj_mutacije = 0.004
st_generacij = 1000


# In[44]:


pop_velikost = 20
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# In[45]:


pop_velikost = 100
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# Zaključili smo s preizkušanjem argumentov na metodi CX, kot naslednjo vzemimo PMX:

# In[46]:


CO = "PMX"
verj_mutacije = 0
st_generacij = 100


# In[47]:


pop_velikost = 20
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# In[48]:


pop_velikost = 100
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# In[49]:


CO = "PMX"
verj_mutacije = 0
st_generacij = 1000


# In[50]:


pop_velikost = 20
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# In[51]:


pop_velikost = 100
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# Verjetnost mutacije zopet zamenjamo:

# In[52]:


CO = "PMX"
verj_mutacije = 0.005
st_generacij = 100


# In[53]:


pop_velikost = 20
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# In[54]:


pop_velikost = 100
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# In[55]:


CO = "PMX"
verj_mutacije = 0.005
st_generacij = 1000


# In[56]:


pop_velikost = 20
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# In[57]:


pop_velikost = 100
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# Vzamemo še tretjo verjetnost mutacije:

# In[58]:


CO = "PMX"
verj_mutacije = 0.04
st_generacij = 100


# In[59]:


pop_velikost = 20
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# In[60]:


pop_velikost = 100
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# In[61]:


CO = "PMX"
verj_mutacije = 0.04
st_generacij = 1000


# In[62]:


pop_velikost = 20
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# In[63]:


pop_velikost = 100
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# Celoten postopek ponovimo še na tretji metodi, OX:

# In[64]:


CO = "OX"
verj_mutacije = 0
st_generacij = 100


# In[65]:


pop_velikost = 20
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# In[66]:


pop_velikost = 100
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# In[67]:


CO = "OX"
verj_mutacije = 0
st_generacij = 1000


# In[68]:


pop_velikost = 20
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# In[69]:


pop_velikost = 100
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# Menjamo vrednost mutacije na 0.005:

# In[70]:


CO = "OX"
verj_mutacije = 0.005
st_generacij = 100


# In[71]:


pop_velikost = 20
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# In[72]:


pop_velikost = 100
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# In[73]:


CO = "OX"
verj_mutacije = 0.005
st_generacij = 1000


# In[74]:


pop_velikost = 20
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# In[75]:


pop_velikost = 100
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# Še zadnja verjetnost mutacije:

# In[76]:


CO = "OX"
verj_mutacije = 0.04
st_generacij = 100


# In[77]:


pop_velikost = 20
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# In[78]:


pop_velikost = 100
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# In[79]:


CO = "OX"
verj_mutacije = 0.04
st_generacij = 1000


# In[80]:


pop_velikost = 20
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# In[81]:


pop_velikost = 100
pop = pr.populacija(pop_velikost, razdalje)
rezultat = pr.gaTsp(st_generacij, razdalje, pop, 0.005, k_turnir, CO)
print("Dolžina najkrajše poti: " + str(pr.dolzinaPoti(rezultat, razdalje)))
pr.narisi(rezultat, lokacije)


# In[ ]:




