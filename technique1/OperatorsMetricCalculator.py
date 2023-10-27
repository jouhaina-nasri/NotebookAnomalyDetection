from typing import Any, Dict, Set
import ast

class OperatorMetricsCalculator:
    """
    A class for calculating and storing metrics related to operators in the code.
    """

    # Metric names as constants for better maintainability
    TOTAL_OPERATORS = "total_operators"
    UNIQUE_OPERATORS = "unique_operators"

    def __init__(self):
        self._collected_operators: Set[str] = set()
        self._calculated_metrics: Dict[str, int] = {}
        self._internal_data_store: Dict[str, Any] = {}

    def parse_notebook_cell(self, cell: Any) -> None:
        """
        Parse a notebook cell to collect operator metrics.

        Args:
            cell (Any): Notebook cell object or code as a string.
        """
        if isinstance(cell, str):
            self._parse_code_string(cell)
        elif hasattr(cell, "cell_type") and cell.cell_type == "code":
            self._parse_code_string(cell.source)

    def _parse_code_string(self, code: str) -> None:
        """
        Parse a code string to collect operator metrics.

        Args:
            code (str): Python code as a string.
        """
        try:
            ast_tree = ast.parse(code)
        except SyntaxError as e:
            print(f"SyntaxError encountered: {e}")
            return

        for node in ast.walk(ast_tree):
            if isinstance(node, ast.operator):
                self._collected_operators.add(ast.dump(node))

    def get_metrics(self) -> Dict[str, int]:
        """
        Calculate and return operator metrics.

        Returns:
            Dict[str, int]: A dictionary containing metrics related to operators.
        """
        self._calculated_metrics[OperatorMetricsCalculator.TOTAL_OPERATORS] = len(self._collected_operators)
        self._calculated_metrics[OperatorMetricsCalculator.UNIQUE_OPERATORS] = len(set(self._collected_operators))
        self._internal_data_store["collected_operators"] = list(self._collected_operators)

        return self._calculated_metrics
