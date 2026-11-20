"""Tests for the learning-based detector (technique 2)."""
import pytest

xgboost = pytest.importorskip("xgboost")

from technique2 import python_parser as technique2  # noqa: E402

SMELLS = ["LC", "LEC", "CCC", "LE", "CIC"]


@pytest.fixture(scope="module")
def model():
    return technique2.load_model()


def test_predict_returns_binary_labels_per_code_cell(make_notebook, model):
    notebook = make_notebook(
        "x = 1",
        "colors = ['red', 'green', 'blue', 'cyan', 'magenta', 'yellow', 'black', 'white']",
        "%matplotlib inline",
    )
    predictions = technique2.predict([notebook], model=model)

    assert list(predictions.columns) == ["File", "Cell"] + SMELLS
    assert predictions["Cell"].tolist() == [1, 2]  # magic cell skipped
    assert set(predictions[SMELLS].to_numpy().ravel()) <= {0, 1}


def test_predict_on_notebook_without_code(make_notebook, model):
    predictions = technique2.predict([make_notebook()], model=model)
    assert predictions.empty
    assert list(predictions.columns) == ["File", "Cell"] + SMELLS
