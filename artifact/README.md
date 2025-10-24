# Artifact

This artifact contains data for our paper analyzing portability issues in Python projects.

## Setup

To run our scripts, you need to install the required dependencies. We recommend using a virtual environment.

### Installation Instructions

#### Unix/Linux/macOS

```bash
# create virtual environment
python -m venv env

# activate virtual environment
source env/bin/activate

# install requirements
pip install -r requirements.txt
```

#### Windows

```cmd
# create virtual environment
python -m venv env

# activate virtual environment
env\Scripts\activate

# install requirements
pip install -r requirements.txt
```

## Structure

- `data/` - 2,042 analyzed projects
- `rqs/rq1/` - Test re-execution and issue mining results
- `rqs/rq2/` - Code examples with categorization
- `rqs/rq3/` - LLM evaluation (code snippets + results)
- `rqs/rq4/` - Pull requests submitted

## Key Files

- `rqs/rq1/test_reexecution.csv` - Test failures across OSes
- `rqs/rq1/mined_issues.csv` - Portability issues from GitHub
- `rqs/rq2/code_examples.csv` - Categorization of example code
- `rqs/rq4/pull_requests.csv` - Our 33 PRs

See individual RQ folders for details.
