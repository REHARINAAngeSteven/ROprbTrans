// src/Components/BtnResoudre.tsx
import { motion } from 'framer-motion';
import { Zap, Sparkles } from 'lucide-react';

interface SolveButtonsProps {
  onBalaHammer: () => void;
  onSteppingStone: () => void;
  isLoading: boolean;
  disabled: boolean;
}

export function SolveButtons({
  onBalaHammer,
  onSteppingStone,
  isLoading,
  disabled,
}: SolveButtonsProps) {
  return (
    <motion.section
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.6 }}
      className="max-w-7xl mx-auto px-6 py-16"
    >
      <div className="bg-white rounded-lg shadow-md p-8 border-t-4 border-blue-900">
        <h2 className="text-2xl font-bold text-blue-900 mb-8 text-center">Résolution du Problème</h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={onBalaHammer}
            disabled={isLoading || disabled}
            className="flex items-center justify-center gap-3 bg-blue-900 text-white font-bold py-4 px-6 rounded-lg hover:bg-blue-800 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors shadow-md"
          >
            <Zap className="w-5 h-5" />
            {isLoading ? 'Calcul...' : 'Balas-Hammer (Solution Initiale)'}
          </motion.button>

          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={onSteppingStone}
            disabled={isLoading || disabled}
            className="flex items-center justify-center gap-3 bg-green-700 text-white font-bold py-4 px-6 rounded-lg hover:bg-green-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors shadow-md"
          >
            <Sparkles className="w-5 h-5" />
            {isLoading ? 'Optimisation...' : 'Stepping Stone (Optimisation)'}
          </motion.button>
        </div>

        <div className="mt-6 bg-blue-50 rounded-lg p-4 text-sm text-gray-700 border-l-4 border-blue-900">
          <p>
            <strong>Étape 1:</strong> Cliquez sur Balas-Hammer pour obtenir une solution initiale
          </p>
          <p>
            <strong>Étape 2:</strong> Cliquez sur Stepping Stone pour optimiser la solution
          </p>
        </div>
      </div>
    </motion.section>
  );
}
