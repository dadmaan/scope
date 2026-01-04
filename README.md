
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# SCOPE

> Situated Creative Operation and Process Evaluation

This repository provides the open-source implementation of SCOPE (Situated Creative Operation and Process Evaluation), a framework for evaluating AI music generation systems within authentic creative workflows. Current evaluation approaches—objective metrics like FAD and subjective listening studies—assess generated outputs in isolation, overlooking how systems integrate into compositional practice. SCOPE addresses this gap through a three-phase methodology (System Overview, Situated Observation, Formal Assessment) that asks not "how good is the audio?" but "how effectively does this system support creative practice?" The framework was validated through a year-long first-person expert evaluation of four open-source systems (MusicGen, Riffusion, Magenta Studio, and DDSP-VST), revealing that workflow integration shapes creative viability as consequentially as generation quality itself. This repository contains Jupyter notebooks, a Python scoring library, documentation templates, and logging protocols—artifacts refined across 32 evaluation sessions—enabling researchers, practitioners, and developers to conduct systematic, transparent, and reproducible assessments of creative AI tools.

## Requirements

- Python 3.9+
- Jupyter Notebook/Lab

## Installation

### pip (Recommended)

```bash
git clone https://github.com/dadmaan/scope.git
cd scope
pip install -e .
```

With development dependencies:

```bash
pip install -e .[dev]
```

### Docker

```bash
cd docker
docker-compose up
```

Access Jupyter at `http://localhost:8889`

## Usage

The framework provides three Jupyter notebooks implementing the evaluation phases:

| Notebook | Phase | Purpose |
|----------|-------|---------|
| `P1_the_system_overview.ipynb` | System Overview | Assess system architecture, interface, and hardware requirements |
| `P2_the_session_notebook.ipynb` | Situated Observation | Log sessions, incidents, and workflow phases |
| `P3_the_synthesis_journal.ipynb` | Formal Assessment | Quantitative scoring across 8 criteria with reflective journaling |

Run notebooks via Jupyter:

```bash
jupyter lab notebooks/
```

Or via Voila for a dashboard interface:

```bash
voila notebooks/P2_the_session_notebook.ipynb
```

## Project Structure

```text
scope/
├── src/aimusic_eval/     # Python package
│   ├── core/             # Helpers, validators, exporters
│   ├── widgets/          # Jupyter widget components
│   └── schemas/          # JSON validation schemas
├── notebooks/            # Evaluation notebooks
├── examples/             # Sample session and synthesis data
└── docker/               # Docker configuration
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.