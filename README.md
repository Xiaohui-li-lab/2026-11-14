# Decomposition-Composition Law (DCL) Research Repository

**Project:** The Holistic Overview of the Decomposition-Composition Law  
**Author:** Xiaohui Li  
**Affiliation:** Independent Researcher, Baoji, China  
**ORCID:** 0009-0003-8233-7191  
**Email:** danceluck@163.com  
**Data & Code Homepage:** https://github.com/xiaohui-li-lab/

## Overview

This repository provides open-source code, datasets, and reproducible workflows for the paper:

> **"The Holistic Overview of the Decomposition-Composition Law"**  
> Xiaohui Li

The repository implements:
- **DCL formal model**: decomposition and recombination operators.
- **DDI calculator**: Degree of Decomposability Index.
- **CLDS simulation**: Conceptual Lock-in and Decomposition Simulation (agent-based model).
- **DDM benchmark**: Divination-based Decomposition Method benchmark testing.
- **Visualization**: all figures in the paper.
- **Datasets**: CDLD, CLDS outputs, DDM case library.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/xiaohui-li-lab/decomposition-composition-law.git
cd decomposition-composition-law

# Install dependencies
pip install -r requirements.txt

# Generate all datasets
python src/generate_datasets.py

# Run CLDS simulation
python -c "from src.clds_simulation import run_clds_demo; run_clds_demo()"

# Run DDM benchmark
python -c "from src.ddm_benchmark import run_ddm_demo; run_ddm_demo()"

# Generate all figures
python src/visualization.py

# Run unit tests
pytest tests/





2026-11-14/
├── README.md
├── CITATION.cff
├── requirements.txt
├── .gitignore
├── data/
│   ├── cdld_concepts.csv
│   ├── clds_results.csv
│   ├── clds_summary.csv
│   ├── ddm_benchmark_results.csv
│   └── ddm_cases.csv
├── figures/
│   ├── figure1_lockin_pathway.png
│   ├── figure2_dcl_flow.png
│   ├── figure3_ddi_evolution.png
│   ├── figure4_cupf_model.png
│   └── figure5_ddm_flow.png
├── src/
│   ├── __init__.py
│   ├── ddi_calculator.py
│   ├── clds_simulation.py
│   ├── ddm_benchmark.py
│   ├── generate_datasets.py
│   └── visualization.py
├── notebooks/
│   └── reproduce_paper_results.ipynb
└── tests/
    ├── test_ddi.py
    └── test_clds.py



Repository Contents
File/Directory	Description
data/	Generated datasets (CSV format)
figures/	Paper figures (PNG format)
src/ddi_calculator.py	DDI computation utilities
src/clds_simulation.py	Agent-based conceptual lock-in simulation
src/ddm_benchmark.py	Double-blind DDM benchmark simulator
src/generate_datasets.py	Dataset generation scripts
src/visualization.py	Figure generation
notebooks/reproduce_paper_results.ipynb	Complete reproduction notebook
Key Results
The CLDS simulation confirms the paper's main hypotheses:

Positive value concepts have high initial DDI but decline fastest without intervention.
DDM intervention significantly restores DDI across all concept types.
Physical basic units (photons, electrons, etc.) remain near-irreducible.
The DDM benchmark supports H1 (DDM accuracy ≥ 70%) against H0 (chance level ≈ 50%).

Citation
Bibtex
@article{li2025dcl,
  title={The Holistic Overview of the Decomposition-Composition Law},
  author={Li, Xiaohui},
  year={2025},
  publisher={GitHub},
  url={https://github.com/xiaohui-li-lab/}
}
License
This project is released under the MIT License for academic use and reproducibility.

Code

---

## 文件二：`requirements.txt`

```text
numpy>=1.21.0
pandas>=1.3.0
matplotlib>=3.4.0
seaborn>=0.11.0
scipy>=1.7.0
networkx>=2.6.0
jupyter>=1.0.0
pytest>=6.2.0





