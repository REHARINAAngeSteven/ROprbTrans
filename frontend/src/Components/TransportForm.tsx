// src/Components/TransportForm.tsx
import { useState } from 'react';
import { motion } from 'framer-motion';
import { Settings } from 'lucide-react';

interface FormProps {
  onGenerateMatrix: (suppliers: number, destinations: number, costMatrix: number[][], supply: number[], demand: number[]) => void;
}

type Mode = 'aleatoire' | 'manuel';

export function TransportForm({ onGenerateMatrix }: FormProps) {
  const [suppliers, setSuppliers] = useState(4);
  const [destinations, setDestinations] = useState(6);
  const [mode, setMode] = useState<Mode>('aleatoire');
  const [costMatrix, setCostMatrix] = useState<number[][]>([]);
  const [supply, setSupply] = useState<number[]>([]);
  const [demand, setDemand] = useState<number[]>([]);

  const buildEmptyMatrix = (rows: number, cols: number): number[][] =>
    Array(rows)
      .fill(null)
      .map(() => Array(cols).fill(0));

  const generateMatrix = () => {
    if (suppliers < 2 || destinations < 2) {
      alert('Minimum 2 fournisseurs et 2 destinations');
      return;
    }

    let newCostMatrix: number[][];
    let newSupply: number[];
    let newDemand: number[];

    if (mode === 'aleatoire') {
      newCostMatrix = Array(suppliers)
        .fill(null)
        .map(() => Array(destinations)
          .fill(null)
          .map(() => Math.floor(Math.random() * 12) + 2));

      newSupply = Array(suppliers)
        .fill(null)
        .map(() => Math.floor(Math.random() * 100) + 20);

      newDemand = Array(destinations)
        .fill(null)
        .map(() => Math.floor(Math.random() * 80) + 15);
    } else {
      // Mode manuel : on part d'une grille à zéro, entièrement éditable
      // ensuite dans CostMatrix. Aucune valeur n'est imposée.
      newCostMatrix = buildEmptyMatrix(suppliers, destinations);
      newSupply = Array(suppliers).fill(0);
      newDemand = Array(destinations).fill(0);
    }

    setCostMatrix(newCostMatrix);
    setSupply(newSupply);
    setDemand(newDemand);

    onGenerateMatrix(suppliers, destinations, newCostMatrix, newSupply, newDemand);
  };

  return (
    <motion.section
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.6 }}
      className="max-w-7xl mx-auto px-6 py-16"
    >
      <div className="flex items-center gap-3 mb-8">
        <Settings className="w-8 h-8 text-blue-900" />
        <h2 className="text-3xl font-bold text-blue-900">Configuration du Problème</h2>
      </div>

      <div className="bg-white rounded-lg shadow-md p-8 border-t-4 border-blue-900">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
          <div>
            <label className="block text-sm font-bold text-gray-700 mb-3">
              Nombre de fournisseurs
            </label>
            <input
              type="number"
              min="2"
              max="10"
              value={suppliers}
              onChange={(e) => setSuppliers(Math.max(2, parseInt(e.target.value) || 2))}
              className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-blue-900 focus:outline-none text-lg font-semibold"
            />
            <p className="text-xs text-gray-500 mt-2">Lignes A, B, C, D...</p>
          </div>

          <div>
            <label className="block text-sm font-bold text-gray-700 mb-3">
              Nombre de destinations
            </label>
            <input
              type="number"
              min="2"
              max="12"
              value={destinations}
              onChange={(e) => setDestinations(Math.max(2, parseInt(e.target.value) || 2))}
              className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-blue-900 focus:outline-none text-lg font-semibold"
            />
            <p className="text-xs text-gray-500 mt-2">Colonnes 1, 2, 3, 4...</p>
          </div>
        </div>

        <div className="mb-8">
          <label className="block text-sm font-bold text-gray-700 mb-3">
            Mode de saisie
          </label>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <button
              type="button"
              onClick={() => setMode('aleatoire')}
              className={`py-3 px-4 rounded-lg font-semibold border-2 transition-colors ${
                mode === 'aleatoire'
                  ? 'bg-blue-900 text-white border-blue-900'
                  : 'bg-white text-gray-700 border-gray-300 hover:border-blue-900'
              }`}
            >
              Génération aléatoire
            </button>
            <button
              type="button"
              onClick={() => setMode('manuel')}
              className={`py-3 px-4 rounded-lg font-semibold border-2 transition-colors ${
                mode === 'manuel'
                  ? 'bg-blue-900 text-white border-blue-900'
                  : 'bg-white text-gray-700 border-gray-300 hover:border-blue-900'
              }`}
            >
              Saisie manuelle
            </button>
          </div>
          <p className="text-xs text-gray-500 mt-2">
            {mode === 'aleatoire'
              ? 'Les coûts, offres et demandes seront générés aléatoirement (modifiables ensuite).'
              : "La grille sera créée à zéro : entrez vos propres coûts, offres et demandes ci-dessous."}
          </p>
        </div>

        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={generateMatrix}
          className="w-full bg-blue-900 text-white font-bold py-4 px-6 rounded-lg hover:bg-blue-800 transition-colors shadow-md"
        >
          {mode === 'aleatoire' ? 'Générer Matrice Aléatoire' : 'Créer la Grille'}
        </motion.button>

        {costMatrix.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-8 text-sm text-gray-600 bg-gray-50 p-4 rounded-lg"
          >
            <p><strong>Matrice générée:</strong> {suppliers} fournisseurs × {destinations} destinations</p>
            <p><strong>Supply total:</strong> {supply.reduce((a, b) => a + b, 0)}</p>
            <p><strong>Demand total:</strong> {demand.reduce((a, b) => a + b, 0)}</p>
          </motion.div>
        )}
      </div>
    </motion.section>
  );
}