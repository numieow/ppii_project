import recherche as rec

#A lancer depuis la CLI avec la commande "pytest attribue_test.py"

projet1 = (1000, 'Nouveau jardin dans Nancy', 1, "Je voudrais que l'on crée un jardin participatif pour les nancéens.")
projet2 = (1001, 'Plus de poubelles à Nancy', 2, "Il faudrait recycler plus, créons plus de poubelles pour le recyclage.")
projet3 = (1002, 'Panneaux informatifs pour Nancy', 1, "Pour en apprendre plus sur la ville et son histoire.")
projet4 = (1003, 'Plantations dans mon immeuble', 2, "Je voudrais que l'on crée un endroit où l'on pourrait planter des légumes avec les gens de mon immeuble")

liste = [projet1, projet2, projet3, projet4]

# TESTS DE L'ATTRIBUTION DES NOTES
#Le projet 1 ne contient pas du tout le mot 'poubelles'
def test_attribue_notes1():
    res = rec.attribue_notes('poubelles', [projet1])
    assert res == [(0, 0)]
#Le projet 2 contient une fois le mot dans son titre et dans sa description
def test_attribue_notes2():
    res = rec.attribue_notes('poubelles', [projet2])
    assert res == [(36, 0)]
#Test sur une entrée avec plusieurs projets
def test_attribue_notes3():
    res = rec.attribue_notes('poubelles', liste)
    assert res == [(0, 0), (36, 1), (0, 2), (0, 3)]
#Test sur une entrée avec aucun projet
def test_attribue_notes4():
    res = rec.attribue_notes('poubelles', [])
    assert res == []
#Test sur le mot vide
def test_attribue_notes5():
    res = rec.attribue_notes('', liste)
    assert res == [(0, 0), (0, 1), (0, 2), (0, 3)]
#Test sur mot inexistant
def test_attribue_notes6():
    res = rec.attribue_notes('chimerique', liste)
    assert res == [(0, 0), (0, 1), (0, 2), (0, 3)]