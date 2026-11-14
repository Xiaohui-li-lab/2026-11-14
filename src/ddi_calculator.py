"""
Degree of Decomposability Index (DDI) calculator.

Implements equations (5), (6), and (7) from the paper:
- DDI(C) = |D(C)| / (|D(C)| + L(C))
- Lock-degree dynamics: dL/dt = alpha * (1 - DDI) * I(t) - beta * A(t)
"""

import numpy as np
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class ConceptDecomposition:
    """Container for a concept's decomposition structure."""
    concept_name: str
    concept_type: str
    decomposition_units: List[str]
    locked_units: List[str]
    
    @property
    def ddi(self) -> float:
        """Compute DDI."""
        d = len(self.decomposition_units)
        l = len(self.locked_units)
        if d + l == 0:
            return 0.0
        return d / (d + l)
    
    def decompose(self, n_units: int = 1):
        """Move locked units into decomposition units."""
        n = min(n_units, len(self.locked_units))
        moved = self.locked_units[:n]
        self.locked_units = self.locked_units[n:]
        self.decomposition_units.extend(moved)
    
    def lock(self, n_units: int = 1):
        """Move decomposition units into locked units."""
        n = min(n_units, len(self.decomposition_units))
        moved = self.decomposition_units[:n]
        self.decomposition_units = self.decomposition_units[n:]
        self.locked_units.extend(moved)

def compute_ddi(decomposition_units: List[str], locked_units: List[str]) -> float:
    """
    Compute Degree of Decomposability Index.
    
    Parameters
    ----------
    decomposition_units : list
        Currently decomposed minimal/sub-concept units.
    locked_units : list
        Locked units that resist decomposition.
    
    Returns
    -------
    float
        DDI in [0, 1].
    """
    d = len(decomposition_units)
    l = len(locked_units)
    if d + l == 0:
        return 0.0
    return d / (d + l)

def update_lock_degree(lock_degree: float, alpha: float, beta: float,
                       ddi: float, information_input: float,
                       decomposition_activity: float) -> float:
    """
    Update lock degree according to equation (6).
    
    dL/dt = alpha * (1 - DDI) * I(t) - beta * A(t)
    
    Parameters
    ----------
    lock_degree : float
        Current lock degree in [0, 1].
    alpha : float
        Environmental reinforcement coefficient.
    beta : float
        Consciousness-awareness / decomposition coefficient.
    ddi : float
        Current DDI in [0, 1].
    information_input : float
        Information input intensity I(t).
    decomposition_activity : float
        Decomposition activity A(t).
    
    Returns
    -------
    float
        Updated lock degree in [0, 1].
    """
    delta = alpha * (1.0 - ddi) * information_input - beta * decomposition_activity
    new_lock = np.clip(lock_degree + delta, 0.0, 1.0)
    return new_lock

def hierarchical_decomposition(concept: str, levels: int = 5) -> Dict[str, any]:
    """
    Generate a sample hierarchical decomposition tree for a concept.
    This is a utility for dataset generation.
    """
    # Placeholder: actual decompositions are defined in generate_datasets.py
    return {
        'concept': concept,
        'levels': levels,
        'note': 'See generate_datasets.py for full hierarchical structures.'
    }
