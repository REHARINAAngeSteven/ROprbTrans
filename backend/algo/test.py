"""
Tests unitaires pour le problème de transport.

Deux cas de référence sont utilisés :

1. Cas classique 3 sources / 4 destinations, optimum théorique 743.

    couts = [[19, 30, 50, 10],
             [70, 30, 40, 60],
             [40,  8, 70, 20]]
    offre = [7, 9, 18]
    demande = [5, 8, 7, 14]

2. Cas 4 sources / 6 destinations, optimum théorique 3529
   (vérifié indépendamment par programmation linéaire avec scipy.linprog).

    couts = [[24, 22, 61, 49, 83, 35],
             [23, 39, 78, 28, 65, 42],
             [67, 56, 92, 24, 53, 54],
             [71, 43, 91, 67, 40, 49]]
    offre = [18, 32, 14, 9]
    demande = [9, 11, 28, 6, 14, 5]

Chaque cas sert à valider :
- que Balas-Hammer produit une solution de base réalisable (BFS),
- que Stepping Stone améliore cette solution jusqu'à l'optimum théorique,
- que les contraintes d'offre/demande sont respectées à chaque étape.
"""

import unittest

from algo.transport import ProblemeTransport
from algo.balas_hammer import balas_hammer
from algo.stepping_stone import stepping_stone


def construire_probleme_classique() -> ProblemeTransport:
    """
    Cas 3x4, optimum théorique 743.
    Reconstruit le ProblemeTransport de référence (copies fraîches des
    listes, car balas_hammer/equilibrer mutent l'objet).
    """
    couts = [
        [19, 30, 50, 10],
        [70, 30, 40, 60],
        [40, 8, 70, 20],
    ]
    offre = [7, 9, 18]
    demande = [5, 8, 7, 14]

    return ProblemeTransport(
        couts=[row[:] for row in couts],
        offre=offre[:],
        demande=demande[:],
    )


def construire_probleme_4x6() -> ProblemeTransport:
    """
    Cas 4x6, optimum théorique 3529.
    Offre et demande sont déjà équilibrées (73 = 73).
    """
    couts = [
        [24, 22, 61, 49, 83, 35],
        [23, 39, 78, 28, 65, 42],
        [67, 56, 92, 24, 53, 54],
        [71, 43, 91, 67, 40, 49],
    ]
    offre = [18, 32, 14, 9]
    demande = [9, 11, 28, 6, 14, 5]

    return ProblemeTransport(
        couts=[row[:] for row in couts],
        offre=offre[:],
        demande=demande[:],
    )


class TestBalasHammer(unittest.TestCase):
    """Vérifie que Balas-Hammer produit une solution de base réalisable."""

    def setUp(self):
        self.probleme = construire_probleme_classique()
        self.allocation = balas_hammer(self.probleme)

    def test_respecte_offre(self):
        sommes_lignes = [sum(row) for row in self.allocation]
        self.assertEqual(sommes_lignes, self.probleme.offre)

    def test_respecte_demande(self):
        sommes_colonnes = [sum(col) for col in zip(*self.allocation)]
        self.assertEqual(sommes_colonnes, self.probleme.demande)

    def test_aucune_allocation_negative(self):
        for row in self.allocation:
            for valeur in row:
                self.assertGreaterEqual(valeur, 0)

    def test_cout_coherent(self):
        # Le coût de Balas-Hammer doit être un majorant de l'optimum (743).
        cout = self.probleme.cout_total(self.allocation)
        self.assertGreaterEqual(cout, 743)


class TestSteppingStone(unittest.TestCase):
    """Vérifie que Stepping Stone optimise la solution jusqu'à l'optimum."""

    def setUp(self):
        self.probleme = construire_probleme_classique()
        self.allocation_bh = balas_hammer(self.probleme)
        self.allocation_opt = stepping_stone(
            self.probleme,
            [row[:] for row in self.allocation_bh],
        )

    def test_ameliore_ou_egale_balas_hammer(self):
        cout_bh = self.probleme.cout_total(self.allocation_bh)
        cout_opt = self.probleme.cout_total(self.allocation_opt)
        self.assertLessEqual(cout_opt, cout_bh)

    def test_atteint_optimum_theorique(self):
        cout_opt = self.probleme.cout_total(self.allocation_opt)
        self.assertEqual(cout_opt, 743)

    def test_respecte_offre_apres_optimisation(self):
        sommes_lignes = [sum(row) for row in self.allocation_opt]
        self.assertEqual(sommes_lignes, self.probleme.offre)

    def test_respecte_demande_apres_optimisation(self):
        sommes_colonnes = [sum(col) for col in zip(*self.allocation_opt)]
        self.assertEqual(sommes_colonnes, self.probleme.demande)

    def test_aucune_allocation_negative_apres_optimisation(self):
        for row in self.allocation_opt:
            for valeur in row:
                self.assertGreaterEqual(valeur, 0)

    def test_allocation_optimale_attendue(self):
        # Solution optimale précise trouvée lors de la révision.
        attendu = [
            [5, 0, 0, 2],
            [0, 2, 7, 0],
            [0, 6, 0, 12],
        ]
        self.assertEqual(self.allocation_opt, attendu)


class TestBalasHammer4x6(unittest.TestCase):
    """Cas 4x6 : vérifie que Balas-Hammer produit une solution réalisable."""

    def setUp(self):
        self.probleme = construire_probleme_4x6()
        self.allocation = balas_hammer(self.probleme)

    def test_respecte_offre(self):
        sommes_lignes = [sum(row) for row in self.allocation]
        self.assertEqual(sommes_lignes, self.probleme.offre)

    def test_respecte_demande(self):
        sommes_colonnes = [sum(col) for col in zip(*self.allocation)]
        self.assertEqual(sommes_colonnes, self.probleme.demande)

    def test_aucune_allocation_negative(self):
        for row in self.allocation:
            for valeur in row:
                self.assertGreaterEqual(valeur, 0)

    def test_cout_coherent(self):
        # Le coût de Balas-Hammer doit être un majorant de l'optimum (3529).
        cout = self.probleme.cout_total(self.allocation)
        self.assertGreaterEqual(cout, 3529)


class TestSteppingStone4x6(unittest.TestCase):
    """
    Cas 4x6 : vérifie que Stepping Stone optimise jusqu'à l'optimum.

    L'optimum théorique (3529) a été vérifié indépendamment via
    scipy.optimize.linprog. L'allocation optimale n'est pas unique
    pour ce cas (plusieurs bases optimales existent avec le même coût),
    donc seul le coût total est vérifié, pas l'allocation exacte.
    """

    def setUp(self):
        self.probleme = construire_probleme_4x6()
        self.allocation_bh = balas_hammer(self.probleme)
        self.allocation_opt = stepping_stone(
            self.probleme,
            [row[:] for row in self.allocation_bh],
        )

    def test_ameliore_ou_egale_balas_hammer(self):
        cout_bh = self.probleme.cout_total(self.allocation_bh)
        cout_opt = self.probleme.cout_total(self.allocation_opt)
        self.assertLessEqual(cout_opt, cout_bh)

    def test_atteint_optimum_theorique(self):
        cout_opt = self.probleme.cout_total(self.allocation_opt)
        self.assertEqual(cout_opt, 3529)

    def test_respecte_offre_apres_optimisation(self):
        sommes_lignes = [sum(row) for row in self.allocation_opt]
        self.assertEqual(sommes_lignes, self.probleme.offre)

    def test_respecte_demande_apres_optimisation(self):
        sommes_colonnes = [sum(col) for col in zip(*self.allocation_opt)]
        self.assertEqual(sommes_colonnes, self.probleme.demande)

    def test_aucune_allocation_negative_apres_optimisation(self):
        for row in self.allocation_opt:
            for valeur in row:
                self.assertGreaterEqual(valeur, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)