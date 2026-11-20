import pandas as pd

def load_and_merge_data(tool_csv_path, manual_csv_path):
    """
    Load data from CSV files and merge them based on 'File' and 'Cell' columns.
    """
    tool_results = pd.read_csv(tool_csv_path)
    manual_labels = pd.read_csv(manual_csv_path)
    return pd.merge(tool_results, manual_labels, on=['File', 'Cell'], suffixes=('_tool', '_manual'))

def calculate_metrics(merged_data, columns):
    """
    Calculate precision and recall for a list of code smells and store them in a dictionary.
    """
    results = {}
    
    for column in columns:
        tp = ((merged_data[column + '_tool'] == 1) & (merged_data[column + '_manual'] == 1)).sum()
        fp = ((merged_data[column + '_tool'] == 1) & (merged_data[column + '_manual'] == 0)).sum()
        fn = ((merged_data[column + '_tool'] == 0) & (merged_data[column + '_manual'] == 1)).sum()

        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0

        results[column] = {"Precision": precision, "Recall": recall}
    
    return results

def main():
    tool_csv_path = input("Enter the path to the tool's CSV file: ").strip()
    manual_csv_path = input("Enter the path to the manual labels CSV file: ").strip()

    try:
        merged_data = load_and_merge_data(tool_csv_path, manual_csv_path)
    except FileNotFoundError:
        print("One or more specified CSV files could not be found.")
        return
    
    code_smell_columns = [
        "LC",
        "LEC",
        "CCC",
        "LE",
        "CIC"
    ]
    
    results = calculate_metrics(merged_data, code_smell_columns)
    print(results)

if __name__ == "__main__":
    main()
