// src/Components/OptSteppingStone.tsx
import { motion } from 'framer-motion';
import { ChevronDown, ChevronUp } from 'lucide-react';
import { useState } from 'react';

interface OptimizationStepsProps {
  initialCost: number;
  optimizedCost: number;
  improvement: number;
}

export function OptimizationSteps({
  initialCost,
  optimizedCost,
  improvement,
}: OptimizationStepsProps) {
  const [expanded, setExpanded] = useState(true);

  const improvementPercent = ((improvement / initialCost) * 100).toFixed(2);

  return (
    <motion.section
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.6 }}
      className="max-w-7xl mx-auto px-6 py-16"
    >
      <div
        onClick={() => setExpanded(!expanded)}
        className="bg-white rounded-lg shadow-md border-t-4 border-blue-900 cursor-pointer hover:shadow-lg transition-shadow"
      >
        <div className="flex items-center justify-between p-8">
          <h2 className="text-2xl font-bold text-blue-900">Synthèse de l'Optimisation</h2>
          {expanded ? <ChevronUp className="w-6 h-6" /> : <ChevronDown className="w-6 h-6" />}
        </div>

        {expanded && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="px-8 pb-8 border-t border-gray-200"
          >
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <div className="bg-blue-50 rounded-lg p-6 border-l-4 border-blue-900">
                <p className="text-sm text-gray-600 font-semibold mb-2">Solution Initiale (Balas-Hammer)</p>
                <p className="text-3xl font-bold text-blue-900">{initialCost}</p>
              </div>

              <div className="bg-green-50 rounded-lg p-6 border-l-4 border-green-700">
                <p className="text-sm text-gray-600 font-semibold mb-2">Solution Optimale (Stepping Stone)</p>
                <p className="text-3xl font-bold text-green-700">{optimizedCost}</p>
              </div>

              <div className="bg-red-50 rounded-lg p-6 border-l-4 border-red-700">
                <p className="text-sm text-gray-600 font-semibold mb-2">Amélioration</p>
                <p className="text-3xl font-bold text-red-700">
                  {improvement} ({improvementPercent}%)
                </p>
              </div>
            </div>

            <div className="bg-gray-50 rounded-lg p-6 space-y-3">
              <h3 className="font-bold text-gray-800 mb-4">Résumé du processus:</h3>
              <div className="space-y-2 text-sm text-gray-700">
                <p>
                  <strong>1. Balas-Hammer:</strong> Fournit une solution initiale admissible basée sur les pénalités
                </p>
                <p>
                  <strong>2. Stepping Stone:</strong> Améliore la solution en testant des améliorations potentielles
                </p>
                <p>
                  <strong>3. Critère d'optimalité:</strong> Tous les coûts réduits sont ≥ 0
                </p>
                <p>
                  <strong>4. Résultat:</strong> Réduction du coût de {improvement} unités ({improvementPercent}%)
                </p>
              </div>
            </div>
          </motion.div>
        )}
      </div>
    </motion.section>
  );
}
