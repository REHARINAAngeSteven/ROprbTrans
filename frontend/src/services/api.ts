// services/api.ts
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

// Données brutes du problème, telles que saisies par l'utilisateur,
// avant tout équilibrage offre/demande côté backend.
export interface TransportProblem {
  couts: number[][];
  offre: number[];
  demande: number[];
}

// Réponse de POST /balas-hammer.
// couts_equilibres / offre_equilibree / demande_equilibree doivent être
// réutilisés tels quels pour l'appel suivant à /stepping-stone, car le
// backend peut avoir ajouté une ligne ou colonne fictive si offre != demande.
export interface BalasHammerResponse {
  allocation: number[][];
  cout_total: number;
  couts_equilibres: number[][];
  offre_equilibree: number[];
  demande_equilibree: number[];
  a_ete_equilibre: boolean;
}

// Requête de POST /stepping-stone : reprend le problème équilibré
// renvoyé par /balas-hammer, plus l'allocation de départ à optimiser.
export interface SteppingStoneRequest {
  couts: number[][];
  offre: number[];
  demande: number[];
  allocation_initiale: number[][];
}

// Réponse de POST /stepping-stone.
export interface SteppingStoneResponse {
  allocation: number[][];
  cout_total: number;
  cout_initial: number;
}

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const solveBalasHammer = async (
  problem: TransportProblem
): Promise<BalasHammerResponse> => {
  try {
    const response = await api.post<BalasHammerResponse>('/balas-hammer', problem);
    return response.data;
  } catch (error) {
    console.error('Error solving with Balas-Hammer:', error);
    throw error;
  }
};

export const solveSteppingStone = async (
  problem: SteppingStoneRequest
): Promise<SteppingStoneResponse> => {
  try {
    const response = await api.post<SteppingStoneResponse>('/stepping-stone', problem);
    return response.data;
  } catch (error) {
    console.error('Error solving with Stepping Stone:', error);
    throw error;
  }
};

export default api;