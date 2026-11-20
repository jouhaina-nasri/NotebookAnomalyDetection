import csv
from nbformat import read
import nbformat
from python_parser import parse_jupyter_notebook
import glob

def write_to_csv(rows, header, output_path, flatten=False):
    """Écrit des lignes dans un fichier CSV."""
    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for row in rows:
            if flatten and isinstance(row[-1], list):
                for item in row[-1]:
                    writer.writerow(row[:-1] + [item])
            else:
                writer.writerow(row)
    print(f"Résultats sauvegardés dans {output_path}")

def generic_list_metrics(metric_name):
    def extractor(parsed_data):
        metrics = []
        for cell in parsed_data:
            if metric_name in cell:
                metric_value = cell[metric_name]
                if metric_value:
                    metrics.append(metric_value)
        return metrics  # Retourne metrics au lieu de [metrics]
    return extractor

def generic_list_flattened(metric_name):
    def extractor(parsed_data):
        metrics_flattened = []
        for cell in parsed_data:
            if metric_name in cell:
                metric_value = cell[metric_name]
                if metric_value:
                    metrics_flattened.append(metric_value)
        return metrics_flattened  
    return extractor

def metric_extractor_func_for_other_metrics(parsed_data, metric):
    metrics = []
    for cell in parsed_data:
        if metric in cell:
            metrics.append(cell[metric])
    return metrics

def extract_metrics_from_cells(notebook_files, metric_extractor_func):
    """Extract metrics from notebook cells using the metric_extractor_func function."""  
    notebook_metrics = []
    for notebook_file in notebook_files:
        try:
            notebook = nbformat.read(notebook_file, as_version=4)
        except Exception as e:
            print(f"An error occurred: {e}")
            continue
        for cell_index, cell in enumerate(notebook.cells):
            if cell.cell_type == 'code':
                parsed_data = parse_jupyter_notebook(cell)
                file_name = notebook_file.split("/")[-1]
                metrics = metric_extractor_func(parsed_data)
                if metrics:
                    notebook_metrics.append([file_name, cell_index] + metrics)
    return notebook_metrics


def main():
    notebook_dir = input("Please enter the path to the directory containing the notebooks: ")
    output_dir = input("Please enter the path to the directory where you want to save the results: ")
    notebook_files = glob.glob(f"{notebook_dir}/*.ipynb")

    # Other metrics to extract
    metrics_to_extract = ['source_lines_of_code', 'cyclomatic_complexity', 'functional_complexity',
                           'volume', 'difficulty', 'effort', 'time_to_implement', 'scaled_volume', 'num_conditions']


    for metric in metrics_to_extract:
        metrics = extract_metrics_from_cells(notebook_files, lambda data: metric_extractor_func_for_other_metrics(data, metric))
        write_to_csv(metrics, ["Notebook", "Cell", "Value"], f"{output_dir}/{metric}.csv")

    # Generic list metrics
    generic_metrics_to_extract = ['num_loop_comprehension','element_chain_length','nested_array_depth',
                                  'expression_length','num_methods','num_args','comprehension_length',
                                  'args_and_methods','loop_and_condition','num_conditions_comprehension']
    for metric in generic_metrics_to_extract:
        metrics = extract_metrics_from_cells(notebook_files, generic_list_metrics(metric))
        write_to_csv(metrics, ["Notebook", "Cell", "Value"], f"{output_dir}/{metric}.csv")

        metrics_flattened = extract_metrics_from_cells(notebook_files, generic_list_flattened(metric))
        write_to_csv(metrics_flattened, ["Notebook", "Cell", "Value"], f"{output_dir}/{metric}_flattened.csv", flatten=True)


if __name__ == "__main__":
    main()

