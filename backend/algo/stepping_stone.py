"""
Implémentation de la méthode Stepping Stone
pour l'optimisation d'une solution du problème de transport.
"""

from typing import List, Tuple, Optional, Set
from algo.transport import ProblemeTransport

Matrix = List[List[float]]
Position = Tuple[int, int]


# =========================================================
# OUTILS
# =========================================================

def get_bases(allocation: Matrix) -> List[Position]:
    """
    Retourne les cases non nulles (variables de base).
    """
    bases: List[Position] = []

    for i, row in enumerate(allocation):
        for j, value in enumerate(row):
            if value > 0:
                bases.append((i, j))

    return bases


def calcul_gain(couts: Matrix, cycle: List[Position]) -> float:
    """
    Calcule le gain (ou coût réduit) d'un cycle Stepping Stone.
    """
    gain = 0

    for k, (i, j) in enumerate(cycle[:-1]):
        gain += couts[i][j] if k % 2 == 0 else -couts[i][j]

    return gain


# =========================================================
# RECHERCHE DE CYCLE
# =========================================================

def trouver_cycle(
    allocation: Matrix,
    start: Position,
    bases: Set[Position]
) -> Optional[List[Position]]:
    """
    Recherche un cycle fermé valide en alternant lignes/colonnes.
    """

    n = len(allocation)
    m = len(allocation[0])

    def backtrack(path: List[Position]) -> Optional[List[Position]]:
        i, j = path[-1]

        # Étape ligne : on cherche un voisin sur la même ligne i
        if len(path) % 2 == 1:
            for jj in range(m):
                if jj == j:
                    continue

                candidat = (i, jj)

                # Fermeture du cycle : on peut toujours reboucler sur start,
                # même si start n'est pas dans bases (c'est la case vide de départ).
                if candidat == start and len(path) >= 4:
                    return path + [candidat]

                # Sinon, on ne peut continuer que via une autre base,
                # jamais déjà visitée dans le chemin courant.
                if candidat in bases and candidat not in path:
                    result = backtrack(path + [candidat])
                    if result:
                        return result

        # Étape colonne : on cherche un voisin sur la même colonne j
        else:
            for ii in range(n):
                if ii == i:
                    continue

                candidat = (ii, j)

                if candidat == start and len(path) >= 4:
                    return path + [candidat]

                if candidat in bases and candidat not in path:
                    result = backtrack(path + [candidat])
                    if result:
                        return result

        return None

    return backtrack([start])


# =========================================================
# APPLICATION DU CYCLE
# =========================================================

def appliquer_cycle(allocation: Matrix, cycle: List[Position]) -> Matrix:
    """
    Applique une amélioration via cycle Stepping Stone.
    """

    negatif = [
        cycle[k]
        for k in range(1, len(cycle) - 1, 2)
    ]

    theta = min(allocation[i][j] for i, j in negatif)

    for k, (i, j) in enumerate(cycle[:-1]):
        if k % 2 == 0:
            allocation[i][j] += theta
        else:
            allocation[i][j] -= theta

    return allocation


# =========================================================
# ALGORITHME PRINCIPAL
# =========================================================

def stepping_stone(
    probleme: ProblemeTransport,
    allocation: Matrix
) -> Matrix:
    """
    Améliore une solution de transport par Stepping Stone.
    """

    while True:
        best_gain = 0
        best_cycle: Optional[List[Position]] = None

        bases = set(get_bases(allocation))

        for i, row in enumerate(allocation):
            for j, value in enumerate(row):

                # on teste uniquement les cases vides
                if value != 0:
                    continue

                start = (i, j)

                cycle = trouver_cycle(allocation, start, bases)

                if not cycle:
                    continue

                gain = calcul_gain(probleme.couts, cycle)

                if gain < best_gain:
                    best_gain = gain
                    best_cycle = cycle

        # condition d'arrêt
        if best_cycle is None:
            break

        allocation = appliquer_cycle(allocation, best_cycle)

    return allocation