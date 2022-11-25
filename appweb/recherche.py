import sqlite3
import re
import copy as cp


def lst_proj(cle=""):
    con = sqlite3.connect('tables.db')
    cur= con.cursor()
    if cle == "":
        ls=[row for row in cur.execute("SELECT * FROM projets")]
    else:  
        ls=[row for row in cur.execute("SELECT * FROM projets p JOIN motscles mc ON p.id_projet = mc.projet WHERE mc.motcle = ?", [cle])]
    return ls

#print(lst_proj())
#Projets dlf liste de (id_projet,nom,proprio,description)


def attribue_notes(mots_cles,projets=lst_proj()):
    '''Prend en entrée les/le mot(s) clé(s) utilisé(s) pour recherche un projet sur le site
    ainsi que la liste complète des projets de la table.
    Si un des mots clés est trouvé dans le titre du projet, on ajoute un nombre de point égal à 3 fois la longueur du mot.
    Si un des mots clés est trouvé dans la description du projet, on ajoute un nombre de point égal à la longueur du mot.
    Renvoie une liste sous la forme (note, indice du projet dans projets).'''
    m_cles=mots_cles.lower()
    a_chercher=re.split('\s', m_cles)                            #à partir de ce qui est tapé dans la barre de recherche on définit les mots a chercher
    n=len(projets)
    notes=[]
    for i in range(n):                                              #Pour chaque projet
        tot=0                                                       #on créé un note égale à 0
        for mot in a_chercher:                                      #en cherchant chaque mot clé
            for ele in projets[i][1].split(" "):                    #dans le titre (pondération 3*taille_du_mot)
                if mot in ele.lower() :
                    tot+=3*len(mot)
            for ele in projets[i][3].split(" "):                    #dans la description (pondération 1*taille_du_mot)
                if mot in ele.lower() :                                     
                    tot+=len(mot)                                       
        notes.append((tot,i))
    return notes

#def tri(liste):  
#    '''La liste en entrée est de la forme (note, indice dans la liste des projets).
#    Applique un tri dérivé du tri insertion suivant la valeur des notes.
#    Renvoie la liste triée selon le premier élément des tuples.'''
#    var= cp.copy(liste)
#    trie=[]
#    while var != [] :
#        max=(-1,None)
#        for i in var :
#            if i[0] > max[0] :
#                max = i
#        trie.append(max)
#        var.remove(max)
#    return trie

def tri(liste):
    '''La liste en entrée est de la forme (note, indice dans la liste des projets).
    Applique un tri dérivé du tri fusion suivant la valeur des notes.
    Renvoie la liste triée selon le premier élément des tuples.'''
    def fusion(l1,l2):
        res=[]
        while l1!=[] and l2!=[]:
            if l1[0][0]>l2[0][0]:
                res.append(l1[0])
                l1=l1[1:]
            else:
                res.append(l2[0])
                l2=l2[1:]
        return res+l1+l2
    if len(liste)<=1:
        return liste
    l1=liste[len(liste)//2:]
    l2=liste[:len(liste)//2]
    return fusion(tri(l1),tri(l2))

#print(tri([(1,),(2,),(3,),(4,),(5,),(6,),(7,)]))
#print(tri([(1,),(1,),(1,),(2,),(1,)]))
#print(tri([(5,),(4,)]))
def liste_ordonne(mots_cles,projets=lst_proj()):
    '''Prend en entré le/les mot(s) clé(s) utilisé(s) pour rechercher un projet sur le site, 
    ainsi que la liste complète des projets de la table.
    Attribue les notes dans la liste notes et applique un tri sur cette liste.
    Renvoie la liste des id_projets, triée selon les notes décroissantes.'''
    lst=[]
    m_cles=mots_cles.lower()
    notes=attribue_notes(m_cles,projets)
    final=[]
    for i in tri(notes):
        final.append(projets[i[1]][0])
    return final


def recherche(mots_cles,projets=lst_proj()):
    '''Prend en entré le/les mot(s) clé(s) utilisé(s) pour rechercher un projet sur le site, 
    ainsi que la liste complète des projets de la table.
    Renvoie la liste des id_projets, triée selon les notes décroissantes.'''
    m_cles=mots_cles.lower()
    return liste_ordonne(m_cles,projets)


#print(liste_ordonne("poubelles reyclage jardin",lst_proj()))
#print(recherche("poubelle",lst_proj()))