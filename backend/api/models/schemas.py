from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum

class SolveStep(BaseModel):
    """Étape intermédiaire de la résolution"""
    step_type: str
    description: str
    data: Dict[str, Any]
    iteration: Optional[int] = None

class BalasHammerRequest(BaseModel):
    """Requête pour l'algorithme de Balas-Hammer"""
    couts: List[List[int]] = Field(..., description="Matrice des coûts de transport")
    offre: List[int] = Field(..., description="Offre disponible à chaque source")
    demande: List[int] = Field(..., description="Demande à chaque destination")
    
    class Config:
        json_schema_extra = {
            "example": {
                "couts": [[8, 6, 10], [9, 12, 13], [14, 9, 16]],
                "offre": [40, 30, 50],
                "demande": [35, 45, 40]
            }
        }

class BalasHammerResponse(BaseModel):
    """Réponse de l'algorithme de Balas-Hammer"""
    allocation: List[List[int]]
    cout_total: int
    feasibility: bool
    steps: List[SolveStep]
    iterations: int

class SteppingStoneRequest(BaseModel):
    """Requête pour l'algorithme de Stepping Stone"""
    couts: List[List[int]] = Field(..., description="Matrice des coûts de transport")
    allocation_initial: List[List[int]] = Field(..., description="Allocation initiale (souvent issue de Balas-Hammer)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "couts": [[8, 6, 10], [9, 12, 13], [14, 9, 16]],
                "allocation_initial": [[35, 5, 0], [0, 30, 0], [0, 10, 40]]
            }
        }

class SteppingStoneResponse(BaseModel):
    """Réponse de l'algorithme de Stepping Stone"""
    allocation_optimale: List[List[int]]
    cout_initial: int
    cout_optimal: int
    amelioration: int
    steps: List[SolveStep]
    iterations: int

class HealthResponse(BaseModel):
    status: str
    version: str