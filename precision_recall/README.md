# Code Metrics Evaluation

This repository contains two main Python scripts that help in evaluating code metrics from CSV data:

## Scripts

1. **calculate.py**
    - Description: Loads data from CSV files, merges them based on 'File' and 'Cell' columns, and then calculates precision and recall for a list of code smells.
    - [Demonstration Video](calculate.mkv)

2. **code_smell_evaluation_metrics.py**
    - Description: Loads and merges CSV data similarly but calculates various metrics including global accuracy, precision, recall, MCC (Matthews correlation coefficient), and F1-score for the list of code smells.
    - [Demonstration Video](evaluation.mkv)

## Requirements

- Python 3.x
- pandas

## Installation

To install the required libraries, run:

```bash
pip install pandas
```
## Usage

1. **For `calculate.py`:**
`python calculate.py`

1. **For `code_smell_evaluation_metrics.py`:**
`python code_smell_evaluation_metrics.py`

Both scripts will prompt the user for the path to the tool's CSV file and the path to the manual labels CSV file.
