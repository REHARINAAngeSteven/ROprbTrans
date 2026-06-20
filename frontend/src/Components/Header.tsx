// src/Components/Header.tsx
import { motion } from 'framer-motion';

export function Header() {
  return (
    <motion.header
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="bg-white border-b-4 border-blue-900 shadow-md"
    >
      <div className="max-w-7xl mx-auto px-6 py-12">
        <div className="flex items-center justify-between mb-4">
          <div className="bg-green-600 text-white px-4 py-2 text-sm font-bold rounded">
            RECHERCHE OPÉRATIONNELLE
          </div>
          <div className="text-xs text-gray-600">Problème de Transport</div>
        </div>
        <h1 className="text-4xl font-bold text-red-600 mb-3 text-center">
          Optimisation du Problème de Transport
        </h1>
        <p className="text-xl text-gray-700 text-center font-semibold">
          Algorithmes de Balas-Hammer et Stepping Stone
        </p>
      </div>
    </motion.header>
  );
}
