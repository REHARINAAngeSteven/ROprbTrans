// src/App.tsx
import { useState } from 'react';
import { Header } from './Components/Header';
import { TheorySection } from './Components/SectionThéorie';
import { TransportForm } from './Components/TransportForm';
import { CostMatrix } from './Components/CoutMatrix';
import { SolveButtons } from './Components/BtnResoudre';
import { ResultTable } from './Components/TableauRes';
import { OptimizationSteps } from './Components/OptSteppingStone';
import { Footer } from './Components/Footer';
import { solveBalasHammer, solveSteppingStone } from './services/api';

interface ProblemState {
  costMatrix: number[][];
  supply: number[];
  demand: number[];
}

// Version équilibrée du problème, renvoyée par /balas-hammer.
// Peut différer de ProblemState si une ligne/colonne fictive a été
// ajoutée côté backend (offre != demande).
interface BalancedProblemState {
  costMatrix: number[][];
  supply: number[];
  demand: number[];
}

interface ResultState {
  balasHammer?: {
    X: number[][];
    Z: number;
  };
  steppingStone?: {
    X: number[][];
    Z: number;
  };
}

export default function App() {
  const [problem, setProblem] = useState<ProblemState>({
    costMatrix: [],
    supply: [],
    demand: [],
  });

  // Données équilibrées renvoyées par Balas-Hammer, nécessaires pour
  // que Stepping Stone travaille sur le même référentiel (mêmes
  // dimensions, même offre/demande totales).
  const [balancedProblem, setBalancedProblem] = useState<BalancedProblemState | null>(null);

  const [results, setResults] = useState<ResultState>({});
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Une fois qu'un calcul a été lancé, on verrouille l'édition : modifier
  // les coûts/offre/demande après coup rendrait les résultats affichés
  // incohérents avec les données actuelles de la grille. Pour réessayer
  // d'autres valeurs, il faut régénérer/recréer la grille.
  const isLocked = Boolean(results.balasHammer);

  const handleGenerateMatrix = (
    suppliers: number,
    destinations: number,
    costMatrix: number[][],
    supply: number[],
    demand: number[]
  ) => {
    setProblem({ costMatrix, supply, demand });
    setBalancedProblem(null);
    setResults({});
    setError(null);
  };

  const handleMatrixChange = (newMatrix: number[][]) => {
    setProblem((prev) => ({ ...prev, costMatrix: newMatrix }));
  };

  const handleSupplyChange = (newSupply: number[]) => {
    setProblem((prev) => ({ ...prev, supply: newSupply }));
  };

  const handleDemandChange = (newDemand: number[]) => {
    setProblem((prev) => ({ ...prev, demand: newDemand }));
  };

  const handleBalasHammer = async () => {
    if (problem.costMatrix.length === 0) {
      setError("Veuillez générer une matrice d'abord");
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await solveBalasHammer({
        couts: problem.costMatrix,
        offre: problem.supply,
        demande: problem.demand,
      });

      // On retient la version équilibrée pour l'étape Stepping Stone,
      // qu'il y ait eu équilibrage ou non (dans le cas contraire, elle
      // est simplement identique aux données d'origine).
      setBalancedProblem({
        costMatrix: response.couts_equilibres,
        supply: response.offre_equilibree,
        demand: response.demande_equilibree,
      });

      setResults((prev) => ({
        ...prev,
        balasHammer: {
          X: response.allocation,
          Z: response.cout_total,
        },
      }));
    } catch (err) {
      setError('Erreur lors du calcul avec Balas-Hammer. Vérifiez que le backend est actif.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSteppingStone = async () => {
    if (!results.balasHammer || !balancedProblem) {
      setError("Veuillez d'abord résoudre avec Balas-Hammer");
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await solveSteppingStone({
        couts: balancedProblem.costMatrix,
        offre: balancedProblem.supply,
        demande: balancedProblem.demand,
        allocation_initiale: results.balasHammer.X,
      });

      setResults((prev) => ({
        ...prev,
        steppingStone: {
          X: response.allocation,
          Z: response.cout_total,
        },
      }));
    } catch (err) {
      setError("Erreur lors de l'optimisation avec Stepping Stone.");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const improvement =
    results.balasHammer && results.steppingStone
      ? results.balasHammer.Z - results.steppingStone.Z
      : 0;

  // Le tableau de résultats affiche la matrice de coûts ET l'offre/demande
  // associées à l'allocation montrée. Une fois équilibré, on doit afficher
  // la version équilibrée (balancedProblem), pas les données d'origine,
  // sans quoi les dimensions ne correspondraient plus à l'allocation reçue.
  const displayedCostMatrix = balancedProblem?.costMatrix ?? problem.costMatrix;
  const displayedSupply = balancedProblem?.supply ?? problem.supply;
  const displayedDemand = balancedProblem?.demand ?? problem.demand;

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <TheorySection />

      <TransportForm onGenerateMatrix={handleGenerateMatrix} />

      {problem.costMatrix.length > 0 && (
        <>
          <CostMatrix
            costMatrix={problem.costMatrix}
            supply={problem.supply}
            demand={problem.demand}
            onMatrixChange={isLocked ? undefined : handleMatrixChange}
            onSupplyChange={isLocked ? undefined : handleSupplyChange}
            onDemandChange={isLocked ? undefined : handleDemandChange}
          />

          {isLocked && (
            <div className="max-w-7xl mx-auto px-6 -mt-10 pb-6">
              <p className="text-xs text-gray-500 italic">
                La grille est verrouillée après un calcul. Régénérez ou recréez une grille
                ci-dessus pour tester d'autres valeurs.
              </p>
            </div>
          )}

          <SolveButtons
            onBalaHammer={handleBalasHammer}
            onSteppingStone={handleSteppingStone}
            isLoading={isLoading}
            disabled={problem.costMatrix.length === 0}
          />

          {error && (
            <div className="max-w-7xl mx-auto px-6 py-8">
              <div className="bg-red-50 border-l-4 border-red-600 rounded-lg p-6 text-red-700">
                <p className="font-semibold">Erreur: {error}</p>
              </div>
            </div>
          )}

          {results.balasHammer && (
            <ResultTable
              title="Solution Initiale - Algorithme de Balas-Hammer"
              costMatrix={displayedCostMatrix}
              allocationMatrix={results.balasHammer.X}
              totalCost={results.balasHammer.Z}
              supply={displayedSupply}
              demand={displayedDemand}
              showCalculation={true}
            />
          )}

          {results.steppingStone && (
            <ResultTable
              title="Solution Optimale - Algorithme de Stepping Stone"
              costMatrix={displayedCostMatrix}
              allocationMatrix={results.steppingStone.X}
              totalCost={results.steppingStone.Z}
              supply={displayedSupply}
              demand={displayedDemand}
              showCalculation={true}
              isOptimal={true}
            />
          )}

          {results.balasHammer && results.steppingStone && (
            <OptimizationSteps
              initialCost={results.balasHammer.Z}
              optimizedCost={results.steppingStone.Z}
              improvement={improvement}
            />
          )}
        </>
      )}

      <Footer />
    </div>
  );
}