from typing import List, Dict, Any
from algo.transport import ProblemeTransport
from algo.balas_hammer import balas_hammer

def solve_balas_hammer(couts: List[List[int]], offre: List[int], demande: List[int]) -> tuple:
    """
    Exécute l'algorithme de Balas-Hammer avec suivi des étapes.
    Retourne (allocation, cout_total, steps)
    """
    
    # Création du problème
    p = ProblemeTransport(couts=couts, offre=offre, demande=demande)
    p.equilibrer()
    
    steps = []
    
    # Suivi des étapes (personnalisation nécessaire de balas_hammer)
    # Pour l'instant, on exécute simplement l'algorithme
    # Plus tard, on pourra modifier balas_hammer.py pour retourner les étapes
    
    allocation = balas_hammer(p)
    cout_total = p.cout_total(allocation)
    
    # Ajouter des étapes de simulation
    steps.append({
        "step_type": "initialisation",
        "description": "Problème équilibré et prêt pour Balas-Hammer",
        "data": {
            "offre": offre,
            "demande": demande,
            "couts": couts
        }
    })
    
    return allocation, cout_total, steps