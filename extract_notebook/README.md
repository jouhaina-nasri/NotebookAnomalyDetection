## Overview

This directory contains the Python script `notebook_cell_reader.py`, which is designed to extract the source content of specified code cells from Jupyter notebooks. The script reads input from a CSV file, where each row specifies the path to a Jupyter notebook and the index of the cell whose content should be extracted. The extracted content is then written to an output CSV file.

## `notebook_cell_reader.py`

**Functionality**:
- Extract the source content of a specified code cell from a Jupyter notebook.
- Read the paths to Jupyter notebooks and cell indices from an input CSV file.
- Write the extracted cell content to an output CSV file.

**Key Functions**:

- `get_code_cell_content(notebook_path, cell_index)`: Extracts the source content of a code cell given a notebook's path and a cell's index.

**Usage**:

To use the script:

1. Prepare an input CSV file with at least the following columns:
   - `File`: Specifies the path to the Jupyter notebook.
   - `Cell`: Indicates the index of the cell to extract.

2. Run the script and provide the paths to the input and output CSV files when prompted.

3. The script will read the input CSV file, extract the specified cells' content, and write the results to the output CSV file.

## Dependencies

To use `notebook_cell_reader.py`, ensure you have the following Python libraries installed:
- `nbformat`
- `pandas`

You can install these libraries using `pip`:
`pip install nbformat pandas`
