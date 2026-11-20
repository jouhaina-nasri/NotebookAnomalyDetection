import argparse
import os
import json
import csv
import nbformat
from python_parser import parse_jupyter_notebook

def read_thresholds():
    thresholds_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'thresholds.json')
    with open(thresholds_path, 'r') as f:
        return json.load(f)

def write_to_csv(csv_writer, metrics, thresholds, file, cell_number):
    # Initializes the results list with the file name and cell number
    file_name = os.path.basename(file)

    results = [file_name, str(cell_number)]
    
    # Rule for "Long Cell"
    long_cell_condition = (
        metrics['source_lines_of_code'] >= thresholds['SLOC'] and
        (metrics['cyclomatic_complexity'] + metrics['functional_complexity']) >= thresholds['CC_FC']
    ) or (
        metrics['source_lines_of_code'] >= thresholds['SLOC'] and
        metrics['volume'] >= thresholds['VOL']
    )
    results.append(1 if long_cell_condition else 0)
    
    # Rule for "Long Element Chain"
    max_nested_arrays = max(metrics.get('nested_array_depth', []) or [0])
    max_length_element_chain = max(metrics.get('element_chain_length', []) or [0])
    long_element_chain_condition = max_nested_arrays >= thresholds['DNA'] or max_length_element_chain >= thresholds['LOEC']
    results.append(1 if long_element_chain_condition else 0)

    # Rule for "Complex Container Comprehension"
    max_loop_condition = max(metrics.get('loop_and_condition', []) or [0])
    max_length_comprehension = max(metrics.get('comprehension_length', []) or [0])
    complex_list_comprehension_condition = max_loop_condition >= thresholds['NOL_NOCC'] and max_length_comprehension >= thresholds['LOC']
    results.append(1 if complex_list_comprehension_condition else 0)
    
    # Rule for "Long Expression"
    max_length_expression = max(metrics.get('expression_length', []) or [0])
    long_ternary_condition = max_length_expression >= thresholds['NOCE']
    results.append(1 if long_ternary_condition else 0)
    
    # Rule for "Complex IF-Conditional"
    max_nested_conditions = max(metrics.get('nested_condition_depth', []) or [0])
    number_conditions_if = metrics.get('num_conditions', 0)
    complex_ternary_condition = max_nested_conditions >= thresholds['DNIC'] or number_conditions_if >= thresholds['NOIC']
    results.append(1 if complex_ternary_condition else 0)
    
    # Writing results to CSV file
    csv_writer.writerow(results)

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

HEADER = ["File", "Cell", "LC", "LEC", "CCC", "LE", "CIC"]

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
