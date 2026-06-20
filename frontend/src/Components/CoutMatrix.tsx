// src/Components/CoutMatrix.tsx
import { motion } from 'framer-motion';
import { AlertCircle, CheckCircle2 } from 'lucide-react';

interface CostMatrixProps {
  costMatrix: number[][];
  supply: number[];
  demand: number[];
  onMatrixChange?: (matrix: number[][]) => void;
  onSupplyChange?: (supply: number[]) => void;
  onDemandChange?: (demand: number[]) => void;
}

const getSupplierLabel = (idx: number) => String.fromCharCode(65 + idx);

export function CostMatrix({
  costMatrix,
  supply,
  demand,
  onMatrixChange,
  onSupplyChange,
  onDemandChange,
}: CostMatrixProps) {
  if (costMatrix.length === 0) {
    return null;
  }

  const handleCellChange = (i: number, j: number, value: string) => {
    if (!onMatrixChange) return;
    const newMatrix = costMatrix.map((row) => [...row]);
    newMatrix[i][j] = parseInt(value) || 0;
    onMatrixChange(newMatrix);
  };

  const handleSupplyChange = (i: number, value: string) => {
    if (!onSupplyChange) return;
    const newSupply = [...supply];
    newSupply[i] = parseInt(value) || 0;
    onSupplyChange(newSupply);
  };

  const handleDemandChange = (j: number, value: string) => {
    if (!onDemandChange) return;
    const newDemand = [...demand];
    newDemand[j] = parseInt(value) || 0;
    onDemandChange(newDemand);
  };

  const supplyTotal = supply.reduce((a, b) => a + b, 0);
  const demandTotal = demand.reduce((a, b) => a + b, 0);
  const isBalanced = supplyTotal === demandTotal;
  const isEditable = Boolean(onMatrixChange);

  return (
    <motion.section
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.6 }}
      className="max-w-7xl mx-auto px-6 py-16"
    >
      <h2 className="text-2xl font-bold text-blue-900 mb-6">Matrice de Coûts et Ressources</h2>

      {!isBalanced ? (
        <div className="flex items-center gap-3 bg-yellow-50 border-l-4 border-yellow-600 p-4 mb-6 rounded">
          <AlertCircle className="w-5 h-5 text-yellow-600 flex-shrink-0" />
          <p className="text-sm text-yellow-700">
            <strong>Attention:</strong> Les ressources ne sont pas équilibrées. Supply: {supplyTotal}, Demand: {demandTotal}.
            {' '}Le backend ajoutera automatiquement une ligne ou colonne fictive pour équilibrer avant de résoudre.
          </p>
        </div>
      ) : (
        <div className="flex items-center gap-3 bg-green-50 border-l-4 border-green-600 p-4 mb-6 rounded">
          <CheckCircle2 className="w-5 h-5 text-green-600 flex-shrink-0" />
          <p className="text-sm text-green-700">
            <strong>Équilibré:</strong> Supply: {supplyTotal} = Demand: {demandTotal}.
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
                <th className="border-2 border-gray-300 bg-gray-300 w-24 h-12 font-bold">Supply</th>
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
                        readOnly={!isEditable}
                        onChange={(e) => handleCellChange(i, j, e.target.value)}
                        className={`w-full h-full text-center font-semibold text-gray-700 border-0 focus:outline-none ${
                          isEditable ? 'focus:bg-blue-50' : 'bg-gray-50 cursor-not-allowed'
                        }`}
                      />
                    </td>
                  ))}
                  <td className="border-2 border-gray-300 bg-gray-50 w-24 h-12 text-center p-1">
                    <input
                      type="number"
                      value={supply[i] ?? 0}
                      readOnly={!onSupplyChange}
                      onChange={(e) => handleSupplyChange(i, e.target.value)}
                      className={`w-full h-full text-center font-bold text-red-600 border-0 focus:outline-none ${
                        onSupplyChange ? 'focus:bg-red-50' : 'bg-gray-50 cursor-not-allowed'
                      }`}
                    />
                  </td>
                </tr>
              ))}
              <tr>
                <td className="border-2 border-gray-300 bg-gray-300 w-16 h-12 font-bold text-center">
                  Demand
                </td>
                {demand.map((d, j) => (
                  <td key={j} className="border-2 border-gray-300 bg-gray-50 w-24 h-12 text-center p-1">
                    <input
                      type="number"
                      value={d}
                      readOnly={!onDemandChange}
                      onChange={(e) => handleDemandChange(j, e.target.value)}
                      className={`w-full h-full text-center font-bold text-red-600 border-0 focus:outline-none ${
                        onDemandChange ? 'focus:bg-red-50' : 'bg-gray-50 cursor-not-allowed'
                      }`}
                    />
                  </td>
                ))}
                <td className="border-2 border-gray-300 bg-gray-300 w-24 h-12"></td>
              </tr>
            </tbody>
          </table>
        </div>

        {!isEditable && (
          <p className="text-xs text-gray-400 mt-4 italic">
            L'édition est désactivée (callbacks non fournis).
          </p>
        )}
      </div>
    </motion.section>
  );
}