from typing import Any, Dict, Set
import ast

class OperandMetricsCalculator:
    """
    Class to calculate and store metrics related to operands in the code.
    """

    # Constants to represent metric types
    TOTAL_OPERANDS = "total_operands"
    UNIQUE_OPERANDS = "unique_operands"

    def __init__(self):
        self._collected_operands: Set[str] = set()
        self._calculated_metrics: Dict[str, int] = {}
        self._internal_data_store: Dict[str, Any] = {}

    def parse_notebook_cell(self, cell: Any) -> None:
        """
        Parse a notebook cell to collect operand metrics.
        
        Args:
            cell (Any): Notebook cell object or code as a string.
        """
        if isinstance(cell, str):
            self._parse_code_string(cell)
        elif hasattr(cell, "cell_type") and cell.cell_type == "code":
            self._parse_code_string(cell.source)

    def _parse_code_string(self, code: str) -> None:
        """
        Parse a code string to collect operand metrics.
        
        Args:
            code (str): Python code as a string.
        """
        try:
            ast_tree = ast.parse(code)
        except SyntaxError as e:
            print(f"SyntaxError encountered: {e}")
            return

        for node in ast.walk(ast_tree):
            if isinstance(node, ast.Name):
                self._collected_operands.add(node.id)

    def get_metrics(self) -> Dict[str, int]:
        """
        Calculate and return operand metrics.
        
        Returns:
            Dict[str, int]: A dictionary containing metrics related to operands.
        """
        self._calculated_metrics[OperandMetricsCalculator.TOTAL_OPERANDS] = len(self._collected_operands)
        self._calculated_metrics[OperandMetricsCalculator.UNIQUE_OPERANDS] = len(set(self._collected_operands))
        self._internal_data_store["collected_operands"] = list(self._collected_operands)

        return self._calculated_metrics
