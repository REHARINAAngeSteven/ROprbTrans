# Projet : Optimisation du Problème de Transport

Ce projet implémente en Python des algorithmes classiques de **recherche opérationnelle** pour résoudre un **problème de transport** :

1. Génération d’une solution initiale avec la méthode **Balas-Hammer**
2. Optimisation de cette solution avec la méthode **Stepping Stone**

---

## Objectif

Le programme cherche à minimiser le coût total de transport entre plusieurs sources (offres) et destinations (demandes), à partir :

* d’une matrice de coûts,
* des quantités disponibles,
* des quantités demandées.

---

# Fonctionnalités

## Équilibrage du problème

La fonction `equilibrer()` vérifie si :

```text
Somme des offres = Somme des demandes
```

Si ce n’est pas le cas :

* une ligne fictive est ajoutée si l’offre est insuffisante,
* une colonne fictive est ajoutée si la demande est insuffisante.

Les coûts fictifs sont fixés à `0`.

---

## Méthode Balas-Hammer

La fonction `ballas_hammer()` génère une solution initiale en utilisant :

* les pénalités de lignes et colonnes,
* la sélection du coût minimal,
* l’allocation maximale possible à chaque étape.

### Étapes principales

1. Calcul des pénalités
2. Sélection de la ligne/colonne la plus pénalisante
3. Choix de la cellule au coût minimal
4. Allocation des quantités
5. Désactivation des lignes/colonnes saturées

---

## Calcul du coût total

La fonction `calculer_cout_total()` calcule :

```text
Coût total = Σ (coût × quantité transportée)
```

---

## Optimisation Stepping Stone

La méthode `stepping_stone()` améliore la solution initiale :

* recherche des cycles d’amélioration,
* calcul des gains potentiels,
* réallocation des quantités,
* réduction du coût total.

### Fonctions associées

* `trouver_cycle()` : détection des cycles
* `calcul_gain()` : évaluation du gain
* `appliquer_cycle()` : mise à jour de la solution

---

# Structure du projet

```Premier ebauche du projet
.
├── ballas_hammer.py
└── README.md
```

---

# Exemple de données

```python
C = [
    [24,22,61,49,83,35],
    [23,39,78,28,65,42],
    [67,56,92,24,53,54],
    [71,43,91,67,40,49]
]

offre = [18,32,14,9]

demande = [9,11,28,6,14,5]
```

---

# Exemple d’exécution

## Solution initiale

Le programme affiche :

```text
Solution initiale :
[...]
```

## Coût initial

```text
Coût initial Z = ...
```

## Solution optimisée

```text
Solution optimisée :
[...]
```

## Coût optimal

```text
Coût optimal Z = ...
```

---

# Algorithmes utilisés

* Méthode de Balas-Hammer
* Méthode Stepping Stone
* Recherche de cycles
* Optimisation des coûts de transport

---

# Technologies

* Python 3
* Programmation procédurale
* Recherche opérationnelle

---

# Utilisation

Exécuter simplement :

```bash
python ballas_hammer.py
```

---

# Auteur
Steven
Projet académique d’optimisation des problèmes de transport en recherche opérationnelle.
