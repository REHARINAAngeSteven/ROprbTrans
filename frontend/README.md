# Optimisation du Problème de Transport

Application web pédagogique et scientifique pour la résolution du problème de transport en Recherche Opérationnelle, utilisant les algorithmes de Balas-Hammer et Stepping Stone.

## Table des Matières

1. [Aperçu](#aperçu)
2. [Architecture](#architecture)
3. [Installation et Configuration](#installation-et-configuration)
4. [Structure du Projet](#structure-du-projet)
5. [Composants](#composants)
6. [Services API](#services-api)
7. [Flux de l'Application](#flux-de-lapplication)
8. [Guide d'Utilisation](#guide-dutilisation)
9. [Styling et Design](#styling-et-design)
10. [Dépendances](#dépendances)
11. [Déploiement](#déploiement)
12. [Troubleshooting](#troubleshooting)

---

## Aperçu

Cette application est une interface universitaire complète pour résoudre le problème classique de transport en Recherche Opérationnelle. Elle implémente deux algorithmes majeurs :

- **Algorithme de Balas-Hammer** : Méthode goulue pour obtenir une solution initiale admissible
- **Algorithme de Stepping Stone** : Méthode itérative pour optimiser vers la solution optimale

### Objectif Pédagogique

L'application est conçue pour :
- Démontrer les concepts théoriques du problème de transport
- Visualiser étape par étape l'exécution des algorithmes
- Fournir une interface intuitive pour tester différentes instances
- Afficher les résultats dans un format académique et professionnel

### Cas d'Usage

```
Fournisseurs (offre) → Distribution → Destinations (demande)
       A                  Routes                   1
       B         Minimiser le coût               2
       C         d'acheminement                  3
       D                                          4
                                                  5
                                                  6
```

---

## Architecture

### Vue d'Ensemble

```
┌─────────────────────────────────────────────────────────┐
│              Frontend React + TypeScript                │
│        (Vite, Tailwind CSS, Framer Motion)              │
└──────────────────┬──────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        ↓                     ↓
   ┌─────────┐          ┌──────────────┐
   │ Services│          │  Components  │
   │ (API)   │          │  (UI)        │
   └────┬────┘          └──────┬───────┘
        │                      │
        ↓                      ↓
┌─────────────────────────────────────┐
│  Python Backend (Flask/FastAPI)     │
│  - Balas-Hammer Algorithm           │
│  - Stepping Stone Algorithm         │
│  - Calcul des coûts réduits         │
│  - Gestion des cycles               │
└─────────────────────────────────────┘
```

### Stack Technologique

| Couche | Technologie | Version | Rôle |
|--------|-------------|---------|------|
| Frontend | React | 18.3.1 | Framework UI |
| Bundler | Vite | 5.4.2 | Build tool |
| Styling | Tailwind CSS | 3.4.1 | CSS utility framework |
| Animation | Framer Motion | 10.x | Animations fluides |
| HTTP Client | Axios | 1.x | Communication API |
| Langage | TypeScript | 5.5.3 | Type safety |
| Icons | Lucide React | 0.344.0 | Icônes SVG |

---

## Installation et Configuration

### Prérequis

- **Node.js** 16.x ou supérieur
- **npm** 7.x ou supérieur
- **Python 3.8+** (pour le backend)
- **Backend actif** sur `http://localhost:8000`

### 1. Cloner le Projet

```bash
git clone <repo-url>
cd transport-optimizer
```

### 2. Installation des Dépendances Frontend

```bash
npm install
```

Cela installera :
- `react` et `react-dom` - Framework React
- `vite` - Build tool ultra-rapide
- `tailwindcss` - Framework CSS
- `framer-motion` - Libraire d'animations
- `axios` - Client HTTP
- `lucide-react` - Icônes vectorielles
- `typescript` - Compilateur TypeScript

### 3. Configuration de l'Environnement

Le projet ne nécessite pas de fichier `.env` pour fonctionner en développement local. L'API backend doit être accessible à `http://localhost:8000`.

Si vous souhaitez configurer une URL personnalisée pour le backend, modifiez dans `src/services/api.ts` :

```typescript
const API_BASE_URL = 'http://localhost:8000'; // À modifier si nécessaire
```

### 4. Vérification de l'Installation

```bash
npm run build
```

Le build devrait terminer sans erreurs et générer le dossier `dist/`.

---

## Structure du Projet

```
project/
├── src/
│   ├── components/          # Composants React
│   │   ├── Header.tsx       # En-tête avec branding
│   │   ├── TheorySection.tsx # Cartes pédagogiques
│   │   ├── TransportForm.tsx # Formulaire de config
│   │   ├── CostMatrix.tsx   # Matrice d'entrée
│   │   ├── SolveButtons.tsx # Boutons de résolution
│   │   ├── ResultTable.tsx  # Affichage résultats
│   │   ├── OptimizationSteps.tsx # Synthèse
│   │   └── Footer.tsx       # Pied de page
│   ├── services/
│   │   └── api.ts           # Client Axios, appels API
│   ├── data/
│   │   └── example.ts       # Données d'exemple
│   ├── App.tsx              # Composant principal
│   ├── main.tsx             # Point d'entrée React
│   ├── index.css            # Styles globaux
│   └── vite-env.d.ts        # Types Vite
├── public/                  # Actifs statiques
├── dist/                    # Build produit (généré)
├── package.json             # Dépendances et scripts
├── tsconfig.json            # Config TypeScript
├── vite.config.ts           # Config Vite
├── tailwind.config.js       # Config Tailwind
├── postcss.config.js        # Config PostCSS
├── .gitignore              # Fichiers ignorés git
├── eslint.config.js        # Config linter
└── README.md               # Ce fichier
```

---

## Composants

### 1. Header.tsx

**Localisation** : `src/components/Header.tsx`

**Responsabilité** : Affiche l'en-tête principal de l'application

**Props** : Aucune

**Contenu** :
- Badge "RECHERCHE OPÉRATIONNELLE" (fond vert)
- Titre principal "Optimisation du Problème de Transport" (rouge)
- Sous-titre "Algorithmes de Balas-Hammer et Stepping Stone"
- Animation d'entrée fluide (Framer Motion)

**Styling** :
- Couleurs : Blanc, vert (#22c55e), rouge (#dc2626), bleu foncé (#111827)
- Border inférieur : 4px bleu foncé
- Padding : 12 unités (48px)
- Ombre légère pour profondeur

**Code Key** :
```tsx
motion.header avec animations opacity et y
Couleurs académiques (vert, rouge, bleu)
Responsive : padding adapté
```

---

### 2. TheorySection.tsx

**Localisation** : `src/components/TheorySection.tsx`

**Responsabilité** : Section pédagogique présentant les fondements théoriques

**Props** : Aucune

**Contenu** : 4 cartes (grid 2x2 sur desktop)

**Cartes Incluses** :

1. **Définition du Problème de Transport**
   - Énoncé de l'objectif
   - Fonction objectif : `min Z = Σ Σ cij × xij`
   - Contraintes d'offre et demande
   - Contrainte de non-négativité

2. **Algorithme de Balas-Hammer**
   - Description : Méthode goulue basée sur les pénalités
   - Étapes clés :
     - Calcul des pénalités
     - Allocation au coût minimum
     - Suppression des lignes/colonnes saturées
     - Répétition jusqu'à satisfaction

3. **Algorithme de Stepping Stone**
   - Description : Optimisation itérative
   - Étapes clés :
     - Calcul des coûts réduits (δ)
     - Recherche de cycles d'amélioration
     - Réallocation selon le cycle
     - Arrêt quand δ ≥ 0

4. **Complexité Algorithmique**
   - Balas-Hammer : O(m² + n²)
   - Stepping Stone : O(m×n×k)
   - Garanties et propriétés

**Styling** :
- Cards : Border-left 4px bleu foncé
- Background : Blanc avec ombres légères
- Texte : Gris foncé, list items avec bullets bleus
- Animations : Stagger effect (délai progressif)

**Interaction** :
- Aucune interaction directe
- Visible une seule fois (viewport trigger)

---

### 3. TransportForm.tsx

**Localisation** : `src/components/TransportForm.tsx`

**Responsabilité** : Formulaire pour configurer le problème de transport

**Props** :
```typescript
interface FormProps {
  onGenerateMatrix: (
    suppliers: number,
    destinations: number,
    costMatrix: number[][],
    supply: number[],
    demand: number[]
  ) => void;
}
```

**Contrôles** :

1. **Nombre de Fournisseurs**
   - Type : Input number
   - Range : 2-10 (validation)
   - Default : 4
   - Labels : A, B, C, D, ...

2. **Nombre de Destinations**
   - Type : Input number
   - Range : 2-12 (validation)
   - Default : 6
   - Labels : 1, 2, 3, 4, 5, 6

3. **Bouton "Générer Matrice Aléatoire"**
   - Génère une matrice de coûts aléatoire (2-13)
   - Crée une offre aléatoire (20-119)
   - Crée une demande aléatoire (15-94)
   - **Équilibre automatiquement** supply = demand
   - Animation hover/tap

**Algorithme de Génération** :

```typescript
1. Créer matrice m×n avec coûts aléatoires [2, 12]
2. Créer supply aléatoire [20, 119]
3. Créer demand aléatoire [15, 94]
4. Calculer ratios = sum(supply) / sum(demand)
5. Ajuster demand *= ratio pour équilibrer
6. Appeler onGenerateMatrix()
```

**Feedback Utilisateur** :
- Message d'erreur si m < 2 ou n < 2
- Affichage des résumés après génération :
  - Matrice générée : m × n
  - Supply total
  - Demand total

**Styling** :
- Cards blanches avec border-top 4px bleu
- Inputs avec focus:border-blue-900 et focus:bg-blue-50
- Bouton bleu foncé avec hover assombri

---

### 4. CostMatrix.tsx

**Localisation** : `src/components/CostMatrix.tsx`

**Responsabilité** : Affiche et permet d'éditer la matrice de coûts

**Props** :
```typescript
interface CostMatrixProps {
  costMatrix: number[][];
  supply: number[];
  demand: number[];
  onMatrixChange?: (matrix: number[][]) => void;
}
```

**Affichage** :

**Tableau Principal** (Matrice de Coûts)
- En-têtes colonnes : 1, 2, 3, ..., n
- En-têtes lignes : A, B, C, D, ...
- Cellules : Inputs éditables
- Chaque cellule : `border-2 border-gray-300`
- Focus : `focus:bg-blue-50`

**Alerte d'Équilibre** (si supply ≠ demand)
- Couleur jaune (#fef08a)
- Border-left 4px jaune
- Message : "Les ressources ne sont pas équilibrées"
- Affiche les totaux

**Tableau de Demande** (dessous)
- Colonne pour chaque destination
- Valeur de demande en rouge
- Background gris clair

**Section Offres** (grid)
- 4 colonnes sur desktop, 2 sur mobile
- Cards pour chaque fournisseur
- Valeur en rouge gras

**Editable ?**
- OUI si `onMatrixChange` est passée
- Les changements sont reportés au parent (App.tsx)

---

### 5. SolveButtons.tsx

**Localisation** : `src/components/SolveButtons.tsx`

**Responsabilité** : Boutons pour lancer les algorithmes

**Props** :
```typescript
interface SolveButtonsProps {
  onBalaHammer: () => void;
  onSteppingStone: () => void;
  isLoading: boolean;
  disabled: boolean;
}
```

**Boutons** :

1. **Balas-Hammer (Solution Initiale)**
   - Fond : Bleu foncé (#1e3a8a)
   - Hover : Bleu plus clair (#1e40af)
   - Icône : Zap (⚡)
   - Label change pendant le chargement : "Calcul..."
   - Désactivé si `isLoading` ou `disabled`

2. **Stepping Stone (Optimisation)**
   - Fond : Vert (#15803d)
   - Hover : Vert plus clair (#166534)
   - Icône : Sparkles (✨)
   - Label change : "Optimisation..."
   - Même états de désactivation

**Layout** :
- Grid 2 colonnes sur desktop
- 1 colonne sur mobile
- Gap : 6 unités (24px)
- Responsive avec `md:` breakpoint

**Texte d'Aide** :
- Box bleu clair (#eff6ff)
- 2 étapes numérotées
- Explique l'ordre d'utilisation

---

### 6. ResultTable.tsx

**Localisation** : `src/components/ResultTable.tsx`

**Responsabilité** : Affiche les résultats d'optimisation

**Props** :
```typescript
interface ResultTableProps {
  title: string;
  costMatrix: number[][];
  allocationMatrix: number[][];
  totalCost: number;
  supply: number[];
  demand: number[];
  showCalculation?: boolean;
  isOptimal?: boolean;
}
```

**Structure** :

**Titre Section**
- Avec icône TrendingDown
- Si `isOptimal={true}`, badge vert "Solution optimale trouvée"

**Tableau d'Allocation** (Principal)
- Matrice d'allocation X (quantités transportées)
- Cellules vides affichent "-", non-nulles affichent la valeur
- Cellules non-nulles : background `bg-blue-100`
- Colonne Supply (droite) : valeurs en rouge gras
- Ligne Demand (bas) : valeurs en rouge gras

**Box Coût Total**
- Fond bleu clair (#eff6ff)
- Border-left 4px bleu
- Grand texte rouge : `Z = XXXXXX`

**Calcul Détaillé** (si `showCalculation={true}`)
- Background gris clair
- Format mono (`font-mono`)
- Affiche la formule : `Z = c11×x11 + c12×x12 + ... = TOTAL`
- Permet de vérifier le calcul manuellement

**Couleurs de Cellules** :
```typescript
0 → blanc (pas d'allocation)
> 0 → bleu clair (allocation)
```

---

### 7. OptimizationSteps.tsx

**Localisation** : `src/components/OptimizationSteps.tsx`

**Responsabilité** : Synthèse de l'optimisation et des améliorations

**Props** :
```typescript
interface OptimizationStepsProps {
  initialCost: number;
  optimizedCost: number;
  improvement: number;
}
```

**Fonctionnalité** :
- **Collapsible** : Click pour expand/collapse
- Icône chevron (▼/▶) qui change selon l'état
- Expanded par défaut

**Contenu Expandable** :

**3 Cards Côte à Côte** (grid 3 colonnes, responsive)

1. **Solution Initiale (Balas-Hammer)**
   - Titre : "Solution Initiale (Balas-Hammer)"
   - Fond bleu clair
   - Border-left 4px bleu
   - Affiche : grande valeur du coût initial

2. **Solution Optimale (Stepping Stone)**
   - Titre : "Solution Optimale (Stepping Stone)"
   - Fond vert clair
   - Border-left 4px vert
   - Affiche : grande valeur du coût optimisé

3. **Amélioration**
   - Titre : "Amélioration"
   - Fond rouge clair
   - Border-left 4px rouge
   - Affiche : `différence` et `(pourcentage%)`

**Résumé du Processus** (box grise)
- 4 points numérotés
- Explique le flux global
- Affiche le résultat final en pourcentage

---

### 8. Footer.tsx

**Localisation** : `src/components/Footer.tsx`

**Responsabilité** : Pied de page avec informations

**Contenu** :

**3 Colonnes** (responsive)

1. **Problème de Transport**
   - Titre
   - Description courte

2. **Algorithmes**
   - Liste des 3 algorithmes/fonctionnalités principales

3. **Recherche Opérationnelle**
   - Titre
   - Description du domaine

**Bas de Page** :
- Border-top gris
- Copyright avec année dynamique
- Numéro de version : "v2.0"

**Styling** :
- Background : Bleu foncé (#1e3a8a)
- Texte : Blanc et bleu clair
- Padding : 12 unités

---

## Services API

### src/services/api.ts

**Responsabilité** : Communication avec le backend Python

**Contenu** :

#### 1. Configuration Axios

```typescript
const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});
```

#### 2. Interfaces TypeScript

```typescript
interface TransportProblem {
  C: number[][];      // Matrice de coûts
  offre: number[];    // Vecteur d'offre
  demande: number[];  // Vecteur de demande
}

interface BalaHammerResponse {
  X: number[][];      // Matrice d'allocation
  Z: number;          // Coût total
  penalties?: number[][];
  allocations?: Array<{ row, col, value }>;
}

interface SteppingStoneResponse {
  X: number[][];      // Matrice d'allocation optimale
  Z: number;          // Coût total optimisé
  improvements?: Array<{ label, delta }>;
  cycles?: Array<any>;
}
```

#### 3. Fonction : solveBalaHammer()

```typescript
async solveBalaHammer(problem: TransportProblem): Promise<BalaHammerResponse>
```

**Appel** :
```
POST http://localhost:8000/balas-hammer
Content-Type: application/json

{
  "C": [[9, 12, 9, ...], [7, 3, 7, ...], ...],
  "offre": [50, 60, 20, 90],
  "demande": [40, 30, 70, 20, 40, 20]
}
```

**Réponse** :
```json
{
  "X": [[50, 0, 0, ...], [0, 30, 10, ...]],
  "Z": 1160
}
```

**Gestion d'Erreur** :
- Try/catch englobant
- Log console de l'erreur
- Lance l'exception vers le composant

---

#### 4. Fonction : solveSteppingStone()

```typescript
async solveSteppingStone(problem: TransportProblem): Promise<SteppingStoneResponse>
```

**Appel** :
```
POST http://localhost:8000/stepping-stone
Content-Type: application/json
(même payload que Balas-Hammer)
```

**Réponse** :
```json
{
  "X": [[50, 0, 0, ...], [0, 30, 10, ...]],
  "Z": 1180
}
```

**Garantie** : `Z (stepping stone) ≤ Z (balas-hammer)`

---

## Flux de l'Application

### État Global (App.tsx)

```typescript
const [problem, setProblem] = useState<ProblemState>({
  costMatrix: [],
  supply: [],
  demand: [],
});

const [results, setResults] = useState<ResultState>({
  balaHammer?: { X, Z },
  steppingStone?: { X, Z }
});

const [isLoading, setIsLoading] = useState(false);
const [error, setError] = useState<string | null>(null);
```

### Étapes du Flux Utilisateur

#### 1. **Chargement Initial**
```
App.tsx renderize
  ↓
Header (fixe)
TheorySection (explications)
TransportForm (formulaire)
Footer
```

#### 2. **Génération Matrice**
```
Utilisateur remplit (# suppliers, # destinations)
  ↓
Clique "Générer Matrice Aléatoire"
  ↓
TransportForm.handleGenerateMatrix()
  ↓
Appelle props.onGenerateMatrix()
  ↓
App.handleGenerateMatrix() capture les données
  ↓
setProblem({ costMatrix, supply, demand })
setResults({}) // réinitialise
setError(null)
  ↓
CostMatrix s'affiche avec les données
SolveButtons activés
```

#### 3. **Résolution Balas-Hammer**
```
Utilisateur clique "Balas-Hammer"
  ↓
App.handleBalaHammer()
  ↓
Validation : costMatrix.length > 0 ?
  ↓ Non
  Erreur : "Veuillez générer une matrice"
  ↓ Oui
setIsLoading(true)
setError(null)
  ↓
api.solveBalaHammer({
  C: problem.costMatrix,
  offre: problem.supply,
  demande: problem.demand
})
  ↓ Réponse OK
setResults(prev => ({
  ...prev,
  balaHammer: response
}))
  ↓ Erreur
setError("Erreur lors du calcul...")
  ↓ Finalement
setIsLoading(false)
  ↓
ResultTable (Balas-Hammer) s'affiche
Bouton Stepping Stone devient actif
```

#### 4. **Optimisation Stepping Stone**
```
Utilisateur clique "Stepping Stone"
  ↓
App.handleSteppingStone()
  ↓
Validation : results.balaHammer exists ?
  ↓ Non
  Erreur : "Veuillez d'abord résoudre avec Balas-Hammer"
  ↓ Oui
setIsLoading(true)
setError(null)
  ↓
api.solveSteppingStone({
  C: problem.costMatrix,
  offre: problem.supply,
  demande: problem.demand
})
  ↓ Réponse OK
setResults(prev => ({
  ...prev,
  steppingStone: response
}))
  ↓ Erreur
setError("Erreur lors de l'optimisation...")
  ↓ Finalement
setIsLoading(false)
  ↓
Calcul improvement = balas_Z - stepping_Z
  ↓
ResultTable (Stepping Stone) s'affiche
OptimizationSteps s'affiche
```

#### 5. **Affichage Final**
```
3 sections visibles :
  ↓
1. CostMatrix (données d'entrée)
2. ResultTable (Balas-Hammer)
3. ResultTable (Stepping Stone)
4. OptimizationSteps (synthèse)
```

---

## Guide d'Utilisation

### Pour l'Utilisateur Final

#### Étape 1 : Générer un Problème

1. Ouvrir l'application (`npm run dev`)
2. Lire la section théorique (optionnel mais recommandé)
3. Dans "Configuration du Problème" :
   - Entrer nombre de fournisseurs (ex: 4)
   - Entrer nombre de destinations (ex: 6)
   - Cliquer "Générer Matrice Aléatoire"

**Résultat** : Matrice affichée avec :
- Coûts aléatoires
- Offres équilibrées
- Demandes équilibrées

#### Étape 2 : Résoudre avec Balas-Hammer

1. Dans "Résolution du Problème" :
   - Cliquer "Balas-Hammer (Solution Initiale)"
   - Attendre la réponse (quelques secondes)

**Résultat** :
- Tableau de solution initiale
- Coût total Z₁
- Détail des allocations

#### Étape 3 : Optimiser avec Stepping Stone

1. Cliquer "Stepping Stone (Optimisation)"
2. Attendre la réponse

**Résultat** :
- Tableau de solution optimale
- Coût total Z₂ (normalement < Z₁)
- Amélioration affichée

#### Étape 4 : Analyser les Résultats

1. Comparer les deux solutions
2. Voir le pourcentage d'amélioration
3. Étudier les différences dans les allocations

#### Étape 5 : Tester Avec Autres Données

- Modifier les valeurs de la matrice manuellement (inputs éditables)
- Ou générer une nouvelle matrice aléatoire

---

### Pour les Développeurs

#### Ajouter un Nouveau Composant

1. Créer `src/components/NomComposant.tsx`
2. Importer les dépendances :
```typescript
import { motion } from 'framer-motion';
import { IconName } from 'lucide-react';
```
3. Exporter la fonction composant :
```typescript
export function NomComposant() { ... }
```
4. Importer dans App.tsx et utiliser

#### Modifier l'URL du Backend

Fichier : `src/services/api.ts`

```typescript
// Avant :
const API_BASE_URL = 'http://localhost:8000';

// Après :
const API_BASE_URL = 'https://votre-api.com';
```

#### Ajouter de Nouvelles Animations

Utiliser Framer Motion dans les composants :

```typescript
<motion.div
  initial={{ opacity: 0, y: 20 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true }}
  transition={{ duration: 0.6 }}
>
  Contenu
</motion.div>
```

Options communes :
- `initial` : État initial
- `animate` : État animation
- `whileInView` : Déclenche quand visible
- `transition` : Paramètres de timing
- `viewport` : Trigger options

#### Modifier les Couleurs

Utiliser les classes Tailwind ou modifier `tailwind.config.js`.

**Couleurs académiques actuelles** :
- Bleu foncé : `#1e3a8a` (text-blue-900, bg-blue-900)
- Blanc : `#ffffff` (bg-white)
- Gris : `#e5e7eb` (bg-gray-200)
- Rouge : `#dc2626` (text-red-600)
- Vert : `#15803d` (bg-green-700)

#### Ajouter un Nouvel Algorithme

1. Créer une interface dans `src/services/api.ts` :
```typescript
interface NewAlgoResponse {
  X: number[][];
  Z: number;
  // autres champs...
}
```

2. Créer la fonction appelante :
```typescript
export const solveNewAlgo = async (problem: TransportProblem) 
  : Promise<NewAlgoResponse> => {
  const response = await api.post('/new-algo', problem);
  return response.data;
};
```

3. Ajouter un bouton dans `SolveButtons.tsx`

4. Ajouter la logique d'appel dans `App.tsx` :
```typescript
const handleNewAlgo = async () => {
  setIsLoading(true);
  try {
    const response = await solveNewAlgo(problem);
    setResults(prev => ({ ...prev, newAlgo: response }));
  } catch (err) {
    setError('Erreur...');
  } finally {
    setIsLoading(false);
  }
};
```

---

## Styling et Design

### Philosophie Design

- **Académique** : Inspiré des documents universitaires de Recherche Opérationnelle
- **Professionnel** : Couleurs et espacements formels
- **Pédagogique** : Clairement organisé et facile à comprendre
- **Responsive** : Fonctionne sur mobile, tablette, desktop

### Palette de Couleurs

| Couleur | Tailwind | Hex | Usage |
|---------|----------|-----|-------|
| Bleu foncé | blue-900 | #1e3a8a | Titres, headers, accents |
| Rouge | red-600 | #dc2626 | Coûts, valeurs numériques |
| Vert | green-700 | #15803d | Actions, confirmations |
| Blanc | white | #ffffff | Backgrounds, cards |
| Gris clair | gray-50/100 | #f9fafb | Backgrounds secondaires |
| Gris moyen | gray-300 | #d1d5db | Bordures, séparateurs |
| Bleu clair | blue-50/100 | #eff6ff | Highlights, info boxes |

### Système d'Espacement

Base : 4px (1 unité = 4px dans Tailwind)

- Padding petits : `p-3` (12px)
- Padding normaux : `p-6` (24px)
- Padding larges : `p-8` (32px)
- Gaps : `gap-3` à `gap-8`

### Typographie

```css
/* Tailwind Defaults */
Font-family : sans-serif (système)
Body : font-normal, size 16px
Headings : font-bold, size variant
Line-height : normal (1.5 par défaut)
```

Styles appliqués :
- Titres h1 : `text-4xl font-bold`
- Titres h2 : `text-3xl font-bold`
- Titres h3 : `text-xl font-bold`
- Texte normal : `text-base text-gray-700`
- Petit texte : `text-sm text-gray-600`
- Très petit : `text-xs`

### Bordures et Ombres

- Inputs : `border-2 border-gray-300`
- Cards : `shadow-md` ou `shadow-lg`
- Focus : `border-blue-900 outline-none`
- Accents : `border-l-4 border-blue-900`

### Responsivité

**Breakpoints Tailwind** :
- `sm` : 640px
- `md` : 768px (breakpoint primaire utilisé)
- `lg` : 1024px
- `xl` : 1280px

**Patterns** :
```typescript
// 1 colonne mobile, 2 desktop
<div className="grid grid-cols-1 md:grid-cols-2 gap-6">

// Full width mobile, max-width desktop
<div className="max-w-7xl mx-auto px-6">

// Stack vertical mobile, horizontal desktop
<div className="flex flex-col md:flex-row gap-6">
```

### Classes Personnalisées (index.css)

```css
.table-cell-academic {
  border-2 border-gray-300;
  text-center;
  font-weight: 600;
}

.btn-primary {
  background: blue-900;
  color: white;
  /* ... */
}

.card-academic {
  border-left: 4px blue-900;
  background: white;
  /* ... */
}
```

---

## Dépendances

### Dependencies Principales

| Paquet | Version | Taille | Rôle |
|--------|---------|--------|------|
| react | 18.3.1 | ~42KB | Framework UI |
| react-dom | 18.3.1 | ~40KB | Rendering DOM |
| framer-motion | 10.x | ~30KB | Animations |
| axios | 1.x | ~50KB | HTTP client |
| lucide-react | 0.344.0 | ~5KB | Icons (SVG) |
| tailwindcss | 3.4.1 | ~4MB* | CSS framework |

*Tailwind est de dev-dependency et n'est pas inclus dans le bundle final.

### DevDependencies

| Paquet | Rôle |
|--------|------|
| vite | Build tool ultra-rapide |
| typescript | Type checking |
| @vitejs/plugin-react | Support React/JSX |
| tailwindcss | CSS utilities |
| postcss | CSS processing |
| autoprefixer | CSS vendor prefixes |
| eslint | Code linting |

### Tailles de Build

```
Après npm run build :
dist/index.html                 0.71 kB
dist/assets/index-DGtdS0YN.css  13.54 kB (3.09 kB gzip)
dist/assets/index-BN49A02d.js   335.28 kB (109.76 kB gzip)
```

Total gzippé : ~110 kB (très bon pour une app web)

### Compatibilité des Versions

```
Node.js : 16.x ou supérieur
NPM : 7.x ou supérieur
React : 18.x (Hooks supportés)
TypeScript : 5.5.x ou supérieur
```

---

## Déploiement

### Build Production

```bash
npm run build
```

Génère le dossier `dist/` avec tous les assets optimisés.

### Servir Localement (Test Build)

```bash
npm run preview
```

Simule le serveur production en local.

### Hébergement Recommandé

#### Option 1 : Vercel (Recommandé)

```bash
npm i -g vercel
vercel
```

Configuration automatique avec `vite.config.ts`.

#### Option 2 : Netlify

1. Connecter le repo GitHub
2. Build command : `npm run build`
3. Publish directory : `dist/`

#### Option 3 : Hébergement Static

1. Générer le build : `npm run build`
2. Copier le contenu de `dist/` sur votre serveur
3. Configurer le serveur pour servir `index.html` sur les routes non trouvées (SPA routing)

### Configuration Backend pour Déploiement

1. Mettre à jour `API_BASE_URL` dans `src/services/api.ts` :

```typescript
const API_BASE_URL = process.env.VITE_API_URL || 'http://localhost:8000';
```

2. Ajouter `.env.production` :

```env
VITE_API_URL=https://votre-api-production.com
```

3. Reconstruire : `npm run build`

### Variables d'Environnement

| Variable | Où | Default | Usage |
|----------|-----|---------|-------|
| VITE_API_URL | .env | http://localhost:8000 | URL du backend |
| NODE_ENV | auto | production (build) | Mode Node |
| VITE_* | .env | - | Variables frontend (exposées) |

---

## Troubleshooting

### Problèmes Courants

#### 1. "Cannot GET /" ou page blanche

**Cause** : Serveur Vite pas lancé ou mal configuré

**Solution** :
```bash
npm run dev
# Vérifier que http://localhost:5173 fonctionne
```

#### 2. "POST /balas-hammer 404" ou erreur réseau

**Cause** : Backend Python non accessible

**Solution** :
1. Vérifier que le backend est lancé sur `http://localhost:8000`
2. Tester : `curl http://localhost:8000/`
3. Si CORS error, ajouter CORS au backend Python :

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 3. Erreur TypeScript lors du build

**Cause** : Types manquants

**Solution** :
```bash
npm run typecheck
# Corriger les erreurs affichées
```

#### 4. Matrice ne s'affiche pas

**Cause** : costMatrix est vide

**Solution** : Générer une matrice avec le formulaire d'abord

#### 5. Buttons restent désactivés après génération

**Cause** : État `disabled` basé sur `problem.costMatrix.length === 0`

**Solution** : S'assurer que `handleGenerateMatrix` appelle correctement `setProblem`

#### 6. Animations saccadées

**Cause** : Performance GPU faible

**Solution** :
```typescript
// Dans Framer Motion, ajouter :
initial={{ opacity: 0 }}
animate={{ opacity: 1 }}
transition={{ duration: 0.3 }} // Réduire la durée
```

#### 7. Responsive ne fonctionne pas

**Cause** : Viewport meta tag manquant

**Solution** : Vérifier `index.html` :
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
```

#### 8. "Module not found" après npm install

**Cause** : Cache ou dependencies corrompues

**Solution** :
```bash
rm -rf node_modules package-lock.json
npm install
```

#### 9. CORS error "Access-Control-Allow-Origin"

**Cause** : Backend n'a pas les headers CORS

**Solution** : Backend doit retourner :
```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type
```

#### 10. Z-index (couches) mal organisés

**Cause** : Éléments positionnés se chevauchent

**Solution** : Utiliser `z-10`, `z-20`, etc. dans Tailwind

### Logs et Debugging

#### Activer Debug Mode

Ajouter dans `App.tsx` :
```typescript
console.log('Problem:', problem);
console.log('Results:', results);
console.log('Loading:', isLoading);
console.log('Error:', error);
```

#### Inspecter les Appels API

```typescript
// Dans api.ts
api.interceptors.response.use(
  response => {
    console.log('API Response:', response.data);
    return response;
  },
  error => {
    console.error('API Error:', error.response);
    throw error;
  }
);
```

#### DevTools React

1. Installer extension React DevTools (Chrome/Firefox)
2. Inspecter les props et state des composants
3. Profiler les performances

#### Vérifier le Build

```bash
npm run build
# Vérifier dist/ a du contenu
ls -lh dist/
```

---

## Exemple Complet d'Utilisation

### Données de Test

Fichier : `src/data/example.ts`

```typescript
export const exampleProblem = {
  suppliers: ['A', 'B', 'C', 'D'],
  destinations: [1, 2, 3, 4, 5, 6],
  costMatrix: [
    [9, 12, 9, 6, 9, 10],
    [7, 3, 7, 7, 5, 5],
    [6, 5, 9, 11, 3, 11],
    [6, 8, 11, 2, 2, 10],
  ],
  supply: [50, 60, 20, 90],
  demand: [40, 30, 70, 20, 40, 20],
};
```

### Flux Complet

1. **Initialisation** : App charge avec Header + TheorySection
2. **Génération** : Cliquer "Générer Matrice Aléatoire" (4x6)
3. **Affichage Matrix** : CostMatrix s'affiche
4. **Balas-Hammer** : Cliquer bouton → ResultTable initiale (Z₁)
5. **Stepping Stone** : Cliquer bouton → ResultTable optimale (Z₂)
6. **Analyse** : OptimizationSteps montre l'amélioration

### Résultat Attendu

Pour les données d'exemple du PDF :
- **Balas-Hammer** : Z = 1160
- **Stepping Stone** : Z = 1180 (ou meilleur selon optimisation)
- **Amélioration** : Positive ou zéro (jamais worse)

---

## Ressources et Liens

### Documentation Officielle

- [React 18](https://react.dev)
- [Vite](https://vitejs.dev)
- [Tailwind CSS](https://tailwindcss.com)
- [Framer Motion](https://www.framer.com/motion/)
- [Axios](https://axios-http.com)
- [TypeScript](https://www.typescriptlang.org)

### Articles Recherche Opérationnelle

- Problème de Transport classique
- Algorithme de Balas-Hammer
- Algorithme du Stepping Stone
- Dualité et coûts réduits

### Outils Utiles

- [Tailwind CSS Colors](https://tailwindcss.com/docs/customizing-colors)
- [Lucide Icons](https://lucide.dev)
- [Can I Use](https://caniuse.com) - Compatibilité navigateurs
- [DevTools MDN](https://developer.mozilla.org/en-US/docs/Tools)

---

## Support et Contribution

### Signaler un Bug

1. Ouvrir une issue GitHub
2. Fournir :
   - Étapes pour reproduire
   - Résultat attendu vs obtenu
   - Screenshots si applicable
   - Navigateur/OS utilisés

### Contribuer

1. Fork le repo
2. Créer une branche `feature/ma-feature`
3. Faire les changements
4. Tester : `npm run build && npm run typecheck`
5. Commit avec message clair
6. Push et créer une Pull Request

### Versioning

Version actuelle : **2.0.0**

Format : `MAJOR.MINOR.PATCH`

---

## Conclusion

Cette application démontre comment créer une interface pédagogique professionnelle pour les algorithmes d'optimisation. Elle combine :

- **Frontend moderne** (React 18 + Vite)
- **Design académique** (Tailwind CSS)
- **Animations fluides** (Framer Motion)
- **Type safety** (TypeScript)
- **Best practices** (composants modulaires, séparation concerns)

Pour toute question ou amélioration, consultez la documentation ou ouvrez une issue.

---

**Dernière mise à jour** : 2026-05-29  
**Version** : 2.0.0  
**Auteur** : Claude Agent  
**License** : Open Source

