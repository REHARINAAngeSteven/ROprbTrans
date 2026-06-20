from typing import List, Dict, Any
from algo.transport import ProblemeTransport
from algo.stepping_stone import stepping_stone

def solve_stepping_stone(couts: List[List[int]], allocation_initial: List[List[int]]) -> tuple:
    """
    Exécute l'algorithme de Stepping Stone avec suivi des étapes.
    Retourne (allocation_optimale, cout_initial, cout_optimal, amelioration, steps)
    """
    
    # Création du problème
    n = len(couts)
    m = len(couts[0])
    offre = [sum(row) for row in allocation_initial]
    demande = [sum(col) for col in zip(*allocation_initial)]
    
    p = ProblemeTransport(couts=couts, offre=offre, demande=demande)
    p.equilibrer()
    
    # Calcul du coût initial
    cout_initial = p.cout_total(allocation_initial)
    
    steps = []
    
    # Exécution de Stepping Stone
    allocation_optimale = stepping_stone(p, allocation_initial)
    cout_optimal = p.cout_total(allocation_optimale)
    amelioration = cout_initial - cout_optimal
    
    return allocation_optimale, cout_initial, cout_optimal, amelioration, steps