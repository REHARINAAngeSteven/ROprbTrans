"""
Schémas Pydantic pour l'API du problème de transport.

Ces modèles définissent le contrat de données entre le backend FastAPI
et le frontend React : ce que le frontend doit envoyer (Request) et ce
qu'il peut attendre en retour (Response).
"""

from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


Matrix = List[List[float]]


class ProblemeInput(BaseModel):
    """
    Données brutes du problème de transport, telles que saisies côté
    frontend (avant tout équilibrage offre/demande).
    """

    couts: Matrix = Field(..., description="Matrice des coûts unitaires (lignes = sources, colonnes = destinations)")
    offre: List[float] = Field(..., description="Capacités des sources")
    demande: List[float] = Field(..., description="Besoins des destinations")

    @field_validator("couts")
    @classmethod
    def couts_non_vide(cls, v: Matrix) -> Matrix:
        if not v or not v[0]:
            raise ValueError("La matrice des coûts ne peut pas être vide.")
        longueur = len(v[0])
        if any(len(row) != longueur for row in v):
            raise ValueError("Toutes les lignes de la matrice des coûts doivent avoir la même longueur.")
        return v

    def valider_dimensions(self) -> None:
        """
        Vérifie que les dimensions de couts/offre/demande sont cohérentes
        entre elles. Séparé du validator Pydantic car il faut accéder à
        plusieurs champs en même temps (model_validator serait l'autre option).
        """
        if len(self.couts) != len(self.offre):
            raise ValueError(
                f"Le nombre de lignes de couts ({len(self.couts)}) doit "
                f"correspondre au nombre de sources dans offre ({len(self.offre)})."
            )
        if len(self.couts[0]) != len(self.demande):
            raise ValueError(
                f"Le nombre de colonnes de couts ({len(self.couts[0])}) doit "
                f"correspondre au nombre de destinations dans demande ({len(self.demande)})."
            )


class BalasHammerResponse(BaseModel):
    """Réponse de l'endpoint /balas-hammer."""

    allocation: Matrix = Field(..., description="Solution de base réalisable")
    cout_total: float = Field(..., description="Coût total de cette allocation")
    couts_equilibres: Matrix = Field(..., description="Matrice des coûts après équilibrage éventuel")
    offre_equilibree: List[float] = Field(..., description="Offre après équilibrage éventuel")
    demande_equilibree: List[float] = Field(..., description="Demande après équilibrage éventuel")
    a_ete_equilibre: bool = Field(..., description="True si une ligne/colonne fictive a été ajoutée")


class SteppingStoneRequest(BaseModel):
    """
    Requête de l'endpoint /stepping-stone.

    Le frontend doit fournir le problème déjà équilibré (couts_equilibres,
    offre_equilibree, demande_equilibree renvoyés par /balas-hammer) ainsi
    que l'allocation de départ à optimiser.
    """

    couts: Matrix = Field(..., description="Matrice des coûts (déjà équilibrée)")
    offre: List[float] = Field(..., description="Offre (déjà équilibrée)")
    demande: List[float] = Field(..., description="Demande (déjà équilibrée)")
    allocation_initiale: Matrix = Field(..., description="Allocation de départ à optimiser (ex: résultat de Balas-Hammer)")


class SteppingStoneResponse(BaseModel):
    """Réponse de l'endpoint /stepping-stone."""

    allocation: Matrix = Field(..., description="Allocation optimisée")
    cout_total: float = Field(..., description="Coût total après optimisation")
    cout_initial: float = Field(..., description="Coût total avant optimisation, pour calculer le gain côté frontend")


class ErrorResponse(BaseModel):
    """Format d'erreur uniforme renvoyé par l'API."""

    detail: str