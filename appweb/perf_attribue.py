import recherche as rec
import string, random
import matplotlib.pyplot as plt
import time
import numpy as np

#projet1 = (1000, 'Nouveau jardin dans Nancy', 1, "Je voudrais que l'on crée un jardin participatif pour les nancéens.")
#projet2 = (1001, 'Plus de poubelles à Nancy', 2, "Il faudrait recycler plus, créons plus de poubelles pour le recyclage.")
#projet3 = (1002, 'Panneaux informatifs pour Nancy', 1, "Pour en apprendre plus sur la ville et son histoire.")
#projet4 = (1003, 'Plantations dans mon immeuble', 2, "Je voudrais que l'on crée un endroit où l'on pourrait planter des légumes avec les gens de mon immeuble")
#liste = [projet1, projet2, projet3, projet4]

#Cette liste contient une liste avec 1 projet, puis une liste avec 2, puis avec 3 puis 4
#liste_croissante = [liste[:i] for i in range(1, len(liste) + 1)]


LONGUEUR = 10                               #Longueur des mots créés
NB_MOTS = 400                               #Nombre de mots créés
alphabet = string.ascii_letters             #Définition de l'alphabet
MOTS_TITRE = 7                              #Nombre de mots dans le titre des projets créés
MOTS_DESC = 20                              #Nombre de mots dans le description des projets créés
NB_PROJETS = 500                            #Nombre de projets aléatoires créés

liste_mots = []
for i in range(NB_MOTS):
    mot = ''.join(random.choice(alphabet) for i in range(LONGUEUR))
    liste_mots.append(mot)
#print(liste_mots)

def crea_proj(n):
    '''Fonction qui va créer des projets avec MOTS_TITRE mots dans le titre et MOTS_DESC dans la description.
    Les mots seront créés aléatoirement, et seront des mots de longueur LONGUEUR.
    Renvoie une liste de n projets créés aléatoirement.'''
    projets = []
    for i in range(n):
        titre = ""
        description = ""
        for j in range(MOTS_TITRE):
            titre += ''.join(random.choice(alphabet) for i in range(LONGUEUR)) + ' '
        for k in range(MOTS_DESC):
            description += ''.join(random.choice(alphabet) for i in range(LONGUEUR)) + ' '
        projets.append((0, titre, 0, description))
    return projets

#Création de la liste de projets aléatoires : 
liste = crea_proj(NB_PROJETS)
liste_croissante = [liste[:i] for i in range(1, len(liste) + 1)]

#On va utiliser la fonction perf_counter() de time pour calculer les temps de calcul

def calc_perf():
    '''Calcule les temps d'exécution de recherche avec les mots de liste_mots, 
    pour toutes les listes de projets de liste_croissante.'''
    temps_tot = []                                  #Cette liste va stocker les NB_PROJETS listes avec les temps d'execution pour 1, 2... NB_PROJETS projets
    for liste in liste_croissante:
        temps = np.zeros(len(liste_mots))           #Cette liste va stocker les temps d'exécution pour chacun des mots de liste_mots
        for i in range(len(liste_mots)):
            start = time.perf_counter()             #Calcul du temps d'exécution
            rec.attribue_notes(liste_mots[i], liste)
            end = time.perf_counter()
            temps[i] = end - start
        temps_tot.append(temps)                     #Ajout du temps dans temps_tot
    return temps_tot


def sup_mean(L_L):
    '''Prends en entrée une liste de listes d'entiers, et renvoie une liste avec 
    la moyenne de chacune des listes d'entiers'''
    moyennes = []
    for liste in L_L:
        moyennes.append(sum(liste)/len(liste))
    return moyennes

#print(sup_mean(calc_perf()))


plt.figure()
title = f"Temps d'attribution de note par taille d'entrée (moyennée sur {NB_MOTS} mots)"
plt.title(title)
x = np.linspace(1, NB_PROJETS, NB_PROJETS)
y = sup_mean(calc_perf())
plt.xlabel("Nombre de projets")
plt.ylabel("Temps d'exécution (s)")
plt.plot(x, y)
plt.show()
