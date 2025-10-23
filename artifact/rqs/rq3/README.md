# RQ3: Tool Effectiveness for Detection and Repair

This folder contains data for evaluating static analysis tools and Large Language Models (LLMs) on portability issue detection and repair.

## Contents

### Code Snippets
- `code/nonportable/` - 30 non-portable Python files with OS-specific issues
- `code/portable/fixed/` - 30 fixed versions from actual GitHub issues
- `code/portable/unrelated/` - 30 unrelated portable code samples
- **Total: 90 code snippets** for evaluation

### Detection Results
- `detection_results/results_full.csv` - Classification results for 90 samples across 3 LLMs (llama-3.3, grok-4-fast, gpt-4o-mini)
- `detection_results/results_summary.csv` - Confusion matrices and performance metrics
- `detection_results/analysis.py` - Script for analyzing results

### Repair Results
- `fix_results/fix_generic_summary.csv` - Repair results with generic prompts
- `fix_results/fix_specific_summary.csv` - Repair results with pattern-guided prompts
- `fix_results/fix_generic_analysis.py` - Script for correctness verification

### Scripts
- `run_detection.py` - Script to run detection evaluation
- `run_fix_generic.py` - Script to run repair evaluation
