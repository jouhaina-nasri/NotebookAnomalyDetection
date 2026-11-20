"""Technique 2: detect code smells in Jupyter notebooks with the trained XGBoost model.

The features are computed by the same parser as technique 1
(technique1.python_parser), so both techniques always see identical metrics.
"""
import argparse
import os
import sys

import joblib
import xgboost
import nbformat
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(BASE_DIR))  # repository root, so that technique1 is importable

from technique1.python_parser import FEATURES, parse_jupyter_notebook, to_features  # noqa: E402

SMELLS = ['LC', 'LEC', 'CCC', 'LE', 'CIC']
# Native XGBoost format, portable across XGBoost versions. It was exported from
# trained_xgboost_model.pkl (kept for the training notebooks) with identical predictions.
MODEL_PATH = os.path.join(BASE_DIR, 'trained_xgboost_model.json')


def extract_metrics_from_notebook(file_path):
    """Return one row (File, Cell, *FEATURES) per analyzable code cell."""
    notebook = nbformat.read(file_path, as_version=4)
    file_name = os.path.basename(file_path)

    rows = []
    for cell_number, cell in enumerate(notebook.cells):
        if cell.cell_type != 'code':
            continue
        for metrics in parse_jupyter_notebook(cell):
            features = to_features(metrics)
            rows.append([file_name, cell_number] + [features[name] for name in FEATURES])
    return rows


def load_model(path=MODEL_PATH):
    if path.endswith('.pkl'):
        return joblib.load(path)
    model = xgboost.XGBClassifier()
    model.load_model(path)
    return model


def predict(notebook_files, model=None):
    """Predict the 5 code smells for every code cell of the given notebooks."""
    model = model or load_model()

    rows = []
    for notebook_file in notebook_files:
        rows.extend(extract_metrics_from_notebook(notebook_file))

    df = pd.DataFrame(rows, columns=['File', 'Cell'] + FEATURES)
    if df.empty:
        return pd.DataFrame(columns=['File', 'Cell'] + SMELLS)

    predictions_df = pd.DataFrame(model.predict(df[FEATURES]), columns=SMELLS)
    predictions_df['File'] = df['File']
    predictions_df['Cell'] = df['Cell']
    return predictions_df[['File', 'Cell'] + SMELLS]


def main(notebook_files, output='predictions.csv'):
    predict(notebook_files).to_csv(output, index=False)
    print(f"Predictions saved to {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect code smells in Jupyter notebooks (XGBoost model).")
    parser.add_argument("notebooks", nargs="*", help="paths of .ipynb files")
    parser.add_argument("-o", "--output", default="predictions.csv", help="output CSV file (default: predictions.csv)")
    args = parser.parse_args()
    notebook_files = args.notebooks or [
        p.strip() for p in input("Enter the paths of the Jupyter notebooks separated by commas: ").split(",")
    ]
    main(notebook_files, args.output)
