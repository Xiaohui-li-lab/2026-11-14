"""
Generate all figures for the paper.

Figures:
1. Conceptual lock-in and decomposition pathway.
2. DCL formalized flow.
3. DDI evolution curves from CLDS.
4. CUPF model diagram.
5. DDM operational flow.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import numpy as np
import pandas as pd
import networkx as nx
import os

plt.style.use('seaborn-v0_8-whitegrid')

def save_figure(fig, name: str, save_dir: str = 'figures'):
    os.makedirs(save_dir, exist_ok=True)
    path = os.path.join(save_dir, name)
    fig.savefig(path, dpi=300, bbox_inches='tight')
    print(f"Saved {path}")
    plt.close(fig)

def figure1_lockin_pathway(save_dir='figures'):
    """Figure 1: Lock-in and decomposition pathway."""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    # Nodes
    nodes = {
        'Open Concept': (1.5, 5),
        'Information Input': (4, 5),
        'Locked Concept': (7, 5),
        'Conscious Awareness': (7, 3),
        'Decomposition': (4, 3),
        'New Concept': (1.5, 3)
    }
    
    colors = {'start': '#4CAF50', 'process': '#2196F3', 'lock': '#F44336', 'new': '#9C27B0'}
    
    for name, (x, y) in nodes.items():
        if name == 'Open Concept':
            color = colors['start']
        elif name == 'Locked Concept':
            color = colors['lock']
        elif name == 'New Concept':
            color = colors['new']
        else:
            color = colors['process']
        box = FancyBboxPatch((x-0.7, y-0.3), 1.4, 0.6,
                             boxstyle="round,pad=0.05",
                             facecolor=color, edgecolor='black', alpha=0.8)
        ax.add_patch(box)
        ax.text(x, y, name, ha='center', va='center', fontsize=10, color='white', weight='bold')
    
    # Arrows
    arrows = [
        ('Open Concept', 'Information Input'),
        ('Information Input', 'Locked Concept'),
        ('Locked Concept', 'Conscious Awareness'),
        ('Conscious Awareness', 'Decomposition'),
        ('Decomposition', 'New Concept'),
        ('New Concept', 'Open Concept')
    ]
    for start, end in arrows:
        ax.annotate('', xy=nodes[end], xytext=nodes[start],
                    arrowprops=dict(arrowstyle='->', color='black', lw=1.5))
    
    ax.set_title('Figure 1 | Conceptual lock-in and decomposition pathway', fontsize=14, weight='bold')
    save_figure(fig, 'figure1_lockin_pathway.png', save_dir)

def figure2_dcl_flow(save_dir='figures'):
    """Figure 2: DCL formalized flow with operators D and R."""
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis('off')
    
    # Boxes
    box_c = FancyBboxPatch((0.5, 1.5), 1.5, 1, boxstyle="round,pad=0.05",
                           facecolor='#E3F2FD', edgecolor='#1565C0', lw=2)
    box_d = FancyBboxPatch((3.0, 1.5), 1.0, 1, boxstyle="round,pad=0.05",
                           facecolor='#FFF3E0', edgecolor='#EF6C00', lw=2)
    box_mu = FancyBboxPatch((5.0, 1.5), 1.5, 1, boxstyle="round,pad=0.05",
                            facecolor='#E8F5E9', edgecolor='#2E7D32', lw=2)
    box_r = FancyBboxPatch((7.5, 1.5), 1.0, 1, boxstyle="round,pad=0.05",
                           facecolor='#FFF3E0', edgecolor='#EF6C00', lw=2)
    box_cp = FancyBboxPatch((9.5, 1.5), 1.5, 1, boxstyle="round,pad=0.05",
                            facecolor='#F3E5F5', edgecolor='#6A1B9A', lw=2)
    
    for box in [box_c, box_d, box_mu, box_r, box_cp]:
        ax.add_patch(box)
    
    ax.text(1.25, 2.0, 'Concept C', ha='center', va='center', fontsize=11, weight='bold')
    ax.text(3.5, 2.0, 'D', ha='center', va='center', fontsize=14, weight='bold')
    ax.text(5.75, 2.0, '{m₁,...,mₙ}', ha='center', va='center', fontsize=10, weight='bold')
    ax.text(8.0, 2.0, 'R', ha='center', va='center', fontsize=14, weight='bold')
    ax.text(10.25, 2.0, "Concept C'", ha='center', va='center', fontsize=11, weight='bold')
    
    # Arrows
    ax.annotate('', xy=(3.0, 2.0), xytext=(2.0, 2.0),
                arrowprops=dict(arrowstyle='->', lw=2, color='black'))
    ax.annotate('', xy=(5.0, 2.0), xytext=(4.0, 2.0),
                arrowprops=dict(arrowstyle='->', lw=2, color='black'))
    ax.annotate('', xy=(7.5, 2.0), xytext=(6.5, 2.0),
                arrowprops=dict(arrowstyle='->', lw=2, color='black'))
    ax.annotate('', xy=(9.5, 2.0), xytext=(8.5, 2.0),
                arrowprops=dict(arrowstyle='->', lw=2, color='black'))
    
    # Equations
    ax.text(5, 3.2, r'$C \xrightarrow{D} \{m_1, ..., m_n\} \xrightarrow{R} C\'$',
            ha='center', fontsize=13)
    
    ax.set_title('Figure 2 | Decomposition-Composition Law formalized flow', fontsize=14, weight='bold')
    save_figure(fig, 'figure2_dcl_flow.png', save_dir)

def figure3_ddi_evolution(clds_results_path='data/clds_results.csv', save_dir='figures'):
    """Figure 3: DDI evolution curves from CLDS simulation."""
    df = pd.read_csv(clds_results_path)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    concept_order = ['state_force', 'positive_value', 'personal_psychological',
                     'socio_political', 'physical_basic']
    palette = ['#F44336', '#4CAF50', '#2196F3', '#FF9800', '#9E9E9E']
    
    for idx, condition in enumerate([False, True]):
        ax = axes[idx]
        sub = df[df['ddm_applied'] == condition]
        for ctype, color in zip(concept_order, palette):
            cdata = sub[sub['concept_type'] == ctype]
            ax.plot(cdata['step'], cdata['mean_ddi'], label=ctype, color=color, lw=2)
            ax.fill_between(cdata['step'],
                            cdata['mean_ddi'] - cdata['std_ddi'],
                            cdata['mean_ddi'] + cdata['std_ddi'],
                            color=color, alpha=0.15)
        ax.set_xlabel('Simulation step', fontsize=12)
        ax.set_ylabel('Mean DDI', fontsize=12)
        ax.set_ylim(0, 1)
        ax.legend(title='Concept type', loc='best')
        title = 'With DDM intervention' if condition else 'No DDM intervention'
        ax.set_title(title, fontsize=13, weight='bold')
    
    fig.suptitle('Figure 3 | DDI evolution across concept types (CLDS simulation)',
                 fontsize=14, weight='bold')
    save_figure(fig, 'figure3_ddi_evolution.png', save_dir)

def figure4_cupf_model(save_dir='figures'):
    """Figure 4: Consciousness as Universal Processing Field model."""
    fig, ax = plt.subplots(figsize=(9, 9))
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Central consciousness field
    center_circle = Circle((0, 0), 0.35, color='#7B1FA2', alpha=0.9, zorder=5)
    ax.add_patch(center_circle)
    ax.text(0, 0, 'Ψ(x,t)', ha='center', va='center', fontsize=16, color='white', weight='bold')
    
    # Orbital domains
    domains = [
        ('Physical', 0.8, 90, '#E53935'),
        ('Psychological', 0.8, 18, '#1E88E5'),
        ('Social', 0.8, -54, '#43A047'),
        ('Spiritual', 0.8, -126, '#FB8C00'),
        ('Imaginary', 0.8, 162, '#8E24AA')
    ]
    
    for label, r, angle, color in domains:
        rad = np.deg2rad(angle)
        x, y = r * np.cos(rad), r * np.sin(rad)
        circle = Circle((x, y), 0.18, color=color, alpha=0.8, zorder=4)
        ax.add_patch(circle)
        ax.text(x, y, label, ha='center', va='center', fontsize=10, color='white', weight='bold')
        ax.annotate('', xy=(0.35*np.cos(rad), 0.35*np.sin(rad)), xytext=(x, y),
                    arrowprops=dict(arrowstyle='->', color=color, lw=2, alpha=0.7))
    
    # Properties
    props = ['Attachment', 'Subtlety', 'Hyper-velocity', 'Commonality']
    for i, prop in enumerate(props):
        angle = -90 + i * 25
        rad = np.deg2rad(angle)
        x, y = 0.55 * np.cos(rad), 0.55 * np.sin(rad)
        ax.text(x, y, prop, ha='center', va='center', fontsize=9,
                bbox=dict(boxstyle='round', facecolor='#FCE4EC', edgecolor='#AD1457'))
    
    ax.set_title('Figure 4 | Consciousness as Universal Processing Field (CUPF)',
                 fontsize=14, weight='bold')
    save_figure(fig, 'figure4_cupf_model.png', save_dir)

def figure5_ddm_flow(save_dir='figures'):
    """Figure 5: DDM operational flow and information-theoretic interpretation."""
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    steps = [
        ('1. Calm state', 2, 7),
        ('2. Focus on event/person/concept', 2, 5.5),
        ('3. Trigger random event', 2, 4),
        ('4. Interpret output', 2, 2.5),
        ('5. Conceptual decomposition achieved', 2, 1)
    ]
    
    for text, x, y in steps:
        box = FancyBboxPatch((x-1.2, y-0.3), 2.4, 0.6,
                             boxstyle="round,pad=0.05",
                             facecolor='#BBDEFB', edgecolor='#1976D2', lw=1.5)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=10, weight='bold')
    
    # Arrows between steps
    for i in range(len(steps) - 1):
        ax.annotate('', xy=(steps[i+1][1], steps[i+1][2] + 0.3),
                    xytext=(steps[i][1], steps[i][2] - 0.3),
                    arrowprops=dict(arrowstyle='->', lw=2, color='#1565C0'))
    
    # Information theory box
    info_box = FancyBboxPatch((5.5, 2.5), 4, 3.5,
                              boxstyle="round,pad=0.1",
                              facecolor='#FFF8E1', edgecolor='#F9A825', lw=2)
    ax.add_patch(info_box)
    ax.text(7.5, 5.5, 'Information-theoretic view', ha='center', fontsize=12, weight='bold')
    ax.text(7.5, 4.8, r'Inject strong perturbation $\eta(t)$', ha='center', fontsize=10)
    ax.text(7.5, 4.2, r'Break locked state $L(C)$', ha='center', fontsize=10)
    ax.text(7.5, 3.6, r'Force reorganization of information', ha='center', fontsize=10)
    ax.text(7.5, 3.0, r'Restore DDI and generate new concepts', ha='center', fontsize=10)
    
    # Arrow from random trigger to info box
    ax.annotate('', xy=(5.5, 4), xytext=(3.2, 4),
                arrowprops=dict(arrowstyle='->', lw=1.5, color='#F9A825', ls='--'))
    
    ax.set_title('Figure 5 | Divination-based Decomposition Method (DDM) flow',
                 fontsize=14, weight='bold')
    save_figure(fig, 'figure5_ddm_flow.png', save_dir)

def generate_all_figures():
    """Generate all paper figures."""
    print("Generating Figure 1...")
    figure1_lockin_pathway()
    print("Generating Figure 2...")
    figure2_dcl_flow()
    print("Generating Figure 3...")
    figure3_ddi_evolution()
    print("Generating Figure 4...")
    figure4_cupf_model()
    print("Generating Figure 5...")
    figure5_ddm_flow()
    print("\nAll figures generated.")

if __name__ == '__main__':
    generate_all_figures()
