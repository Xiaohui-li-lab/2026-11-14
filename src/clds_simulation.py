"""
Conceptual Lock-in and Decomposition Simulation (CLDS).

Agent-based model implementing the dynamics described in the paper:
- 1000 agents on a 100x100 grid.
- Five concept types: state_force, positive_value, personal_psychological,
  socio_political, physical_basic.
- Each step: information input drives lock-in or decomposition.
- Every ddm_interval steps: DDM perturbation is applied.
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from typing import List, Dict, Tuple
import os

CONCEPT_TYPES = {
    'state_force': {
        'initial_ddi_mean': 0.22,
        'initial_ddi_std': 0.05,
        'examples': ['military force', 'nuclear deterrence', 'killing', 'coercive force']
    },
    'positive_value': {
        'initial_ddi_mean': 0.81,
        'initial_ddi_std': 0.06,
        'examples': ['justice', 'love', 'purity', 'democracy', 'Amitabha', 'God']
    },
    'personal_psychological': {
        'initial_ddi_mean': 0.75,
        'initial_ddi_std': 0.07,
        'examples': ['sensation', 'memory', 'first impression', 'good and evil']
    },
    'socio_political': {
        'initial_ddi_mean': 0.68,
        'initial_ddi_std': 0.08,
        'examples': ['democracy vs dictatorship', 'love vs hate', 'victory vs defeat']
    },
    'physical_basic': {
        'initial_ddi_mean': 0.06,
        'initial_ddi_std': 0.02,
        'examples': ['photon', 'electron', 'quark', 'neutrino']
    },
}

@dataclass
class Concept:
    """A concept carried by an agent."""
    name: str
    concept_type: str
    ddi: float
    lock_degree: float
    free_units: int = 0
    locked_units: int = 0
    
    def __post_init__(self):
        # Initialize unit counts from DDI using base scale of 10 units
        total = 10
        self.free_units = int(round(np.clip(self.ddi, 0, 1) * total))
        self.locked_units = total - self.free_units
        self.lock_degree = np.clip(self.lock_degree, 0.0, 1.0)
        self.recalculate_ddi()
    
    def recalculate_ddi(self):
        total = self.free_units + self.locked_units
        self.ddi = self.free_units / total if total > 0 else 0.0
    
    def lock_step(self, alpha: float, beta: float, info_input: float):
        """One time-step of lock-in/decomposition dynamics."""
        activity = self.ddi  # decomposition activity proportional to openness
        delta = alpha * (1.0 - self.ddi) * info_input - beta * activity
        self.lock_degree = np.clip(self.lock_degree + delta, 0.0, 1.0)
        
        if delta > 0:
            # Locking: free units become locked
            amount = min(self.free_units, max(1, int(np.ceil(delta * 2))))
            self.free_units -= amount
            self.locked_units += amount
        elif delta < 0:
            # Decomposition: locked units become free
            amount = min(self.locked_units, max(1, int(np.ceil(-delta * 2))))
            self.locked_units -= amount
            self.free_units += amount
        self.recalculate_ddi()
    
    def apply_ddm(self, gamma: float):
        """Apply DDM perturbation: locked units are released."""
        if self.locked_units == 0:
            return
        amount = max(1, int(np.ceil(gamma * self.locked_units)))
        amount = min(amount, self.locked_units)
        self.locked_units -= amount
        self.free_units += amount
        self.lock_degree = np.clip(self.lock_degree - gamma * self.lock_degree, 0.0, 1.0)
        self.recalculate_ddi()

@dataclass
class Agent:
    """Cognitive agent carrying multiple concepts."""
    agent_id: int
    x: int = 0
    y: int = 0
    concepts: Dict[str, Concept] = field(default_factory=dict)
    
    def step(self, alpha: float, beta: float, info_input: float):
        for concept in self.concepts.values():
            concept.lock_step(alpha, beta, info_input)
    
    def apply_ddm(self, gamma: float):
        for concept in self.concepts.values():
            concept.apply_ddm(gamma)

class CLDS:
    """
    Conceptual Lock-in and Decomposition Simulation.
    
    Parameters
    ----------
    n_agents : int
        Number of cognitive agents.
    grid_size : tuple
        Size of the spatial grid.
    alpha : float
        Lock-in reinforcement coefficient.
    beta : float
        Decomposition coefficient.
    gamma : float
        DDM perturbation strength.
    n_steps : int
        Number of simulation steps.
    ddm_interval : int
        Interval between DDM interventions.
    seed : int
        Random seed for reproducibility.
    """
    
    def __init__(self,
                 n_agents: int = 1000,
                 grid_size: Tuple[int, int] = (100, 100),
                 alpha: float = 0.05,
                 beta: float = 0.12,
                 gamma: float = 0.30,
                 n_steps: int = 500,
                 ddm_interval: int = 100,
                 seed: int = 42):
        self.n_agents = n_agents
        self.grid_size = grid_size
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.n_steps = n_steps
        self.ddm_interval = ddm_interval
        self.rng = np.random.default_rng(seed)
        self.agents: List[Agent] = []
        self.history: pd.DataFrame = pd.DataFrame()
        self._init_agents()
    
    def _init_agents(self):
        positions = self.rng.integers(
            0, min(self.grid_size), size=(self.n_agents, 2)
        )
        for i in range(self.n_agents):
            x, y = positions[i]
            agent = Agent(agent_id=i, x=int(x), y=int(y))
            for ctype, params in CONCEPT_TYPES.items():
                ddi = np.clip(
                    self.rng.normal(params['initial_ddi_mean'], params['initial_ddi_std']),
                    0.0, 1.0
                )
                lock = 1.0 - ddi
                agent.concepts[ctype] = Concept(
                    name=ctype, concept_type=ctype, ddi=ddi, lock_degree=lock
                )
            self.agents.append(agent)
    
    def reset(self, seed: int = None):
        """Re-initialize the simulation."""
        if seed is not None:
            self.rng = np.random.default_rng(seed)
        self.agents = []
        self.history = pd.DataFrame()
        self._init_agents()
    
    def run(self, apply_ddm: bool = True) -> pd.DataFrame:
        """
        Run the simulation.
        
        Parameters
        ----------
        apply_ddm : bool
            Whether to apply DDM perturbations.
        
        Returns
        -------
        pd.DataFrame
            Time series of mean DDI and lock degree per concept type.
        """
        records = []
        for step in range(self.n_steps):
            info_input = float(self.rng.normal(1.0, 0.2))
            for agent in self.agents:
                agent.step(self.alpha, self.beta, info_input)
                if apply_ddm and (step + 1) % self.ddm_interval == 0:
                    agent.apply_ddm(self.gamma)
            
            for ctype in CONCEPT_TYPES.keys():
                ddis = [a.concepts[ctype].ddi for a in self.agents]
                locks = [a.concepts[ctype].lock_degree for a in self.agents]
                records.append({
                    'step': step + 1,
                    'concept_type': ctype,
                    'mean_ddi': float(np.mean(ddis)),
                    'std_ddi': float(np.std(ddis)),
                    'mean_lock_degree': float(np.mean(locks)),
                    'std_lock_degree': float(np.std(locks)),
                    'ddm_applied': apply_ddm
                })
        self.history = pd.DataFrame(records)
        return self.history
    
    def get_summary(self) -> pd.DataFrame:
        """Return final-step summary statistics."""
        if self.history.empty:
            raise ValueError("Run simulation before getting summary.")
        final = self.history[self.history['step'] == self.n_steps]
        return final[['concept_type', 'mean_ddi', 'std_ddi']].copy()

def run_clds_demo(save_dir: str = 'data'):
    """Run demo simulation and save results."""
    os.makedirs(save_dir, exist_ok=True)
    
    print("Running CLDS without DDM intervention...")
    sim_no_ddm = CLDS(seed=42)
    df_no_ddm = sim_no_ddm.run(apply_ddm=False)
    summary_no_ddm = sim_no_ddm.get_summary()
    summary_no_ddm['condition'] = 'no_ddm'
    
    print("Running CLDS with DDM intervention...")
    sim_ddm = CLDS(seed=2025)
    df_ddm = sim_ddm.run(apply_ddm=True)
    summary_ddm = sim_ddm.get_summary()
    summary_ddm['condition'] = 'ddm'
    
    # Combine time series
    df_combined = pd.concat([df_no_ddm, df_ddm], ignore_index=True)
    df_combined.to_csv(os.path.join(save_dir, 'clds_results.csv'), index=False)
    
    # Table matching paper: initial, no-intervention final, DDM final
    initial = []
    for ctype, params in CONCEPT_TYPES.items():
        initial.append({
            'concept_type': ctype,
            'initial_ddi_mean': params['initial_ddi_mean'],
            'initial_ddi_std': params['initial_ddi_std']
        })
    df_initial = pd.DataFrame(initial)
    
    df_summary = pd.merge(df_initial, summary_no_ddm, on='concept_type')
    df_summary = pd.merge(df_summary, summary_ddm, on='concept_type',
                          suffixes=('_no_ddm', '_ddm'))
    df_summary.to_csv(os.path.join(save_dir, 'clds_summary.csv'), index=False)
    
    print("\nFinal Summary (matching Table 1 in paper):")
    print(df_summary.to_string(index=False))
    return df_combined, df_summary

if __name__ == '__main__':
    run_clds_demo()
