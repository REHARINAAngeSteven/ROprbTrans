"""
Résolution du problème de transport.

Méthodes implémentées :
- Balas-Hammer (solution initiale)
- Stepping Stone (amélioration)

Auteur : Steven
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple, Optional, Set

Position = Tuple[int, int]
Matrix = List[List[int]]

@dataclass
class ProblemeTransport:
    """
    Représente un problème de transport.

    Attributes:
        couts: Matrice des coûts unitaires.
        offre: Quantités disponibles.
        demande: Quantités demandées.
    """

    couts: Matrix
    offre: List[int]
    demande: List[int]

    def __post_init__(self) -> None:
        """Équilibre automatiquement le problème."""
        self.equilibrer()

    def equilibrer(self) -> None:
        """
        Équilibre le problème de transport.

        Ajoute une ligne ou une colonne fictive
        si l'offre totale est différente de la demande totale.
        """
        offre_totale = sum(self.offre)
        demande_totale = sum(self.demande)

        if offre_totale < demande_totale:
            difference = demande_totale - offre_totale
            self.couts.append([0] * len(self.couts[0]))
            self.offre.append(difference)

        elif offre_totale > demande_totale:
            difference = offre_totale - demande_totale

            for ligne in self.couts:
                ligne.append(0)

            self.demande.append(difference)

    @staticmethod
    def deux_plus_petits(valeurs: List[int]) -> Tuple[float, float]:
        """
        Retourne les deux plus petites valeurs.

        Complexité : O(n)
        """
        minimum_1 = float("inf")
        minimum_2 = float("inf")

        for valeur in valeurs:
            if valeur < minimum_1:
                minimum_2 = minimum_1
                minimum_1 = valeur
            elif valeur < minimum_2:
                minimum_2 = valeur

        return minimum_1, minimum_2

    def calculer_max_penalite(
        self,
        lignes_actives: List[bool],
        colonnes_actives: List[bool]
    ) -> Optional[Tuple[str, int]]:
        """
        Calcule la pénalité maximale selon Balas-Hammer.
        """
        max_penalite = -1
        meilleur_cout = float("inf")
        choix = None

        # Analyse des lignes
        for i, active in enumerate(lignes_actives):
            if not active:
                continue

            valeurs = [
                self.couts[i][j]
                for j, active_col in enumerate(colonnes_actives)
                if active_col
            ]

            if not valeurs:
                continue

            min1, min2 = self.deux_plus_petits(valeurs)

            penalite = (
                float("inf")
                if min2 == float("inf")
                else min2 - min1
            )

            if (
                penalite > max_penalite
                or (
                    penalite == max_penalite
                    and min1 < meilleur_cout
                )
            ):
                max_penalite = penalite
                meilleur_cout = min1
                choix = ("ligne", i)

        # Analyse des colonnes
        for j, active in enumerate(colonnes_actives):
            if not active:
                continue

            valeurs = [
                self.couts[i][j]
                for i, active_ligne in enumerate(lignes_actives)
                if active_ligne
            ]

            if not valeurs:
                continue

            min1, min2 = self.deux_plus_petits(valeurs)

            penalite = (
                float("inf")
                if min2 == float("inf")
                else min2 - min1
            )

            if (
                penalite > max_penalite
                or (
                    penalite == max_penalite
                    and min1 < meilleur_cout
                )
            ):
                max_penalite = penalite
                meilleur_cout = min1
                choix = ("colonne", j)

        return choix

    def trouver_min_colonne(
        self,
        ligne: int,
        colonnes_actives: List[bool]
    ) -> int:
        """
        Trouve la colonne active de coût minimal.
        """
        return min(
            (
                j
                for j, active in enumerate(colonnes_actives)
                if active
            ),
            key=lambda j: self.couts[ligne][j],
            default=-1,
        )

    def trouver_min_ligne(
        self,
        colonne: int,
        lignes_actives: List[bool]
    ) -> int:
        """
        Trouve la ligne active de coût minimal.
        """
        return min(
            (
                i
                for i, active in enumerate(lignes_actives)
                if active
            ),
            key=lambda i: self.couts[i][colonne],
            default=-1,
        )

    def balas_hammer(self) -> Matrix:
        """
        Génère une solution initiale par Balas-Hammer.
        """
        nb_lignes = len(self.couts)
        nb_colonnes = len(self.couts[0])

        allocation = [
            [0] * nb_colonnes
            for _ in range(nb_lignes)
        ]

        offre = self.offre.copy()
        demande = self.demande.copy()

        lignes_actives = [True] * nb_lignes
        colonnes_actives = [True] * nb_colonnes

        while (
            any(valeur > 0 for valeur in offre)
            and any(valeur > 0 for valeur in demande)
        ):
            choix = self.calculer_max_penalite(
                lignes_actives,
                colonnes_actives
            )

            if choix is None:
                break

            type_choix, indice = choix

            if type_choix == "ligne":
                ligne = indice
                colonne = self.trouver_min_colonne(
                    ligne,
                    colonnes_actives
                )
            else:
                colonne = indice
                ligne = self.trouver_min_ligne(
                    colonne,
                    lignes_actives
                )

            quantite = min(
                offre[ligne],
                demande[colonne]
            )

            allocation[ligne][colonne] += quantite

            offre[ligne] -= quantite
            demande[colonne] -= quantite

            if offre[ligne] == 0:
                lignes_actives[ligne] = False

            if demande[colonne] == 0:
                colonnes_actives[colonne] = False
        return allocation
    
    def cout_total(self, allocation: Matrix) -> int:
        """
        Calcule le coût total d'une allocation.
        """
        return sum(
            cout * quantite
            for ligne_couts, ligne_alloc in zip(
                self.couts,
                allocation
            )
            for cout, quantite in zip(
                ligne_couts,
                ligne_alloc
            )
        )
