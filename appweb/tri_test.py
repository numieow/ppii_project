import recherche as rec

#A lancer depuis la CLI avec la commande "pytest tri_test.py"

# TESTS DE L'IMPLEMENTATION DU TRI INSERTION MODIFIE
#Test basique
def test_tri1():
    res = rec.tri([(19, 4), (1, 2), (5, 3)])
    assert res == [(19, 4), (5, 3), (1, 2)]
def test_tri5():
    res = rec.tri([(0,0), (0,0), (0,0), (0,0)])
    assert res == [(0,0), (0,0), (0,0), (0,0)]
#Test sur liste vide
def test_tri2():
    res = rec.tri([])
    assert res == []
#Montrer la stabilité
def test_tri3():
    res = rec.tri([(1, 12), (1, 8), (1, 1000), (1, 22)])
    assert res == [(1, 12), (1, 8), (1, 1000), (1, 22)]
#Montrer que le deuxième élément n'a pas d'importance
def test_tri4():
    res = rec.tri([(4, 23), (2, 23), (3, 23)])
    assert res == [(4, 23), (3, 23), (2, 23)]
#Sur des plus grandes tailles :
def test_tri6():
    res = rec.tri([(i, 1) for i in range(0, 1001)])
    assert res == [(i, 1) for i in range(1000, -1, -1)]