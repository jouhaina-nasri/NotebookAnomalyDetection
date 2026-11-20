import ast
import warnings

# Analyzed notebooks often contain old-style escapes ('\d' in non-raw strings);
# Python >= 3.12 warns about them when parsing, which only adds noise here.
warnings.filterwarnings('ignore', message='invalid escape sequence')  # SyntaxWarning or DeprecationWarning (< 3.12)

try:  # imported as part of the technique1 package (technique2, tests)
    from .ComprehensionMetricCalculator import count_conditions_per_comprehension, count_loops_per_comprehension,count_loops_and_conditions_in_comprehensions,calculate_comprehension_length
    from .ConditionMetricCalculator import count_if_statements, find_max_if_depths
    from .CyclomaticComplexityCalculator import calculate_cyclomatic_complexity
    from .ElementChainMetricCalculator import extract_nesting_value, extract_element_counts
    from .ExpressionMetricCalculator import extract_assignment_lengths, identify_args_per_expression , identify_methods_per_expression, identify_total_per_expression
    from .HalsteadMetricCalculator import MetricsCalculator
    from .SlocMetricCalculator import count_source_lines_of_code
    from .FunctionnalComplexityCalculator import calculate_complexity
except ImportError:  # imported as a top-level module (detector.py, app.py)
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



# Features used by both detection techniques (rule thresholds and XGBoost model),
# in the order expected by the trained model.
FEATURES = ['SLOC', 'CC', 'FC', 'VOL', 'NOL_NOCC', 'LOC', 'DNA', 'LOEC', 'NOCE', 'DNIC', 'NOIC']


def _max_or_zero(values):
    return max(values) if isinstance(values, list) and values else 0


def to_features(metrics):
    """Reduce the raw metrics of one cell to the 11 features used for detection."""
    return {
        'SLOC': metrics['source_lines_of_code'],
        'CC': metrics['cyclomatic_complexity'],
        'FC': metrics['functional_complexity'],
        'VOL': metrics['volume'],
        'NOL_NOCC': _max_or_zero(metrics.get('loop_and_condition')),
        'LOC': _max_or_zero(metrics.get('comprehension_length')),
        'DNA': _max_or_zero(metrics.get('nested_array_depth')),
        'LOEC': _max_or_zero(metrics.get('element_chain_length')),
        'NOCE': _max_or_zero(metrics.get('expression_length')),
        'DNIC': _max_or_zero(metrics.get('nested_condition_depth')),
        'NOIC': metrics.get('num_conditions', 0),
    }
