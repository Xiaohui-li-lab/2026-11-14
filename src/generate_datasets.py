"""
Generate all datasets used in the paper.

Datasets produced:
1. cdld_concepts.csv - Conceptual Decomposition Level Dataset (200 concepts).
2. ddm_cases.csv - Author's DDM case library.
3. concept_lockin_scores.csv - Pre-computed lock-in scores by concept type.
"""

import pandas as pd
import numpy as np
import os

CONCEPT_DECOMPOSITIONS = {
    'justice': {
        'type': 'positive_value',
        'levels': [
            ['justice'],
            ['fairness', 'rights', 'obligations', 'punishment', 'compassion'],
            ['equality', 'reciprocity', 'protection', 'restoration', 'empathy']
        ]
    },
    'love': {
        'type': 'positive_value',
        'levels': [
            ['love'],
            ['attachment', 'care', 'intimacy', 'commitment', 'empathy'],
            ['neurochemistry', 'bonding', 'trust', 'sacrifice', 'understanding']
        ]
    },
    'purity': {
        'type': 'positive_value',
        'levels': [
            ['purity'],
            ['cleanliness', 'innocence', 'separation', 'holiness'],
            ['absence_of_contaminant', 'moral_intention', 'boundary_maintenance']
        ]
    },
    'Amitabha': {
        'type': 'positive_value',
        'levels': [
            ['Amitabha'],
            ['infinite light', 'boundless compassion', 'pure land'],
            ['photon', 'awareness', 'intention', 'radiance']
        ]
    },
    'military_force': {
        'type': 'state_force',
        'levels': [
            ['military force'],
            ['violence', 'organization', 'threat', 'domination'],
            ['fear', 'hierarchy', 'weapon', 'territory']
        ]
    },
    'nuclear_deterrence': {
        'type': 'state_force',
        'levels': [
            ['nuclear deterrence'],
            ['mutual destruction', 'threat credibility', 'arsenal'],
            ['fear', 'balance_of_power', 'annihilation_potential']
        ]
    },
    'sensation': {
        'type': 'personal_psychological',
        'levels': [
            ['sensation'],
            ['perception', 'affect', 'bodily_state', 'attention'],
            ['receptor_activation', 'neural_signal', 'valence']
        ]
    },
    'memory': {
        'type': 'personal_psychological',
        'levels': [
            ['memory'],
            ['encoding', 'storage', 'retrieval', 'consolidation'],
            ['synaptic_change', 'pattern_reactivation', 'context']
        ]
    },
    'first_impression': {
        'type': 'personal_psychological',
        'levels': [
            ['first impression'],
            ['appearance', 'behavior', 'context', 'prior_expectation'],
            ['facial_features', 'movement', 'social_category', 'emotional_tag']
        ]
    },
    'democracy': {
        'type': 'socio_political',
        'levels': [
            ['democracy'],
            ['voting', 'representation', 'rule_of_law', 'public_deliberation'],
            ['election', 'accountability', 'rights_protection', 'participation']
        ]
    },
    'photon': {
        'type': 'physical_basic',
        'levels': [
            ['photon'],
            ['quantum_of_light', 'electromagnetic_field_excitation'],
            ['irreducible_at_current_physics_level']
        ]
    },
    'electron': {
        'type': 'physical_basic',
        'levels': [
            ['electron'],
            ['lepton', 'electric_charge', 'spin'],
            ['irreducible_at_current_physics_level']
        ]
    },
    'quark': {
        'type': 'physical_basic',
        'levels': [
            ['quark'],
            ['fundamental_fermion', 'color_charge', 'strong_interaction'],
            ['irreducible_at_current_physics_level']
        ]
    },
}

def flatten_decompositions():
    """Flatten hierarchical decompositions into long-format CSV rows."""
    rows = []
    concept_id = 0
    for concept, data in CONCEPT_DECOMPOSITIONS.items():
        levels = data['levels']
        ctype = data['type']
        for level_idx, units in enumerate(levels):
            for unit in units:
                parent = concept if level_idx == 0 else levels[level_idx - 1][0]
                is_leaf = (level_idx == len(levels) - 1)
                rows.append({
                    'concept_id': concept_id,
                    'root_concept': concept,
                    'concept_type': ctype,
                    'level': level_idx,
                    'node': unit,
                    'parent': parent,
                    'is_leaf': is_leaf
                })
        concept_id += 1
    return pd.DataFrame(rows)

def generate_full_cdld(n_concepts: int = 200, seed: int = 42) -> pd.DataFrame:
    """
    Generate the Conceptual Decomposition Level Dataset.
    Includes the 13 detailed concepts above plus synthetic concepts
    to reach n_concepts total.
    """
    rng = np.random.default_rng(seed)
    base = flatten_decompositions()
    
    # Add synthetic concepts
    synthetic_types = {
        'positive_value': 60,
        'state_force': 30,
        'personal_psychological': 40,
        'socio_political': 40,
        'physical_basic': 17
    }
    
    concept_id = base['concept_id'].max() + 1 if not base.empty else 0
    synth_rows = []
    
    for ctype, count in synthetic_types.items():
        for i in range(count):
            root = f"{ctype}_concept_{i+1}"
            n_levels = rng.integers(3, 7)
            levels = [[root]]
            for lvl in range(1, n_levels):
                n_units = rng.integers(3, 7)
                units = [f"{root}_L{lvl}_U{u}" for u in range(n_units)]
                levels.append(units)
            
            for level_idx, units in enumerate(levels):
                for unit in units:
                    parent = root if level_idx == 0 else levels[level_idx - 1][0]
                    is_leaf = (level_idx == len(levels) - 1)
                    synth_rows.append({
                        'concept_id': concept_id,
                        'root_concept': root,
                        'concept_type': ctype,
                        'level': level_idx,
                        'node': unit,
                        'parent': parent,
                        'is_leaf': is_leaf
                    })
            concept_id += 1
    
    synth_df = pd.DataFrame(synth_rows)
    full_df = pd.concat([base, synth_df], ignore_index=True)
    return full_df

def generate_ddm_cases() -> pd.DataFrame:
    """Generate DDM case library from the paper."""
    cases = [
        {
            'case_id': 1,
            'target': 'News Broadcast and related group (including author)',
            'method': 'digital divination (upper sign 8)',
            'result': '功名成就栋梁材 (Achievements as a pillar of society)',
            'initial_ddi': 0.35,
            'final_ddi': 0.88,
            'interpretation': 'Locked social-achievement concept decomposed into constructive contribution.'
        },
        {
            'case_id': 2,
            'target': 'Italian girl',
            'method': 'digital divination (middle sign 10)',
            'result': '宛如持灯更觅火；眼前是真 (Like holding a lamp to seek fire; what is before the eyes is real)',
            'initial_ddi': 0.35,
            'final_ddi': 0.76,
            'interpretation': 'Confusion about seeking externals decomposed into recognition of present reality.'
        }
    ]
    return pd.DataFrame(cases)

def generate_lockin_scores() -> pd.DataFrame:
    """Generate concept lock-in score reference table."""
    data = [
        {'concept_type': 'state_force', 'initial_ddi_mean': 0.22, 'initial_ddi_std': 0.05,
         'typical_lock_degree': 0.85, 'examples': 'military force, nuclear deterrence, killing'},
        {'concept_type': 'positive_value', 'initial_ddi_mean': 0.81, 'initial_ddi_std': 0.06,
         'typical_lock_degree': 0.75, 'examples': 'justice, love, purity, Amitabha, God'},
        {'concept_type': 'personal_psychological', 'initial_ddi_mean': 0.75, 'initial_ddi_std': 0.07,
         'typical_lock_degree': 0.70, 'examples': 'sensation, memory, first impression'},
        {'concept_type': 'socio_political', 'initial_ddi_mean': 0.68, 'initial_ddi_std': 0.08,
         'typical_lock_degree': 0.80, 'examples': 'democracy vs dictatorship, love vs hate'},
        {'concept_type': 'physical_basic', 'initial_ddi_mean': 0.06, 'initial_ddi_std': 0.02,
         'typical_lock_degree': 0.95, 'examples': 'photon, electron, quark, neutrino'}
    ]
    return pd.DataFrame(data)

def main():
    save_dir = 'data'
    os.makedirs(save_dir, exist_ok=True)
    
    print("Generating CDLD dataset...")
    cdld = generate_full_cdld(n_concepts=200, seed=42)
    cdld.to_csv(os.path.join(save_dir, 'cdld_concepts.csv'), index=False)
    print(f"  Saved {len(cdld)} rows to cdld_concepts.csv")
    
    print("Generating DDM case library...")
    ddm_cases = generate_ddm_cases()
    ddm_cases.to_csv(os.path.join(save_dir, 'ddm_cases.csv'), index=False)
    print(f"  Saved {len(ddm_cases)} cases to ddm_cases.csv")
    
    print("Generating lock-in score reference...")
    scores = generate_lockin_scores()
    scores.to_csv(os.path.join(save_dir, 'concept_lockin_scores.csv'), index=False)
    print(f"  Saved {len(scores)} rows to concept_lockin_scores.csv")
    
    print("\nAll datasets generated successfully.")

if __name__ == '__main__':
    main()
