"""Regression test: the detector must reproduce the published tool results.

tests/fixtures/notebooks holds 14 small notebooks from the labeled sample
(covering every smell); expected_tool_results.csv holds the matching rows of
precision_recall/result_tool.csv.
"""
import csv
import glob
import os

import pandas as pd

import detector
from conftest import FIXTURES


def test_detector_reproduces_published_results(tmp_path):
    thresholds = detector.read_thresholds()
    output = tmp_path / "results.csv"
    with open(output, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(detector.HEADER)
        for notebook in sorted(glob.glob(os.path.join(FIXTURES, "notebooks", "*.ipynb"))):
            detector.analyze_notebook(notebook, writer, thresholds)

    expected = pd.read_csv(os.path.join(FIXTURES, "expected_tool_results.csv"))
    actual = pd.read_csv(output)
    merged = expected.merge(actual, on=["File", "Cell"], how="left", suffixes=("_expected", "_actual"))

    assert len(merged) == len(expected) == 14
    for smell in detector.SMELLS:
        mismatches = merged[merged[f"{smell}_expected"] != merged[f"{smell}_actual"]]
        assert mismatches.empty, f"{smell} differs on:\n{mismatches[['File', 'Cell']]}"
