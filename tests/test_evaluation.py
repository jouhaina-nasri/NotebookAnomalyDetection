"""Full evaluation against the 383 manually labeled cells.

Needs the 325 labeled notebooks from data/ (listed in tests/eval_notebooks.txt).
It is skipped when they are missing; the CI `evaluation` job fetches them.
"""
import csv
import os

import pandas as pd
import pytest

import detector
from conftest import ROOT

DATA = os.path.join(ROOT, "data")
NOTEBOOKS = open(os.path.join(ROOT, "tests", "eval_notebooks.txt")).read().split("\n")
NOTEBOOKS = [n for n in NOTEBOOKS if n]

pytestmark = [
    pytest.mark.evaluation,
    pytest.mark.skipif(
        not all(os.path.exists(os.path.join(DATA, n)) for n in NOTEBOOKS),
        reason="labeled notebooks from data/ are not checked out",
    ),
]


@pytest.fixture(scope="module")
def merged(tmp_path_factory):
    output = tmp_path_factory.mktemp("eval") / "results.csv"
    thresholds = detector.read_thresholds()
    with open(output, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(detector.HEADER)
        for name in NOTEBOOKS:
            detector.analyze_notebook(os.path.join(DATA, name), writer, thresholds)

    labels = pd.read_csv(os.path.join(ROOT, "precision_recall", "manual_labeling.csv"))
    tool = pd.read_csv(output).drop_duplicates(["File", "Cell"])
    return labels.merge(tool, on=["File", "Cell"], suffixes=("_manual", "_tool"))


def confusion(merged, smells):
    tp = fp = fn = tn = 0
    for s in smells:
        tool, manual = merged[f"{s}_tool"] == 1, merged[f"{s}_manual"] == 1
        tp += (tool & manual).sum()
        fp += (tool & ~manual).sum()
        fn += (~tool & manual).sum()
        tn += (~tool & ~manual).sum()
    return tp, fp, fn, tn


def test_every_labeled_cell_is_analyzed(merged):
    assert len(merged) == 383


def test_global_scores_match_the_readme(merged):
    tp, fp, fn, tn = confusion(merged, detector.SMELLS)
    precision, recall = tp / (tp + fp), tp / (tp + fn)
    mcc = (tp * tn - fp * fn) / ((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn)) ** 0.5

    assert round(precision, 3) == 0.980
    assert round(recall, 3) == 0.947
    assert round(mcc, 3) == 0.959


@pytest.mark.parametrize("smell", ["LC", "LEC", "CCC", "LE", "CIC"])
def test_per_smell_f1_is_above_0_9(merged, smell):
    tp, fp, fn, _ = confusion(merged, [smell])
    assert 2 * tp / (2 * tp + fp + fn) > 0.9
