import ast

from ComprehensionMetricCalculator import count_conditions_per_comprehension, count_loops_per_comprehension,count_loops_and_conditions_in_comprehensions,calculate_comprehension_length
from ConditionMetricCalculator import count_if_statements, find_max_if_depths
from CyclomaticComplexityCalculator import calculate_cyclomatic_complexity
from ElementChainMetricCalculator import extract_nesting_value, extract_element_counts
from ExpressionMetricCalculator import extract_assignment_lengths, identify_args_per_expression , identify_methods_per_expression, identify_total_per_expression
from HalsteadMetricCalculator import MetricsCalculator
from SlocMetricCalculator import count_source_lines_of_code
from FunctionnalComplexityCalculator import calculate_complexity

from collections import namedtuple

def parse_jupyter_notebook(cell):
    if cell.source.startswith('%'):
        return []

    try:
        cell_ast = ast.parse(cell.source)
    except SyntaxError:
        return []

    # Metrics
    sloc = count_source_lines_of_code(cell.source)
    cyclomatic_complexity = calculate_cyclomatic_complexity(cell_ast)

    metrics_calculator = MetricsCalculator(cell.source)
    volume = metrics_calculator.calculate_volume()
    difficulty = metrics_calculator.calculate_difficulty()
    effort = metrics_calculator.calculate_effort()
    time_to_implement = metrics_calculator.calculate_time_to_implement()
    scaled_volume = metrics_calculator.calculate_scaled_volume()

    functional_complexity = calculate_complexity(cell_ast)
    
    # Comprehensions metrics
    num_loop_comprehension = count_loops_per_comprehension(cell_ast)
    num_conditions_comprehension = count_conditions_per_comprehension(cell_ast)
    loop_and_condition = count_loops_and_conditions_in_comprehensions(cell_ast)
    comprehension_length = calculate_comprehension_length(cell.source, cell_ast)

    # Element chain metrics
    nested_array_depth = extract_nesting_value(cell_ast)
    element_chain_length = extract_element_counts(cell_ast)

    # Expression metrics
    expression_length = extract_assignment_lengths(cell_ast)
    num_methods = identify_methods_per_expression(cell_ast)
    num_args = identify_args_per_expression(cell_ast)
    args_and_methods = identify_total_per_expression(cell_ast)

    # Condition metrics
    nested_condition_depth = find_max_if_depths(cell_ast)
    num_conditions = count_if_statements(cell_ast)

    Metrics = namedtuple('Metrics', [
        'source_lines_of_code',
        'cyclomatic_complexity',
        'functional_complexity',
        'volume',
        'difficulty',
        'effort',
        'time_to_implement',
        'scaled_volume',
        'num_loop_comprehension',
        'num_conditions_comprehension',
        'loop_and_condition',
        'comprehension_length',
        'nested_array_depth',
        'element_chain_length',
        'expression_length',
        'num_methods',
        'num_args',
        'args_and_methods',
        'nested_condition_depth',
        'num_conditions'
    ])

    cell_metrics = Metrics(
        sloc, cyclomatic_complexity, functional_complexity, volume, difficulty, effort, 
        time_to_implement, scaled_volume, num_loop_comprehension, num_conditions_comprehension, 
        loop_and_condition, comprehension_length, nested_array_depth, element_chain_length,
        expression_length, num_methods, num_args, args_and_methods, nested_condition_depth,
        num_conditions
    )

    return [cell_metrics._asdict()]

