"""Tests for the Flask API (technique1/app.py)."""
import csv
import io

import pytest


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("UPLOAD_FOLDER", str(tmp_path / "uploads"))
    import importlib

    import app

    importlib.reload(app)  # pick up UPLOAD_FOLDER
    app.app.config["TESTING"] = True
    return app.app.test_client()


def post(client, *files):
    data = {"notebook_files": [(open(path, "rb"), name) for path, name in files]}
    return client.post("/analyze", data=data, content_type="multipart/form-data")


def test_analyze_returns_csv_with_columns_in_detector_order(client, make_notebook):
    notebook = make_notebook("m = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]")
    response = post(client, (notebook, "nested.ipynb"))

    assert response.status_code == 200
    rows = list(csv.reader(io.StringIO(response.data.decode())))
    assert rows[0] == [
        "File", "Cell", "Long Cell", "Long Element Chain",
        "Complex Container Comprehension", "Long Expression", "Complex IF-Conditional",
    ]
    # The only smell is a Long Element Chain, which must land in its own column.
    assert rows[1] == ["nested.ipynb", "1", "0", "1", "0", "0", "0"]


def test_analyze_handles_several_files(client, make_notebook):
    first = make_notebook("x = 1", name="a.ipynb")
    second = make_notebook("y = 2", "z = 3", name="b.ipynb")
    response = post(client, (first, "a.ipynb"), (second, "b.ipynb"))
    rows = list(csv.reader(io.StringIO(response.data.decode())))
    assert [r[0] for r in rows[1:]] == ["a.ipynb", "b.ipynb", "b.ipynb"]


def test_uploaded_file_names_are_sanitized(client, make_notebook, tmp_path):
    notebook = make_notebook("x = 1")
    response = post(client, (notebook, "../../evil.ipynb"))
    assert response.status_code == 200
    assert not (tmp_path / "evil.ipynb").exists()
    assert (tmp_path / "uploads" / "evil.ipynb").exists()


def test_analyze_without_files(client):
    response = client.post("/analyze", data={}, content_type="multipart/form-data")
    assert "Aucun fichier" in response.data.decode()
