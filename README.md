# SGEMAS: Self-Growing Ephemeral Multi-Agent System

**Official Implementation for the paper:**  
*"SGEMAS: A Self-Growing Ephemeral Multi-Agent System for Unsupervised Online Anomaly Detection via Entropic Homeostasis"*

## Overview
SGEMAS is a bio-inspired anomaly detection framework that treats intelligence as a thermodynamic process. Instead of a static neural network, it uses a dynamic population of agents that grow (mitosis) and die (apoptosis) based on the metabolic cost of tracking the signal.

This repository contains the canonical implementation of **SGEMAS v3.3**, which achieves an AUC of **0.570** on the MIT-BIH Arrhythmia Database (Inter-patient split DS2) in a fully unsupervised, zero-shot regime.

## Key Features
*   **Unsupervised:** No labels required.
*   **Online:** Processes data stream-wise (sample by sample).
*   **Energy-Efficient:** "Wake-on-crisis" architecture; agents only exist when the signal is anomalous.
*   **Interpretable:** The metabolic energy $E(t)$ serves as a direct biomarker for pathology.

## Usage

```python
from sgemas import SGEMAS_v33

# Initialize model
model = SGEMAS_v33()

# Process a signal stream
scores = []
for x in signal:
    out = model.process(x)
    scores.append(out['anom_score'])
```

## Citation
If you use this code, please cite our paper:
```bibtex
@article{hamdi2025sgemas,
  title={SGEMAS: A Self-Growing Ephemeral Multi-Agent System...},
  author={Hamdi, Mustapha},
  journal={Proceedings of...},
  year={2025}
}
```
