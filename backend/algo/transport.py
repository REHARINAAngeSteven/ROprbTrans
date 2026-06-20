from dataclasses import dataclass
from typing import List

Matrix = List[List[float]]


@dataclass
class ProblemeTransport:
    couts: Matrix
    offre: List[float]
    demande: List[float]

    def equilibrer(self):
        total_o = sum(self.offre)
        total_d = sum(self.demande)

        if total_o < total_d:
            diff = total_d - total_o
            self.couts.append([0] * len(self.couts[0]))
            self.offre.append(diff)

        elif total_o > total_d:
            diff = total_o - total_d
            for row in self.couts:
                row.append(0)
            self.demande.append(diff)

    def cout_total(self, allocation: Matrix) -> float:
        return sum(
            c * x
            for row_c, row_x in zip(self.couts, allocation)
            for c, x in zip(row_c, row_x)
        )