from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any
import copy

from api.models.schemas import BalasHammerRequest, BalasHammerResponse, SolveStep
from algo.transport import ProblemeTransport
from algo.balas_hammer import balas_hammer

router = APIRouter(prefix="/balas-hammer", tags=["Balas-Hammer"])

def track_balas_hammer_steps(p: ProblemeTransport):
    """
    Version modifiée de balas_hammer avec suivi des étapes.
    """
    p.equilibrer()
    
    n, m = len(p.couts), len(p.couts[0])
    X = [[0] * m for _ in range(n)]
    
    offre = p.offre[:]
    demande = p.demande[:]
    
    lignes = [True] * n
    colonnes = [True] * m
    
    steps = []
    iteration = 0
    
    # Ajouter l'étape initiale
    steps.append(SolveStep(
        step_type="initialisation",
        description="Problème équilibré",
        data={
            "offre": offre,
            "demande": demande,
            "couts": p.couts,
            "taille": f"{n}x{m}"
        },
        iteration=0
    ))
    
    from algo.balas_hammer import calculer_max_penalite, trouver_min_colonne, trouver_min_ligne
    
    while any(offre) and any(demande):
        iteration += 1
        
        choix = calculer_max_penalite(p, lignes, colonnes)
        if choix is None:
            break
        
        type_, idx = choix
        
        if type_ == "ligne":
            i = idx
            j = trouver_min_colonne(p, i, colonnes)
            description = f"Choix de la ligne {i} avec la plus grande pénalité"
        else:
            j = idx
            i = trouver_min_ligne(p, j, lignes)
            description = f"Choix de la colonne {j} avec la plus grande pénalité"
        
        q = min(offre[i], demande[j])
        
        X[i][j] += q
        offre[i] -= q
        demande[j] -= q
        
        # Enregistrer l'étape
        steps.append(SolveStep(
            step_type="affectation",
            description=description,
            data={
                "iteration": iteration,
                "i": i,
                "j": j,
                "quantite": q,
                "offre_restante": offre[:],
                "demande_restante": demande[:],
                "allocation_courante": copy.deepcopy(X)
            },
            iteration=iteration
        ))
        
        if offre[i] == 0:
            lignes[i] = False
        if demande[j] == 0:
            colonnes[j] = False
    
    # Étape finale
    steps.append(SolveStep(
        step_type="finalisation",
        description="Solution complète obtenue",
        data={
            "allocation_finale": X,
            "iterations_total": iteration
        },
        iteration=iteration
    ))
    
    return X, steps, iteration

@router.post("/solve", response_model=BalasHammerResponse, status_code=status.HTTP_200_OK)
async def solve_balas_hammer(request: BalasHammerRequest):
    """
    Résout un problème de transport avec l'algorithme de Balas-Hammer.
    
    - **couts**: Matrice des coûts de transport (n x m)
    - **offre**: Offre disponible à chaque source (taille n)
    - **demande**: Demande à chaque destination (taille m)
    
    Retourne la solution initiale avec les étapes intermédiaires.
    """
    try:
        # Validation des données
        if not request.couts or not request.offre or not request.demande:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Les matrices ne peuvent pas être vides"
            )
        
        if len(request.couts) != len(request.offre):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Le nombre de lignes ({len(request.couts)}) ne correspond pas à l'offre ({len(request.offre)})"
            )
        
        if len(request.couts[0]) != len(request.demande):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Le nombre de colonnes ({len(request.couts[0])}) ne correspond pas à la demande ({len(request.demande)})"
            )
        
        # Création du problème
        p = ProblemeTransport(
            couts=request.couts,
            offre=request.offre,
            demande=request.demande
        )
        
        # Résolution avec suivi
        allocation, steps, iterations = track_balas_hammer_steps(p)
        cout_total = p.cout_total(allocation)
        
        return BalasHammerResponse(
            allocation=allocation,
            cout_total=cout_total,
            feasibility=True,
            steps=steps,
            iterations=iterations
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erreur lors de la résolution: {str(e)}"
        )