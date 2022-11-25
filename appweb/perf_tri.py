import recherche as rec
import matplotlib.pyplot as plt
import time
import numpy as np
import random

#La longeur max de liste à tester
LONG_MAX = 500

#Le nombre de tests effectués à une longueur donnée, pour ensuite moyenner
NB_MOYENNE = 50

def super_liste(n):
    '''Crée un liste de liste, où super[i] contient i+1 éléments.
    Chaque élément de super est une liste d'éléments de la forme (entier, position dans la liste).'''
    super = []
    for i in range(1, n+1):
        liste = [(random.randint(0, 1000), j) for j in range(i)]
        super.append(liste)
    return super

def calc_perf():
    '''Crée une liste temps où temps[i] contient le temps pour trier la liste sup[i].'''
    temps = []
    sup = super_liste(LONG_MAX)
    for liste in sup:
        start = time.perf_counter()
        rec.tri(liste)
        end = time.perf_counter()
        temps.append(end-start)
    return temps

#Contient NB_MOYENNE calc_perf(), que l'on va ensuite moyenner
hyper_perf = [calc_perf() for i in range(NB_MOYENNE)]

def hyper_mean(hyper):
    '''Crée une liste mean telle que mean[i] contient la moyenne de temps pris pour trier
    une liste à i+1 éléments.'''
    mean = []
    for i in range(len(hyper[0])):
        liste = [hyper[j][i] for j in range(len(hyper))]
        mean.append(sum(liste)/len(liste))
    return mean


plt.figure()
title = f"Temps de tri par taille d'entrée (moyennée sur {NB_MOYENNE} essais)"
plt.title(title)
x = [i for i in range(1, LONG_MAX+1)]
y = hyper_mean(hyper_perf)
plt.xlabel("Taille de l'entrée")
plt.ylabel("Temps d'exécution (s)")
plt.plot(x, y)
plt.show()