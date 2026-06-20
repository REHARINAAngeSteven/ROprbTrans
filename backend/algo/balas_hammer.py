from typing import List, Tuple, Optional
from algo.transport import ProblemeTransport
from algo.utils import deux_plus_petits

Matrix = List[List[float]]


def calculer_max_penalite(p, lignes_actives, colonnes_actives):
    max_penalite = -1
    meilleur_cout = float("inf")
    choix = None

    for i, active in enumerate(lignes_actives):
        if not active:
            continue

        vals = [
            p.couts[i][j]
            for j, ok in enumerate(colonnes_actives)
            if ok
        ]

        if not vals:
            continue

        min1, min2 = deux_plus_petits(vals)
        penalite = float("inf") if min2 == float("inf") else min2 - min1

        if penalite > max_penalite:
            max_penalite = penalite
            meilleur_cout = min1
            choix = ("ligne", i)

    for j, active in enumerate(colonnes_actives):
        if not active:
            continue

        vals = [
            p.couts[i][j]
            for i, ok in enumerate(lignes_actives)
            if ok
        ]

        if not vals:
            continue

        min1, min2 = deux_plus_petits(vals)
        penalite = float("inf") if min2 == float("inf") else min2 - min1

        if penalite > max_penalite:
            max_penalite = penalite
            meilleur_cout = min1
            choix = ("colonne", j)

    return choix


def trouver_min_colonne(p, i, colonnes_actives):
    return min(
        (j for j, ok in enumerate(colonnes_actives) if ok),
        key=lambda j: p.couts[i][j]
    )


def trouver_min_ligne(p, j, lignes_actives):
    return min(
        (i for i, ok in enumerate(lignes_actives) if ok),
        key=lambda i: p.couts[i][j]
    )


def balas_hammer(p):
    p.equilibrer()

    n, m = len(p.couts), len(p.couts[0])
    X = [[0.0] * m for _ in range(n)]

    offre = p.offre[:]
    demande = p.demande[:]

    lignes = [True] * n
    colonnes = [True] * m

    while any(offre) and any(demande):

        choix = calculer_max_penalite(p, lignes, colonnes)
        if choix is None:
            break

        type_, idx = choix

        if type_ == "ligne":
            i = idx
            j = trouver_min_colonne(p, i, colonnes)
        else:
            j = idx
            i = trouver_min_ligne(p, j, lignes)

        q = float(min(offre[i], demande[j]))

        X[i][j] += q
        offre[i] -= q
        demande[j] -= q

        if offre[i] == 0:
            lignes[i] = False
        if demande[j] == 0:
            colonnes[j] = False

    return X