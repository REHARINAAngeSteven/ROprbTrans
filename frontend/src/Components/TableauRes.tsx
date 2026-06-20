// src/Components/TableauRes.tsx
import { motion } from 'framer-motion';
import { TrendingDown } from 'lucide-react';

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

const getSupplierLabel = (idx: number) => String.fromCharCode(65 + idx);

export function ResultTable({
  title,
  costMatrix,
  allocationMatrix,
  totalCost,
  supply,
  demand,
  showCalculation = false,
  isOptimal = false,
}: ResultTableProps) {
  if (allocationMatrix.length === 0) return null;

  const getBackgroundColor = (value: number) => {
    if (value === 0) return 'bg-white';
    return 'bg-blue-100';
  };

  const calculations: string[] = [];
  for (let i = 0; i < allocationMatrix.length; i++) {
    for (let j = 0; j < allocationMatrix[i].length; j++) {
      if (allocationMatrix[i][j] > 0) {
        calculations.push(
          `${costMatrix[i][j]} × ${allocationMatrix[i][j]}`
        );
      }
    }
  }

  return (
    <motion.section
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.6 }}
      className="max-w-7xl mx-auto px-6 py-16"
    >
      <div className="flex items-center gap-3 mb-8">
        <TrendingDown className="w-8 h-8 text-blue-900" />
        <div>
          <h2 className="text-2xl font-bold text-blue-900">{title}</h2>
          {isOptimal && (
            <p className="text-sm text-green-600 font-semibold">Solution optimale trouvée</p>
          )}
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-md p-8 border-t-4 border-blue-900">
        <div className="overflow-x-auto mb-8">
          <table className="border-collapse inline-block min-w-full">
            <thead>
              <tr>
                <th className="border-2 border-gray-300 bg-blue-900 text-white w-16 h-12"></th>
                {Array(allocationMatrix[0].length)
                  .fill(null)
                  .map((_, j) => (
                    <th
                      key={j}
                      className="border-2 border-gray-300 bg-blue-900 text-white w-24 h-12 text-lg font-bold"
                    >
                      {j + 1}
                    </th>
                  ))}
                <th className="border-2 border-gray-300 bg-gray-300 w-16 h-12 font-bold">Supply</th>
              </tr>
            </thead>
            <tbody>
              {allocationMatrix.map((row, i) => (
                <tr key={i}>
                  <td className="border-2 border-gray-300 bg-blue-900 text-white w-16 h-12 font-bold text-lg text-center">
                    {getSupplierLabel(i)}
                  </td>
                  {row.map((allocation, j) => (
                    <td
                      key={j}
                      className={`border-2 border-gray-300 w-24 h-12 text-center font-bold ${getBackgroundColor(
                        allocation
                      )}`}
                    >
                      {allocation > 0 ? allocation : '-'}
                    </td>
                  ))}
                  <td className="border-2 border-gray-300 bg-gray-100 w-16 h-12 text-center font-bold text-red-600">
                    {supply[i]}
                  </td>
                </tr>
              ))}
              <tr>
                <td className="border-2 border-gray-300 bg-gray-300 w-16 h-12 font-bold">Demand</td>
                {demand.map((d, j) => (
                  <td
                    key={j}
                    className="border-2 border-gray-300 bg-gray-100 w-24 h-12 text-center font-bold text-red-600"
                  >
                    {d}
                  </td>
                ))}
                <td className="border-2 border-gray-300 bg-gray-300 w-16 h-12"></td>
              </tr>
            </tbody>
          </table>
        </div>

        <div className="bg-blue-50 rounded-lg p-6 mb-6 border-l-4 border-blue-900">
          <h3 className="text-lg font-bold text-blue-900 mb-4">Coût Total</h3>
          <div className="text-4xl font-bold text-red-600">
            Z = {totalCost.toLocaleString()}
          </div>
        </div>

        {showCalculation && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-gray-50 rounded-lg p-6 border-l-4 border-gray-400"
          >
            <h3 className="text-sm font-bold text-gray-700 mb-3">Calcul du coût:</h3>
            <p className="text-sm text-gray-600 font-mono whitespace-pre-wrap break-words">
              Z = {calculations.join(' + ')} = {totalCost}
            </p>
          </motion.div>
        )}
      </div>
    </motion.section>
  );
}
