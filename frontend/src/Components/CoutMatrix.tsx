import { motion } from 'framer-motion';
import { AlertCircle } from 'lucide-react';

interface CostMatrixProps {
  costMatrix: number[][];
  supply: number[];
  demand: number[];
  onMatrixChange?: (matrix: number[][]) => void;
}

const getSupplierLabel = (idx: number) => String.fromCharCode(65 + idx);

export function CostMatrix({ costMatrix, supply, demand, onMatrixChange }: CostMatrixProps) {
  if (costMatrix.length === 0) {
    return null;
  }

  const handleCellChange = (i: number, j: number, value: string) => {
    if (!onMatrixChange) return;
    const newMatrix = costMatrix.map(row => [...row]);
    newMatrix[i][j] = parseInt(value) || 0;
    onMatrixChange(newMatrix);
  };

  const isBalanced = supply.reduce((a, b) => a + b, 0) === demand.reduce((a, b) => a + b, 0);

  return (
    <motion.section
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.6 }}
      className="max-w-7xl mx-auto px-6 py-16"
    >
      <h2 className="text-2xl font-bold text-blue-900 mb-6">Matrice de Coûts et Ressources</h2>

      {!isBalanced && (
        <div className="flex items-center gap-3 bg-yellow-50 border-l-4 border-yellow-600 p-4 mb-6 rounded">
          <AlertCircle className="w-5 h-5 text-yellow-600" />
          <p className="text-sm text-yellow-700">
            <strong>Attention:</strong> Les ressources ne sont pas équilibrées. Supply: {supply.reduce((a, b) => a + b, 0)}, Demand: {demand.reduce((a, b) => a + b, 0)}
          </p>
        </div>
      )}

      <div className="bg-white rounded-lg shadow-md p-8 overflow-x-auto border-t-4 border-blue-900">
        <div className="inline-block min-w-full">
          <table className="border-collapse">
            <thead>
              <tr>
                <th className="border-2 border-gray-300 bg-blue-900 text-white w-16 h-12"></th>
                {Array(costMatrix[0].length)
                  .fill(null)
                  .map((_, j) => (
                    <th
                      key={j}
                      className="border-2 border-gray-300 bg-blue-900 text-white w-24 h-12 text-lg font-bold"
                    >
                      {j + 1}
                    </th>
                  ))}
              </tr>
            </thead>
            <tbody>
              {costMatrix.map((row, i) => (
                <tr key={i}>
                  <td className="border-2 border-gray-300 bg-blue-900 text-white w-16 h-12 font-bold text-lg text-center">
                    {getSupplierLabel(i)}
                  </td>
                  {row.map((cost, j) => (
                    <td
                      key={j}
                      className="border-2 border-gray-300 w-24 h-12 text-center p-1"
                    >
                      <input
                        type="number"
                        value={cost}
                        onChange={(e) => handleCellChange(i, j, e.target.value)}
                        className="w-full h-full text-center font-semibold text-gray-700 border-0 focus:outline-none focus:bg-blue-50"
                      />
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="mt-8 overflow-x-auto">
          <table className="border-collapse">
            <thead>
              <tr>
                <th className="border-2 border-gray-300 bg-gray-100 w-16 h-10"></th>
                {Array(costMatrix[0].length)
                  .fill(null)
                  .map((_, j) => (
                    <th
                      key={j}
                      className="border-2 border-gray-300 bg-gray-100 w-24 h-10"
                    >
                      <input
                        type="number"
                        value={demand[j]}
                        readOnly
                        className="w-full h-full text-center font-bold text-red-600 border-0 bg-transparent"
                      />
                    </th>
                  ))}
              </tr>
            </thead>
            <tbody>
              <tr>
                <td className="border-2 border-gray-300 bg-gray-100 w-16 h-10 text-center font-bold">
                  Demand
                </td>
                {demand.map((d, j) => (
                  <td key={j} className="border-2 border-gray-300 bg-gray-50 w-24 h-10 text-center">
                    <span className="font-bold text-red-600">{d}</span>
                  </td>
                ))}
              </tr>
            </tbody>
          </table>
        </div>

        <div className="mt-8">
          <h3 className="font-bold text-blue-900 mb-4">Offres des Fournisseurs</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {supply.map((s, i) => (
              <div key={i} className="border-2 border-gray-300 rounded p-3 text-center">
                <p className="text-sm text-gray-600">Fournisseur {getSupplierLabel(i)}</p>
                <p className="text-2xl font-bold text-red-600">{s}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </motion.section>
  );
}
