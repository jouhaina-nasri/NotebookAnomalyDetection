import ast
import sys
sys.path.append("/home/jouhaina/Documents/PFE/detector_tool")

from technique1.ComprehensionMetricCalculator import  count_loops_and_conditions_in_comprehensions,calculate_comprehension_length
from technique1.ConditionMetricCalculator import count_if_statements, find_max_if_depths
from technique1.CyclomaticComplexityCalculator import calculate_cyclomatic_complexity
from technique1.ElementChainMetricCalculator import extract_nesting_value, extract_element_counts
from technique1.ExpressionMetricCalculator import extract_assignment_lengths 
from technique1.HalsteadMetricCalculator import MetricsCalculator
from technique1.SlocMetricCalculator import count_source_lines_of_code
from technique1.FunctionnalComplexityCalculator import calculate_complexity

from collections import namedtuple

import nbformat
import joblib
import pandas as pd

import os

def max_or_zero(lst):
    return max(lst) if lst and isinstance(lst, list) else 0

def parse_jupyter_notebook(cell, file_name, cell_number):
    if cell.source.startswith('%') or cell.cell_type != 'code':
        return []

    try:
        cell_ast = ast.parse(cell.source)
    except SyntaxError:
        return []

    # Metrics
    sloc = count_source_lines_of_code(cell.source)
    cyclomatic_complexity = calculate_cyclomatic_complexity(cell_ast)

    metrics_calculator = MetricsCalculator(cell.source)
    volume = metrics_calculator.calculate_volume()

    functional_complexity = calculate_complexity(cell_ast)
    
    nested_array_depth = max_or_zero(extract_nesting_value(cell_ast))
    element_chain_length = max_or_zero(extract_element_counts(cell_ast))
    loop_and_condition = max_or_zero(count_loops_and_conditions_in_comprehensions(cell_ast))
    comprehension_length = max_or_zero(calculate_comprehension_length(cell.source, cell_ast))
    expression_length = max_or_zero(extract_assignment_lengths(cell_ast))
    nested_condition_depth = max_or_zero(find_max_if_depths(cell_ast))
    num_conditions = count_if_statements(cell_ast)


    Metrics = namedtuple('Metrics', [
        'SLOC',
        'CC',
        'FC',
        'VOL',
        'NOL_NOCC',
        'LOC',
        'DNA',
        'LOEC',
        'NOCE',
        'DNIC',
        'NOIC'
    ])

    cell_metrics = Metrics(
        sloc, cyclomatic_complexity, functional_complexity, volume, loop_and_condition, 
        comprehension_length, nested_array_depth, element_chain_length,
        expression_length, nested_condition_depth, num_conditions
    )

    # Extract execution count or set it to 'N/A' if not available
    execution_count = cell.get('execution_count', 'N/A')

    return [(file_name, cell_number) + cell_metrics]

def extract_metrics_from_notebook(file_path):
    with open(file_path, "r") as f:
        notebook = nbformat.read(f, as_version=4)

    all_metrics = []
    file_name = os.path.basename(file_path)  # Just the filename without the path
    for cell_number, cell in enumerate(notebook.cells):
        if cell.cell_type == 'code':
            metrics = parse_jupyter_notebook(cell, file_name, cell_number)
            all_metrics.extend(metrics)

    return all_metrics

def main(notebook_files):
    # Load the trained XGBoost model
    xgboost_model = joblib.load('trained_xgboost_model.pkl')
    
    all_notebook_metrics = []
    all_files = []  # To store filenames
    all_cells = []  # To store cell numbers
    
    for notebook_file in notebook_files:
        metrics = extract_metrics_from_notebook(notebook_file)
        all_notebook_metrics.extend(metrics)
        
        # Store filename and cell number for each metric
        for i in range(len(metrics)):
            all_files.append(notebook_file)
            all_cells.append(i+1)
     # Convert metrics to DataFrame
    results = []
    for metrics in all_notebook_metrics:
        file_name, cell_num, metrics_tuple = metrics[0], metrics[1], metrics[2:]
        results.append((file_name, cell_num) + metrics_tuple)

    # Convert list of tuples to DataFrame
    df = pd.DataFrame(results, columns=['File', 'Cell', 'SLOC', 'CC', 'FC', 'VOL', 'NOL_NOCC', 'LOC', 'DNA', 'LOEC', 'NOCE', 'DNIC', 'NOIC'])
    
    # Make predictions
    predictions = xgboost_model.predict(df[['SLOC', 'CC', 'FC', 'VOL', 'NOL_NOCC', 'LOC', 'DNA', 'LOEC', 'NOCE', 'DNIC', 'NOIC']])
    
    # Convert predictions to DataFrame and add File and Cell columns
    predictions_df = pd.DataFrame(predictions, columns=['LC', 'LEC', 'CCC', 'LE', 'CIC'])
    predictions_df['File'] = df['File']
    predictions_df['Cell'] = df['Cell']

    # Reorder columns
    predictions_df = predictions_df[['File', 'Cell', 'LC', 'LEC', 'CCC', 'LE', 'CIC']]
    
    # Save predictions to CSV
    predictions_df.to_csv('predictions.csv', index=False)

    print("Predictions saved to predictions.csv")



if __name__ == "__main__":
    # Replace with your actual notebook paths, or pass them as command line arguments
    notebook_files = input("Enter the paths of the Jupyter notebooks separated by commas: ").split(",")
    main(notebook_files)
