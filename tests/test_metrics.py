"""Unit tests for the AST metric extraction (technique1/python_parser.py)."""
import nbformat
import pytest

from python_parser import FEATURES, parse_jupyter_notebook, to_features


def features(source):
    parsed = parse_jupyter_notebook(nbformat.v4.new_code_cell(source))
    assert len(parsed) == 1
    return to_features(parsed[0])


@pytest.mark.parametrize("source", ["%matplotlib inline", "def f(:\n    pass"])
def test_magic_and_invalid_cells_are_skipped(source):
    assert parse_jupyter_notebook(nbformat.v4.new_code_cell(source)) == []


def test_feature_vector_has_the_model_columns():
    assert list(features("x = 1")) == FEATURES


def test_simple_cell_has_no_structural_complexity():
    f = features("x = 1\ny = x + 2\nprint(y)")
    assert f["SLOC"] == 3
    assert f["DNA"] == f["DNIC"] == f["NOIC"] == f["NOL_NOCC"] == 0


def test_nested_if_depth_and_count():
    f = features("if a:\n    if b:\n        x = 1\nif c:\n    pass\nif d:\n    pass")
    assert f["DNIC"] == 2
    assert f["NOIC"] == 4


def test_comprehension_loops_conditions_and_length():
    source = "result = [x * y for x in range(100) for y in range(100) if x % 2 == 0 if y % 3 == 0]"
    f = features(source)
    assert f["NOL_NOCC"] == 3  # one comprehension + two `if` filters
    assert f["LOC"] == len(source) - len("result = ")


def test_nested_containers_depth():
    assert features("m = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]")["DNA"] == 2


def test_element_chain_length():
    assert features("c = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']")["LOEC"] == 8


def test_expression_length_ignores_docstrings():
    assert features('"""A long module docstring that must not count as an expression."""')["NOCE"] == 0
    assert features("total = price * quantity")["NOCE"] == len("total = price * quantity")


def test_halstead_volume_grows_with_code():
    small = features("a = 1")["VOL"]
    large = features("a = 1\nb = a + 2\nc = b * a - 3\nd = (a + b) / c")["VOL"]
    assert 0 <= small < large
