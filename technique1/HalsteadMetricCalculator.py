try:  # imported as part of the technique1 package (technique2)
    from .OperandsMetricCalculator import OperandMetricsCalculator
    from .OperatorsMetricCalculator import OperatorMetricsCalculator
except ImportError:  # imported as a top-level module (detector.py, app.py)
    from OperandsMetricCalculator import OperandMetricsCalculator
    from OperatorsMetricCalculator import OperatorMetricsCalculator
import math

class Constants:
    AVG_BYTES_PER_OPERAND = 18
    BYTE_THRESHOLD = 3000

class MetricsCalculator:

    """
    A class to encapsulate the calculation of code metrics.
    """

    def __init__(self, code_cell):

        """
        Initialize operand and operator metrics calculators.

        Args:
            code_cell (str): The code cell to analyze.
        """
                
        operand_calculator = OperandMetricsCalculator()
        operator_calculator = OperatorMetricsCalculator()

        operand_calculator.parse_notebook_cell(code_cell)
        operator_calculator.parse_notebook_cell(code_cell)

        self.operand_metrics = operand_calculator.get_metrics()
        self.operator_metrics = operator_calculator.get_metrics()

        self.total_operands = self.operand_metrics.get(OperandMetricsCalculator.TOTAL_OPERANDS, 0)
        self.unique_operands = self.operand_metrics.get(OperandMetricsCalculator.UNIQUE_OPERANDS, 0)

        self.total_operators = self.operator_metrics.get(OperatorMetricsCalculator.TOTAL_OPERATORS, 0)
        self.unique_operators = self.operator_metrics.get(OperatorMetricsCalculator.UNIQUE_OPERATORS, 0)

        self.total_entities = self.total_operators + self.total_operands
        self.total_unique_entities = self.unique_operators + self.unique_operands

    def calculate_volume(self) -> float:
        """Calculate and return the code volume metric."""
        if self.total_unique_entities > 0:
            return self.total_entities * math.log2(self.total_unique_entities)
        return 0.0

    def calculate_difficulty(self) -> float:
        """Calculate and return the code difficulty metric."""
        if self.total_unique_entities > 0 and self.unique_operands > 0:
            return (self.unique_operators / 2) * (self.unique_operands / self.total_unique_entities)
        return 0.0

    def calculate_effort(self) -> float:
        """Calculate and return the code effort metric."""
        return self.calculate_difficulty() * self.calculate_volume()

    def calculate_time_to_implement(self) -> float:
        """Calculate and return the time to implement the code."""
        return self.calculate_effort() / Constants.AVG_BYTES_PER_OPERAND

    def calculate_scaled_volume(self) -> float:
        """Calculate and return the scaled code volume."""
        return self.calculate_volume() / Constants.BYTE_THRESHOLD
