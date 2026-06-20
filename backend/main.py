"""
API FastAPI pour le problème de transport.

Expose deux endpoints distincts, correspondant aux deux étapes du projet :
- POST /balas-hammer   : calcule une solution de base réalisable (heuristique)
- POST /stepping-stone : optimise une allocation existante

Lancement (depuis le dossier backend/) :
    uvicorn main:app --reload

Documentation interactive générée automatiquement par FastAPI :
    http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

from algo.transport import ProblemeTransport
from algo.balas_hammer import balas_hammer
from algo.stepping_stone import stepping_stone

from schemas import (
    ProblemeInput,
    BalasHammerResponse,
    SteppingStoneRequest,
    SteppingStoneResponse,
)


app = FastAPI(
    title="API Problème de Transport",
    description="Résolution du problème de transport via Balas-Hammer (solution de base) et Stepping Stone (optimisation).",
    version="1.0.0",
)

# CORS : autorise le frontend React (en dev, sur localhost:3000 ou 5173)
# à appeler cette API depuis un domaine différent.
# En production, remplacer "*" par l'URL exacte du frontend déployé.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    """Endpoint de vérification que l'API est en ligne."""
    return {"status": "ok"}


@app.post("/balas-hammer", response_model=BalasHammerResponse)
def resoudre_balas_hammer(payload: ProblemeInput):
    """
    Calcule une solution de base réalisable via la méthode Balas-Hammer
    (méthode des pénalités / Vogel).

    Équilibre automatiquement le problème si offre != demande (ajout
    d'une source ou destination fictive à coût nul), et renvoie cette
    version équilibrée pour que le frontend puisse la transmettre
    telle quelle à /stepping-stone.
    """
    try:
        payload.valider_dimensions()
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    n_lignes_avant = len(payload.couts)
    n_colonnes_avant = len(payload.couts[0])

    probleme = ProblemeTransport(
        couts=[row[:] for row in payload.couts],
        offre=payload.offre[:],
        demande=payload.demande[:],
    )

    try:
        allocation = balas_hammer(probleme)
    except Exception as exc:
        # Filet de sécurité : toute erreur inattendue dans l'algorithme
        # est renvoyée comme une 500 explicite plutôt qu'un crash silencieux.
        raise HTTPException(status_code=500, detail=f"Erreur lors du calcul Balas-Hammer : {exc}")

    a_ete_equilibre = (
        len(probleme.couts) != n_lignes_avant
        or len(probleme.couts[0]) != n_colonnes_avant
    )

    return BalasHammerResponse(
        allocation=allocation,
        cout_total=probleme.cout_total(allocation),
        couts_equilibres=probleme.couts,
        offre_equilibree=probleme.offre,
        demande_equilibree=probleme.demande,
        a_ete_equilibre=a_ete_equilibre,
    )


@app.post("/stepping-stone", response_model=SteppingStoneResponse)
def optimiser_stepping_stone(payload: SteppingStoneRequest):
    """
    Optimise une allocation existante via la méthode Stepping Stone.

    Le problème (couts, offre, demande) fourni ici doit déjà être
    équilibré (typiquement : les valeurs *_equilibre* renvoyées par
    /balas-hammer), sans quoi les contraintes offre/demande de
    l'allocation initiale ne correspondront pas et le résultat sera
    incohérent.
    """
    if len(payload.couts) != len(payload.offre):
        raise HTTPException(
            status_code=422,
            detail=f"Le nombre de lignes de couts ({len(payload.couts)}) doit "
                   f"correspondre au nombre de sources dans offre ({len(payload.offre)}).",
        )
    if not payload.couts or len(payload.couts[0]) != len(payload.demande):
        raise HTTPException(
            status_code=422,
            detail="Le nombre de colonnes de couts doit correspondre au nombre de destinations dans demande.",
        )
    if len(payload.allocation_initiale) != len(payload.couts) or any(
        len(row) != len(payload.couts[0]) for row in payload.allocation_initiale
    ):
        raise HTTPException(
            status_code=422,
            detail="Les dimensions de allocation_initiale doivent correspondre à celles de couts.",
        )

    probleme = ProblemeTransport(
        couts=[row[:] for row in payload.couts],
        offre=payload.offre[:],
        demande=payload.demande[:],
    )

    allocation_initiale = [row[:] for row in payload.allocation_initiale]
    cout_initial = probleme.cout_total(allocation_initiale)

    try:
        allocation_optimisee = stepping_stone(probleme, allocation_initiale)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'optimisation Stepping Stone : {exc}")

    return SteppingStoneResponse(
        allocation=allocation_optimisee,
        cout_total=probleme.cout_total(allocation_optimisee),
        cout_initial=cout_initial,
    )