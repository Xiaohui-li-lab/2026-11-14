"""
Divination-based Decomposition Method (DDM) benchmark simulator.

Implements the double-blind benchmark described in the paper:
- 1000 real-life events.
- 5 trained diviners + 5 control subjects per event.
- Hit Rate (HR), Information Gain (IG), Delta-DDI metrics.
- Chi-square test and Bayes factor for H0 vs H1.
"""

import numpy as np
import pandas as pd
from scipy import stats
from scipy.special import comb, beta as beta_func, betainc
from typing import Dict
import os

def simulate_ddm_benchmark(n_events: int = 1000,
                           n_diviners: int = 5,
                           n_controls: int = 5,
                           diviner_accuracy: float = 0.75,
                           control_accuracy: float = 0.50,
                           seed: int = 42) -> pd.DataFrame:
    """
    Simulate a double-blind DDM benchmark.
    
    Parameters
    ----------
    n_events : int
        Number of events to predict.
    n_diviners, n_controls : int
        Number of subjects per group.
    diviner_accuracy : float
        Probability that a diviner's binary prediction matches ground truth.
    control_accuracy : float
        Probability that a control subject's binary prediction matches ground truth.
    seed : int
        Random seed.
    
    Returns
    -------
    pd.DataFrame
        Long-format benchmark results.
    """
    rng = np.random.default_rng(seed)
    records = []
    
    for event_id in range(n_events):
        # Ground truth as binary outcome
        true_outcome = int(rng.integers(0, 2))
        
        for div_id in range(n_diviners):
            pred = int(rng.random() < diviner_accuracy)
            records.append({
                'event_id': event_id,
                'subject_type': 'diviner',
                'subject_id': div_id,
                'true_outcome': true_outcome,
                'prediction': pred,
                'hit': int(pred == true_outcome)
            })
        
        for ctrl_id in range(n_controls):
            pred = int(rng.random() < control_accuracy)
            records.append({
                'event_id': event_id,
                'subject_type': 'control',
                'subject_id': ctrl_id,
                'true_outcome': true_outcome,
                'prediction': pred,
                'hit': int(pred == true_outcome)
            })
    
    return pd.DataFrame(records)

def binomial_bf10(k: int, n: int, theta0: float = 0.5) -> float:
    """
    Compute approximate Bayes factor BF_10 for binomial test.
    
    H0: theta = theta0
    H1: theta ~ Uniform(theta0, 1)
    """
    # P(data | H0)
    log_p_h0 = np.log(comb(n, k)) + k * np.log(theta0) + (n - k) * np.log(1 - theta0)
    p_h0 = np.exp(log_p_h0)
    
    # P(data | H1) = C(n,k) * 2 * integral_{theta0}^{1} theta^k (1-theta)^(n-k) dtheta
    B_full = beta_func(k + 1, n - k + 1)
    I_theta0 = betainc(k + 1, n - k + 1, theta0)
    integral = B_full * (1.0 - I_theta0)
    p_h1 = comb(n, k) * 2.0 * integral
    
    return p_h1 / p_h0

def analyze_ddm_benchmark(df: pd.DataFrame) -> Dict:
    """
    Analyze benchmark results.
    
    Returns hit rates, chi-square statistic, p-value, and Bayes factor.
    """
    div = df[df['subject_type'] == 'diviner']
    ctrl = df[df['subject_type'] == 'control']
    
    div_hits = int(div['hit'].sum())
    div_total = len(div)
    ctrl_hits = int(ctrl['hit'].sum())
    ctrl_total = len(ctrl)
    
    div_rate = div_hits / div_total
    ctrl_rate = ctrl_hits / ctrl_total
    
    # Information Gain: log2(P_div / P_control)
    eps = 1e-10
    info_gain = np.log2((div_rate + eps) / (ctrl_rate + eps))
    
    # Chi-square test on contingency table
    contingency = np.array([
        [div_hits, div_total - div_hits],
        [ctrl_hits, ctrl_total - ctrl_hits]
    ])
    chi2, p_value, dof, expected = stats.chi2_contingency(contingency)
    
    # Bayes factor H1 (DDM >= 70%) vs H0 (chance 50%)
    bf10 = binomial_bf10(div_hits, div_total, theta0=0.5)
    
    conclusion = 'H1 supported' if (p_value < 0.001 and bf10 > 100) else 'H0 not rejected'
    
    return {
        'diviner_hit_rate': div_rate,
        'control_hit_rate': ctrl_rate,
        'diviner_hits': div_hits,
        'diviner_total': div_total,
        'control_hits': ctrl_hits,
        'control_total': ctrl_total,
        'information_gain': info_gain,
        'chi2': chi2,
        'p_value': p_value,
        'bayes_factor_10': bf10,
        'conclusion': conclusion
    }

def run_ddm_demo(save_dir: str = 'data'):
    """Run DDM benchmark demo and save results."""
    os.makedirs(save_dir, exist_ok=True)
    
    print("Simulating DDM benchmark...")
    df = simulate_ddm_benchmark(
        n_events=1000, n_diviners=5, n_controls=5,
        diviner_accuracy=0.75, control_accuracy=0.50, seed=123
    )
    df.to_csv(os.path.join(save_dir, 'ddm_benchmark_results.csv'), index=False)
    
    print("Analyzing results...")
    results = analyze_ddm_benchmark(df)
    
    print("\nDDM Benchmark Results:")
    for key, val in results.items():
        print(f"  {key}: {val}")
    
    return df, results

if __name__ == '__main__':
    run_ddm_demo()
