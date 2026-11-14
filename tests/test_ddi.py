import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from ddi_calculator import compute_ddi, update_lock_degree

def test_compute_ddi():
    assert compute_ddi(['a', 'b', 'c'], ['x']) == 0.75
    assert compute_ddi([], ['x', 'y']) == 0.0
    assert compute_ddi(['a'], []) == 1.0
    assert compute_ddi([], []) == 0.0

def test_update_lock_degree_bounds():
    L = update_lock_degree(0.5, 0.05, 0.12, 0.5, 1.0, 0.5)
    assert 0.0 <= L <= 1.0
