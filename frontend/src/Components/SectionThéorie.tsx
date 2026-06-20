// src/Components/SectionThéorie.tsx
import { motion } from 'framer-motion';
import { BookOpen } from 'lucide-react';

const theories = [
  {
    title: 'Définition du Problème de Transport',
    description: 'Minimiser le coût total de transport en distribuant les ressources des fournisseurs vers les destinations.',
    key_points: [
      'Objectif: min Z = Σ Σ cij × xij',
      'Contraintes: Σ xij = offrei (fournisseurs)',
      'Σ xij = demandej (destinations)',
      'xij ≥ 0 (non-négativité)',
    ],
  },
  {
    title: 'Algorithme de Balas-Hammer',
    description: 'Méthode goulue basée sur les pénalités pour obtenir une solution initiale.',
    key_points: [
      'Calcul des pénalités (différences entre les deux plus petits coûts)',
      'Allocation au coût minimum de la ligne/colonne avec plus grande pénalité',
      'Suppression des lignes/colonnes saturées',
      'Répétition jusqu\'à satisfaction complète',
    ],
  },
  {
    title: 'Algorithme de Stepping Stone',
    description: 'Méthode itérative pour optimiser la solution initiale vers l\'optimum.',
    key_points: [
      'Calcul des coûts réduits (δ) pour les cellules non allouées',
      'Recherche de cycles d\'amélioration',
      'Réallocation selon le cycle si amélioration possible',
      'Arrêt quand tous les δ ≥ 0',
    ],
  },
  {
    title: 'Complexité Algorithmique',
    description: 'Performance et limites des algorithmes.',
    key_points: [
      'Balas-Hammer: O(m² + n²) opérations',
      'm = nombre de fournisseurs, n = nombre de destinations',
      'Solution non garantie optimale mais très proche (heuristique)',
      'Stepping Stone: O(m×n×k) où k = itérations',
    ],
  },
];

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
};

const cardVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5 },
  },
};

export function TheorySection() {
  return (
    <motion.section
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true }}
      variants={containerVariants}
      className="max-w-7xl mx-auto px-6 py-16"
    >
      <div className="flex items-center gap-3 mb-12">
        <BookOpen className="w-8 h-8 text-blue-900" />
        <h2 className="text-3xl font-bold text-blue-900">Fondements Théoriques</h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {theories.map((theory, idx) => (
          <motion.div
            key={idx}
            variants={cardVariants}
            className="bg-white border-l-4 border-blue-900 rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
          >
            <h3 className="text-xl font-bold text-blue-900 mb-3">{theory.title}</h3>
            <p className="text-gray-700 mb-4 text-sm leading-relaxed">{theory.description}</p>
            <ul className="space-y-2">
              {theory.key_points.map((point, i) => (
                <li key={i} className="flex items-start gap-3 text-sm text-gray-600">
                  <span className="text-blue-900 font-bold">•</span>
                  <span>{point}</span>
                </li>
              ))}
            </ul>
          </motion.div>
        ))}
      </div>
    </motion.section>
  );
}
