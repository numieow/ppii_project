import recherche as rec

#A lancer depuis la CLI avec la commande "pytest tri_attru_test.py"


projet1 = (1000, 'Nouveau jardin dans Nancy', 1, "Je voudrais que l'on crée un jardin participatif pour les nancéens.")
projet2 = (1001, 'Plus de poubelles à Nancy', 2, "Il faudrait recycler plus, créons plus de poubelles pour le recyclage.")
projet3 = (1002, 'Panneaux informatifs pour Nancy', 1, "Pour en apprendre plus sur la ville et son histoire.")
projet4 = (1003, 'Plantations dans mon immeuble', 2, "Je voudrais que l'on crée un endroit où l'on pourrait planter des légumes avec les gens de mon immeuble")

liste = [projet1, projet2, projet3, projet4]

#TESTS DU TRI DE L'ATTRIBUTION DES NOTES
#Test avec un mot
def test_tri_attri1():
    res = rec.recherche('poubelles', liste)
    assert res == [1001, 1000, 1002, 1003]
#Test avec le mot vide
def test_tri_attri2():
    res = rec.recherche('', liste)
    assert res == [1000, 1001, 1002, 1003]
#Test avec un mot absent des descriptions
def test_tri_attri3():
    res = rec.recherche('chimérique', liste)
    assert res == [1000, 1001, 1002, 1003]
#Test avec 2 mots
def test_tri_attri4():
    res = rec.recherche('mon immeuble', liste)
    assert res == [1003, 1000, 1001, 1002]
#Test avec une liste vide de projets
def test_tri_attri5():
    res = rec.recherche('panneau', [])
    assert res == []
