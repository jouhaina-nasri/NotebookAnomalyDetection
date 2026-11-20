"""Unit tests for the rule-based detector (technique 1)."""
import csv

import pytest

import detector
from detector import SMELLS, detect_smells, read_thresholds
from python_parser import FEATURES

THRESHOLDS = read_thresholds()


def clean(**overrides):
    f = dict.fromkeys(FEATURES, 0)
    f.update(overrides)
    return f


def flagged(**overrides):
    return {s for s, v in detect_smells(clean(**overrides), THRESHOLDS).items() if v}


def test_clean_cell_has_no_smell():
    assert flagged() == set()


def test_long_cell_needs_size_and_complexity():
    t = THRESHOLDS
    assert flagged(SLOC=t["SLOC"], VOL=t["VOL"]) == {"LC"}
    assert flagged(SLOC=t["SLOC"], CC=t["CC_FC"], FC=0) == {"LC"}
    assert flagged(SLOC=t["SLOC"] - 1, VOL=10 * t["VOL"]) == set()
    assert flagged(SLOC=10 * t["SLOC"]) == set()


@pytest.mark.parametrize(
    "overrides, smell",
    [
        ({"DNA": THRESHOLDS["DNA"]}, "LEC"),
        ({"LOEC": THRESHOLDS["LOEC"]}, "LEC"),
        ({"NOL_NOCC": THRESHOLDS["NOL_NOCC"], "LOC": THRESHOLDS["LOC"]}, "CCC"),
        ({"NOCE": THRESHOLDS["NOCE"]}, "LE"),
        ({"DNIC": THRESHOLDS["DNIC"]}, "CIC"),
        ({"NOIC": THRESHOLDS["NOIC"]}, "CIC"),
    ],
)
def test_each_rule_triggers_at_its_threshold(overrides, smell):
    assert flagged(**overrides) == {smell}
    below = {k: v - 1 for k, v in overrides.items()}
    assert smell not in flagged(**below)


def test_comprehension_rule_needs_both_conditions():
    assert flagged(LOC=10 * THRESHOLDS["LOC"]) == set()
    assert flagged(NOL_NOCC=5) == set()


def test_cli_writes_one_row_per_code_cell(make_notebook, tmp_path, monkeypatch):
    notebook = make_notebook(
        "x = 1",
        "if a:\n    if b:\n        pass",
        "%time x = 2",
    )
    output = tmp_path / "results.csv"
    monkeypatch.setattr("sys.argv", ["detector.py", str(tmp_path), "-o", str(output)])
    detector.main()

    rows = list(csv.reader(output.open()))
    assert rows[0] == ["File", "Cell"] + SMELLS
    assert rows[1:] == [
        ["sample.ipynb", "1", "0", "0", "0", "0", "0"],
        ["sample.ipynb", "2", "0", "0", "0", "0", "1"],
    ]
