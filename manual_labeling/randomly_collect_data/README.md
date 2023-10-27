## Overview

This directory contains two scripts, one in Python (`filename.py`) and another in R (`random_file_sampling.R`). 

1. `filename.py`: Extracts specific code cells from Jupyter notebooks and writes their details to a CSV file.
2. `random_file_sampling.R`: Samples rows from the generated CSV file.

## `filename.py`

**Functionality**:

- Parses Jupyter notebook files from the specified folder.
- Identifies code cells, excluding those that are empty, start with Jupyter magic commands, or contain syntax errors.
- Writes the filename and cell index of the identified cells to a CSV file.

**Usage**:

To use the script:

1. Run the script.
2. When prompted, provide the folder path containing Jupyter notebooks.
3. Next, provide the path where you'd like to save the resulting CSV file.

**Output**:

A CSV file with columns:
- `Notebook`: Name of the notebook file.
- `Cell`: Index of the identified code cell.

## `random_file_sampling.R`

**Functionality**:

- Reads a CSV file containing data from `filename.py`.
- Samples a specified number of rows.
- Writes the sampled data to an output CSV file.

**Usage**:

The script is set to work with specific input and output file paths and a sample size of 383.

**Note**:

The sample size of 383 was obtained using the Sample Size Calculator tool available at [Sample Size Calculator](https://www.calculator.net/sample-size-calculator.html?type=1&cl=95&ci=5&pp=50&ps=1000&x=53&y=25).

## Dependencies

For `filename.py`:
- Ensure you have the Python libraries `csv`, `ast`, `nbformat`, and `glob` installed.

For `random_file_sampling.R`:
- Ensure you have the R `base` package installed, which is typically available by default with an R installation.
