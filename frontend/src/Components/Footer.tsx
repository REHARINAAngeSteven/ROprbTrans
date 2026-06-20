// src/Components/Footer.tsx
import { motion } from 'framer-motion';

export function Footer() {
  const year = new Date().getFullYear();

  return (
    <motion.footer
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      className="bg-blue-900 text-white mt-16"
    >
      <div className="max-w-7xl mx-auto px-6 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
          <div>
            <h3 className="font-bold text-lg mb-3">Problème de Transport</h3>
            <p className="text-blue-100 text-sm">
              Application pédagogique pour l'optimisation des réseaux de distribution
            </p>
          </div>

          <div>
            <h3 className="font-bold text-lg mb-3">Algorithmes</h3>
            <ul className="text-blue-100 text-sm space-y-1">
              <li>• Balas-Hammer (Solution initiale)</li>
              <li>• Stepping Stone (Optimisation)</li>
              <li>• Calcul des coûts réduits</li>
            </ul>
          </div>

          <div>
            <h3 className="font-bold text-lg mb-3">Recherche Opérationnelle</h3>
            <p className="text-blue-100 text-sm">
              Optimisation mathématique pour les problèmes de logistique
            </p>
          </div>
        </div>

        <div className="border-t border-blue-700 pt-8 text-center text-blue-100 text-sm">
          <p>
            Optimisation du Problème de Transport © {year} - Recherche Opérationnelle
          </p>
          <p className="mt-2">v2.0</p>
        </div>
      </div>
    </motion.footer>
  );
}
