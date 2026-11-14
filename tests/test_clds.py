import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from clds_simulation import CLDS

def test_clds_initialization():
    sim = CLDS(n_agents=10, grid_size=(10, 10), n_steps=5, seed=1)
    assert len(sim.agents) == 10
    assert len(sim.agents[0].concepts) == 5

def test_clds_run():
    sim = CLDS(n_agents=10, n_steps=20, seed=1)
    df = sim.run(apply_ddm=True)
    assert not df.empty
    assert 'mean_ddi' in df.columns
    assert df['step'].max() == 20
