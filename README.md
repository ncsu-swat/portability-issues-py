# An Empirical Analysis of Portability Issues in Python Projects

This repository contains the replication package for our paper **"An Empirical Analysis of Cross-OS Portability Issues in Python Projects"**, accepted at **Mining Software Repositories (MSR) 2026**.

## Paper Information

- **Authors:** Denini Silva, MohamadAli Farahat, and Marcelo d'Amorim
- **Conference:** Mining Software Repositories 2026
- **Location:** Rio de Janeiro, Brazil
- **Date:** April 2026

## About This Research

Cross-OS portability is essential for modern software development, yet Python projects often face challenges when running across different operating systems. This paper presents an empirical analysis of portability issues in Python projects, examining their prevalence, characteristics, and potential solutions.

## Repository Structure

- **`artifact/`** - Complete artifact for paper replication
  - `data/` - Dataset of 2,042 analyzed Python projects
  - `rqs/rq1/` - Test re-execution and issue mining results
  - `rqs/rq2/` - Code examples with categorization
  - `rqs/rq3/` - LLM evaluation (code snippets and results)
  - `rqs/rq4/` - Pull requests submitted to open-source projects
- **`experiments/`** - Experimental scripts and intermediate data

## Setup

To replicate our experiments, you need to install the required dependencies. We recommend using a virtual environment.

### Installation Instructions

#### Unix/Linux/macOS

```bash
# Clone the repository
git clone <repository-url>
cd portability-issues-project

# Navigate to artifact directory
cd artifact

# Create virtual environment
python -m venv env

# Activate virtual environment
source env/bin/activate

# Install requirements
pip install -r requirements.txt
```

#### Windows

```cmd
# Clone the repository
git clone <repository-url>
cd portability-issues-project

# Navigate to artifact directory
cd artifact

# Create virtual environment
python -m venv env

# Activate virtual environment
env\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

## Artifact

The complete artifact with detailed documentation is available in the [`artifact/`](artifact/) directory. Please refer to the [artifact README](artifact/README.md) for:

- Detailed description of each research question
- Instructions to reproduce our results
- Dataset documentation and structure

## Citation

If you use this work in your research, please cite:

```bibtex
@inproceedings{silva2026portability,
  author    = {Denini Silva and MohamadAli Farahat and Marcelo d'Amorim},
  title     = {An Empirical Analysis of Cross-OS Portability Issues in Python Projects},
  booktitle = {Proceedings of the 23rd International Conference on Mining Software Repositories},
  year      = {2026},
  month     = {April},
  location  = {Rio de Janeiro, Brazil},
  series    = {MSR '26}
}
```

## Contact

For questions or issues regarding this replication package, please open an issue in this repository.
