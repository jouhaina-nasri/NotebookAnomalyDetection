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
    Calculate global accuracy, precision, recall, MCC, and F1-score for a list of code smells.
    """
    total_tp, total_fp, total_fn, total_tn = 0, 0, 0, 0

    for column in columns:
        tp = ((merged_data[column + '_tool'] == 1) & (merged_data[column + '_manual'] == 1)).sum()
        fp = ((merged_data[column + '_tool'] == 1) & (merged_data[column + '_manual'] == 0)).sum()
        fn = ((merged_data[column + '_tool'] == 0) & (merged_data[column + '_manual'] == 1)).sum()
        tn = ((merged_data[column + '_tool'] == 0) & (merged_data[column + '_manual'] == 0)).sum()

        total_tp += tp
        total_fp += fp
        total_fn += fn
        total_tn += tn

    global_accuracy = (total_tp + total_tn) / (total_tp + total_fp + total_fn + total_tn)
    global_precision = total_tp / (total_tp + total_fp) if total_tp + total_fp != 0 else 0
    global_recall = total_tp / (total_tp + total_fn) if total_tp + total_fn != 0 else 0
    
    # Calcul du MCC
    mcc_numerator = (total_tp * total_tn) - (total_fp * total_fn)
    mcc_denominator = ((total_tp + total_fp) * (total_tp + total_fn) * (total_tn + total_fp) * (total_tn + total_fn)) ** 0.5
    mcc = mcc_numerator / mcc_denominator if mcc_denominator != 0 else 0

    return global_accuracy, global_precision, global_recall, mcc

def calculate_f1_score(precision, recall):
    """
   Calculate F1-score based on precision and recall.
    """
    if precision + recall == 0:
        return 0.0
    return 2 * (precision * recall) / (precision + recall)

def main():
    tool_csv_path = input("Enter the path to the tool's CSV file : ").strip()
    manual_csv_path = input("Enter the path to the manual labels CSV file : ").strip()

    try:
        merged_data = load_and_merge_data(tool_csv_path, manual_csv_path)
    except FileNotFoundError:
        print("One or more specified CSV files could not be found.")
        return

    code_smell_columns = [
        "LC",
        "CCC",
        "LEC",
        "LE",
        "CIC"
    ]

    global_accuracy, global_precision, global_recall, mcc = calculate_metrics(merged_data, code_smell_columns)

    print(f"Global Accuracy: {global_accuracy}")
    print(f"Global Precision: {global_precision}")
    print(f"Global Recall: {global_recall}")
    print(f"MCC: {mcc}")

    f1_score = calculate_f1_score(global_precision, global_recall)
    print(f"F1-score: {f1_score}")

if __name__ == "__main__":
    main()
