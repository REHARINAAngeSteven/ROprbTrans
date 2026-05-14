def equilibrer(C, offre, demande):
    offre_sum = sum(offre)
    demande_sum = sum(demande)

    if offre_sum < demande_sum:
        diff = demande_sum - offre_sum
        C.append([0] * len(C[0]))
        offre.append(diff)
    elif offre_sum > demande_sum:
        diff = offre_sum - demande_sum
        for i in range(len(C)):
            C[i].append(0)
        demande.append(diff)

    return C, offre, demande


def deux_plus_petits(vals):
    vals = sorted(vals)
    if len(vals) == 0:
        return float('inf'), float('inf')
    if len(vals) == 1:
        return vals[0], float('inf')
    return vals[0], vals[1]


def calculer_max_penalite(C, lignes_actives, colonnes_actives):
    max_penalite = -1
    choix = None
    meilleur_cout = float('inf')

    # lignes
    for i in range(len(C)):
        if not lignes_actives[i]:
            continue
        vals = [C[i][j] for j in range(len(C[0])) if colonnes_actives[j]]
        if not vals:
            continue
        min1, min2 = deux_plus_petits(vals)
        penalite = float('inf') if min2 == float('inf') else (min2 - min1)

        if penalite > max_penalite or (penalite == max_penalite and min1 < meilleur_cout):
            max_penalite = penalite
            choix = ("ligne", i)
            meilleur_cout = min1

    # colonnes
    for j in range(len(C[0])):
        if not colonnes_actives[j]:
            continue
        vals = [C[i][j] for i in range(len(C)) if lignes_actives[i]]
        if not vals:
            continue
        min1, min2 = deux_plus_petits(vals)
        penalite = float('inf') if min2 == float('inf') else (min2 - min1)

        if penalite > max_penalite or (penalite == max_penalite and min1 < meilleur_cout):
            max_penalite = penalite
            choix = ("colonne", j)
            meilleur_cout = min1

    return choix


def trouver_min_colonne(C, i, colonnes_actives):
    min_val = float('inf')
    j_star = -1
    for j in range(len(C[0])):
        if colonnes_actives[j] and C[i][j] < min_val:
            min_val = C[i][j]
            j_star = j
    return j_star


def trouver_min_ligne(C, j, lignes_actives):
    min_val = float('inf')
    i_star = -1
    for i in range(len(C)):
        if lignes_actives[i] and C[i][j] < min_val:
            min_val = C[i][j]
            i_star = i
    return i_star


def ballas_hammer(C, offre, demande):
    C = [row[:] for row in C]
    offre = offre[:]
    demande = demande[:]

    C, offre, demande = equilibrer(C, offre, demande)

    n = len(C)
    m = len(C[0])

    X = [[0 for _ in range(m)] for _ in range(n)]

    lignes_actives = [True] * n
    colonnes_actives = [True] * m

    while any(o > 0 for o in offre) and any(d > 0 for d in demande):

        choix = calculer_max_penalite(C, lignes_actives, colonnes_actives)
        if choix is None:
            break

        type_, indice = choix

        if type_ == "ligne":
            i = indice
            j = trouver_min_colonne(C, i, colonnes_actives)
        else:
            j = indice
            i = trouver_min_ligne(C, j, lignes_actives)

        q = min(offre[i], demande[j])
        X[i][j] += q

        offre[i] -= q
        demande[j] -= q

        # dégénérescence
        if offre[i] == 0 and demande[j] == 0:
            colonnes_actives[j] = False
        elif offre[i] == 0:
            lignes_actives[i] = False
        elif demande[j] == 0:
            colonnes_actives[j] = False

    return X
def calculer_cout_total(C, X):
    total = 0
    for i in range(len(C)):
        for j in range(len(C[0])):
            total += C[i][j] * X[i][j]
    return total

def get_bases(X):
    bases = []
    for i in range(len(X)):
        for j in range(len(X[0])):
            if X[i][j] > 0:
                bases.append((i, j))
    return bases


def est_base(X, i, j):
    return X[i][j] > 0


def trouver_cycle(X, start):
    n, m = len(X), len(X[0])
    bases = get_bases(X)
    bases.append(start)

    def backtrack(path):
        i, j = path[-1]

        # alterner ligne / colonne
        if len(path) % 2 == 1:
            # chercher même ligne
            for jj in range(m):
                if jj != j and (i, jj) in bases:
                    if (i, jj) == start and len(path) >= 4:
                        return path + [(i, jj)]
                    if (i, jj) not in path:
                        res = backtrack(path + [(i, jj)])
                        if res:
                            return res
        else:
            # chercher même colonne
            for ii in range(n):
                if ii != i and (ii, j) in bases:
                    if (ii, j) == start and len(path) >= 4:
                        return path + [(ii, j)]
                    if (ii, j) not in path:
                        res = backtrack(path + [(ii, j)])
                        if res:
                            return res
        return None

    return backtrack([start])


def calcul_gain(C, cycle):
    gain = 0
    for k, (i, j) in enumerate(cycle[:-1]):
        if k % 2 == 0:
            gain += C[i][j]
        else:
            gain -= C[i][j]
    return gain


def appliquer_cycle(X, cycle):
    # positions à soustraire
    moins = [cycle[k] for k in range(1, len(cycle)-1, 2)]
    theta = min(X[i][j] for i, j in moins)

    for k, (i, j) in enumerate(cycle[:-1]):
        if k % 2 == 0:
            X[i][j] += theta
        else:
            X[i][j] -= theta

    return X


def stepping_stone(C, X):
    n, m = len(X), len(X[0])

    while True:
        best_gain = 0
        best_cycle = None

        for i in range(n):
            for j in range(m):
                if X[i][j] == 0:
                    cycle = trouver_cycle(X, (i, j))
                    if not cycle:
                        continue

                    gain = calcul_gain(C, cycle)

                    if gain < best_gain:
                        best_gain = gain
                        best_cycle = cycle

        if best_cycle is None:
            break

        X = appliquer_cycle(X, best_cycle)

    return X


# =====================
# TEST
# =====================
if __name__ == "__main__":
    C = [
        [24,22 ,61 ,49 ,83 ,35 ],
        [23,39 ,78 ,28 ,65 ,42 ],
        [67,56 ,92 ,24 ,53 ,54 ],
        [71,43 ,91 ,67 ,40 ,49 ]
    ]

    offre = [18,32 ,14,9 ]
    demande = [9,11 ,28 ,6 ,14 ,5 ]

    X = ballas_hammer(C, offre, demande)

    print("Solution initiale :")
    for ligne in X:
        print(ligne)
    Z = calculer_cout_total(C, X)
    print("\nCoût initiale Z =", Z)

    X_opt = stepping_stone(C, X)

    print("\nSolution optimisée :")
    for ligne in X_opt:
        print(ligne)

    Z = calculer_cout_total(C, X_opt)
    print("\nCoût optimal Z =", Z)
