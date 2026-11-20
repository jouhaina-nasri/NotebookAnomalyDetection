import argparse
import os
import json
import csv
import nbformat
try:  # imported as part of the technique1 package
    from .python_parser import parse_jupyter_notebook, to_features
except ImportError:  # run as a script or imported as a top-level module
    from python_parser import parse_jupyter_notebook, to_features

def read_thresholds():
    thresholds_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'thresholds.json')
    with open(thresholds_path, 'r') as f:
        return json.load(f)

SMELLS = ["LC", "LEC", "CCC", "LE", "CIC"]


def detect_smells(f, thresholds):
    """Apply the detection rules to the features of one cell.

    Returns a dict {smell: 0 or 1} for LC, LEC, CCC, LE and CIC.
    """
    long_cell = f['SLOC'] >= thresholds['SLOC'] and (
        f['CC'] + f['FC'] >= thresholds['CC_FC'] or f['VOL'] >= thresholds['VOL']
    )
    long_element_chain = f['DNA'] >= thresholds['DNA'] or f['LOEC'] >= thresholds['LOEC']
    complex_comprehension = f['NOL_NOCC'] >= thresholds['NOL_NOCC'] and f['LOC'] >= thresholds['LOC']
    long_expression = f['NOCE'] >= thresholds['NOCE']
    complex_if = f['DNIC'] >= thresholds['DNIC'] or f['NOIC'] >= thresholds['NOIC']

    flags = [long_cell, long_element_chain, complex_comprehension, long_expression, complex_if]
    return {smell: int(flag) for smell, flag in zip(SMELLS, flags)}


def write_to_csv(csv_writer, metrics, thresholds, file, cell_number):
    smells = detect_smells(to_features(metrics), thresholds)
    csv_writer.writerow([os.path.basename(file), str(cell_number)] + [smells[s] for s in SMELLS])


def analyze_notebook(file_path, csv_writer, thresholds):
    try:
        notebook = nbformat.read(file_path, as_version=4)
        for cell_number, cell in enumerate(notebook.cells):
            if cell.cell_type == 'code':
                cell_metrics_list = parse_jupyter_notebook(cell)
                for metrics in cell_metrics_list:
                    write_to_csv(csv_writer, metrics, thresholds, file_path, cell_number)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

HEADER = ["File", "Cell"] + SMELLS

def main():
    parser = argparse.ArgumentParser(description="Detect code smells in Jupyter notebooks (rule-based).")
    parser.add_argument("path", nargs="?", help="folder containing .ipynb files")
    parser.add_argument("-o", "--output", default="results.csv", help="output CSV file (default: results.csv)")
    args = parser.parse_args()

    path = args.path or input('Path of folder: ').strip()
    thresholds = read_thresholds()

    header = HEADER

    with open(args.output, mode='w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        # Write the header
        csv_writer.writerow(header)
        
        for file in os.listdir(path):
            if file.endswith(".ipynb"):
                file_path = os.path.join(path, file)
                analyze_notebook(file_path, csv_writer, thresholds)

    print(f"Results saved to {args.output}")

if __name__ == "__main__":
    main()
