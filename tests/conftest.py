import os
import sys

import nbformat
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXTURES = os.path.join(ROOT, "tests", "fixtures")

# technique1 modules are written to be importable both as top-level modules
# (how detector.py and app.py run) and as the technique1 package (technique2).
sys.path.insert(0, os.path.join(ROOT, "technique1"))
sys.path.insert(0, ROOT)


@pytest.fixture
def make_notebook(tmp_path):
    """Write a notebook made of the given code cells and return its path."""

    def _make(*sources, name="sample.ipynb"):
        nb = nbformat.v4.new_notebook()
        nb.cells = [nbformat.v4.new_markdown_cell("# Title")]
        nb.cells += [nbformat.v4.new_code_cell(src) for src in sources]
        path = tmp_path / name
        nbformat.write(nb, str(path))
        return str(path)

    return _make
