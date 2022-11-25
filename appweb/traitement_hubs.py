import sqlite3
import re
import copy as cp


def lst_hubs():
    con = sqlite3.connect('tables.db')
    cur= con.cursor()
    ls=[row for row in cur.execute("SELECT * FROM hub")]
    return ls

#print(lst_hubs())
#hubs de la forme (id_hub, Nom_hub , id_proj_respo, description_hub)


def attribue_notes(mots_cles,hubs=lst_hubs()):
    '''Prend en entrée les/le mot(s) clé(s) utilisé(s) pour recherche un projet sur le site
    ainsi que la liste complète des hubs de la table.
    Si un des mots clés est trouvé dans le titre du hub, on ajoute un nombre de point égal à 3 fois la longueur du mot.
    Si un des mots clés est trouvé dans la description du hub, on ajoute un nombre de point égal à 3 fois la longueur du mot.
    Si un des mots clés est trouvé dans le titre d'un projet membre, on ajoute un nombre de point égal à 3 fois la longueur du mot.
    Si un des mots clés est trouvé dans la description d'un projet membre, on ajoute un nombre de point égal à la longueur du mot.
    Renvoie une liste sous la forme (note, indice du hub dans hubs).'''
    a_chercher=re.split('\s', mots_cles)                            #à partir de ce qui est tapé dans la barre de recherche on définit les mots a chercher
    n=len(hubs)
    notes=[]
    con = sqlite3.connect('tables.db')
    cur= con.cursor()
    for i in range(n):                                              #Pour chaque hub
        tot=0                                                       #on créé un note égale à 0
        for mot in a_chercher:                                      #en cherchant chaque mot clé
            for ele in hubs[i][1].split(" "):                    #dans le titre du hub (pondération 5*taille_du_mot)
                if mot in ele :
                    tot+=5*len(mot)
            for ele in hubs[i][3].split(" "):                    #dans la description du hub (pondération 3*taille_du_mot)
                if mot in ele :                                     
                    tot+=3*len(mot)        
            liste_id_proj_du_hub = [row for row in cur.execute('SELECT id_membre FROM membre_hub WHERE id_hub=?',(hubs[i][0],))]	#Liste des id des projets membres
            liste_proj_du_hub=[]
            for id_proj in liste_id_proj_du_hub:
                projet=[row for row in cur.execute("SELECT * FROM projets WHERE id_projet = ?", [id_proj[0]])][0]
                liste_proj_du_hub.append(projet)
            for ele in liste_proj_du_hub[i][1].split(" "):                    #dans le titre d'un membre (pondération 3*taille_du_mot)
                if mot in ele :
                    tot+=3*len(mot)
            for ele in liste_proj_du_hub[i][3].split(" "):                    #dans la description d'un membre (pondération 1*taille_du_mot)
                if mot in ele :                                     
                    tot+=len(mot) 

        notes.append((tot,i))
    return notes

#Coefficients : titre du hub x5 description hub x3 titre projet x3 desc projet x1


def tri(liste):
    '''La liste en entrée est de la forme (note, indice dans la liste des hubs).
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
def liste_ordonne(mots_cles,hubs=lst_hubs()):
    '''Prend en entré le/les mot(s) clé(s) utilisé(s) pour rechercher un projet sur le site, 
    ainsi que la liste complète des hubs de la table.
    Attribue les notes dans la liste notes et applique un tri sur cette liste.
    Renvoie la liste des id_hub, triée selon les notes décroissantes.'''
    lst=[]
    notes=attribue_notes(mots_cles,hubs)
    final=[]
    for i in tri(notes):
        final.append(hubs[i[1]][0])
    return final


def recherche(mots_cles,hubs):
    '''Prend en entré le/les mot(s) clé(s) utilisé(s) pour rechercher un projet sur le site,  
    ainsi que la liste complète des hubs de la table.
    Renvoie la liste des id_hubs, triée selon les notes décroissantes.'''
    return liste_ordonne(mots_cles,hubs)

#print(recherche("poubelle",lst_hubs()))




def filtrage_mot_cles(list_mots_cles):
    """prend en entré une liste de mots-clés de la table mots-clés
    selectionne les hubs pour lesquels tous les mots clés est présents pour plus de la moitié des projets membres
    renvoie la liste de ces hubs """
    resultat=[]
    con = sqlite3.connect('tables.db')
    cur= con.cursor()
    for hub in lst_hubs() :
        lst_id_membres=[row[0] for row in cur.execute("SELECT id_membre FROM membre_hub WHERE id_hub=?",[hub[0]])]
        moitie=int(len(lst_id_membres)//2)
        dico=dict(zip(list_mots_cles,[0 for i in list_mots_cles]))
        for proj in lst_id_membres:
            lst_mots_associes=[row[0] for row in cur.execute("SELECT motcle FROM motscles WHERE projet=?",[proj])]
            for mot in lst_mots_associes :
                if mot in list_mots_cles:
                    dico[mot]+=1
        mots_du_hub=[bool(ele[1]>=moitie) for ele in dico.items()]
        if (not (False in mots_du_hub)):
            resultat.append(hub)
    return resultat
        #les éléments de resultat sont de la forme (id_hub, Nom_hub , id_proj_respo, description_hub)

#print(filtrage_mot_cles(['Environnement']))
#print(filtrage_mot_cles(['test']))